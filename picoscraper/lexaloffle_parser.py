from enum import Enum
import urllib.request
from html.parser import HTMLParser
from . import GameMetadata
from datetime import datetime


_BASE_URL = 'https://www.lexaloffle.com'
_GAME_PAGE_BASE_URL = _BASE_URL + '/bbs/?pid={id}'


class PageContent(Enum):
    No = 0
    Title = 1
    CartData = 2
    Tag = 3
    Description = 4


def _parse_cart_data(cart_data):
    check_data = False
    for line in cart_data.splitlines():
        if check_data:
            parts = line.strip().split(',')
            return parts[6].strip('"'), parts[8].strip('"')

        if line.strip() == 'pdat=[':
            check_data = True
    return '', ''


def _search_attribute(attrs, name):
    for attr in attrs:
        if attr[0] == name and attr[1]:
            return attr[1]
    return ''


class Pico8HTMLParser(HTMLParser):

    _current: GameMetadata
    _next_data: PageContent
    _tag_cache = ''
    _cartembed_nesting = 0
    _loading_description = False


    def __init__(self):
        HTMLParser.__init__(self)
        self._current = GameMetadata.empty()
        self._next_data = PageContent.No


    def handle_starttag(self, tag, attrs):
        global _BASE_URL
        check_description = False
        self._cartembed_nesting += 1 if (self._cartembed_nesting > 0) else 0      
        
        if tag == 'title':
            self._next_data = PageContent.Title
        elif tag == 'script':
            if _search_attribute(attrs, 'id') == 'cart_data_script':
                self._next_data = PageContent.CartData
        elif tag == 'span':
            if _search_attribute(attrs, 'class') == 'tag':
                self._next_data = PageContent.Tag
        elif tag == 'div':
            if _search_attribute(attrs, 'id').startswith('cartembed_'):
                self._cartembed_nesting = 1
        elif tag == 'br':
            check_description = self._loading_description
        elif tag == 'h1':
            if self._loading_description and self._tag_cache not in ['h2', 'p']:
                self._next_data = PageContent.Description
                check_description = True
        elif tag == 'h2':
            if self._loading_description and self._tag_cache != 'p':
                self._next_data = PageContent.Description
                check_description = True
        elif tag == 'p':
            if self._loading_description:
                self._next_data = PageContent.Description
        elif tag == 'meta':
            if _search_attribute(attrs, 'property') == 'og:image':
                self._current.cover_url = _search_attribute(attrs, 'content')
        elif tag == 'a':
            href = _search_attribute(attrs, 'href')
            if href.endswith('.p8.png'):
                self._current.cart_url = _BASE_URL + href

        self._tag_cache = tag
        self._loading_description = check_description


    def handle_endtag(self, tag):
        if self._cartembed_nesting > 0:
            self._cartembed_nesting -= 1
            self._loading_description = (self._cartembed_nesting) == 0


    def handle_data(self, data):
        if self._next_data == PageContent.Title:
            self._current.title = data
        elif self._next_data == PageContent.CartData:
            release_date_str, developer = _parse_cart_data(data)
            self._current.release_date = datetime.strptime(release_date_str, '%Y-%m-%d %H:%M:%S')
            self._current.developer = developer
        elif self._next_data == PageContent.Tag:
            self._current.tags.append(data.strip())
        elif self._next_data == PageContent.Description:
            self._current.description += '\n' + data
            self._current.description = self._current.description.strip('\n')

        self._next_data = PageContent.No
    

    def handle_comment(self, _):
        pass


    def handle_entityref(self, _):
        pass


    def handle_charref(self, _):
        pass


    def handle_decl(self, _):
        pass


    def get_game_metadata(self, html_content):
        self._current = GameMetadata.empty()
        self.feed(html_content)
        return self._current



def get_game_metadata(id):
    url = _GAME_PAGE_BASE_URL.format(id = id)
    content = urllib.request.urlopen(url).read().decode('utf-8')
    parser = Pico8HTMLParser()
    return parser.get_game_metadata(content)
