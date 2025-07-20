from enum import Enum
from dataclasses import dataclass
import urllib.request
from html.parser import HTMLParser
from datetime import datetime


_BASE_URL = 'https://www.lexaloffle.com'
_GAME_PAGE_BASE_URL = _BASE_URL + '/bbs/?pid={id}'


class PageContent(Enum):
    No = 0
    Title = 1
    CartData = 2
    Tag = 3
    Description = 4


@dataclass
class GameMetadata:
    title: str
    cart_url: str
    cover_url: str
    developer: str
    release_date: datetime
    tag: str
    description: str
    players: int


def empty_metadata() -> GameMetadata:
    return GameMetadata('', '', '', '', datetime.fromtimestamp(0), '', '', 1)


def print_metadata(metadata: GameMetadata):
    print(f'{metadata.title}\n---')
    print(f'{metadata.cart_url}\n---')
    print(f'{metadata.cover_url}\n---')
    print(f'{metadata.release_date}\n---')
    print(f'{metadata.developer}\n---')
    print(f'{metadata.tag}\n---')
    print(f'{metadata.description}\n---')
    print(f'{metadata.players}\n---')


def parse_cart_data(cart_data: str) -> tuple[str, str]:
    check_data = False
    for line in cart_data.splitlines():
        if check_data:
            parts = line.strip().split(',')
            return parts[6].strip('"'), parts[8].strip('"')

        if line.strip() == 'pdat=[':
            check_data = True
    return '', ''


def search_attribute(attrs: list[tuple[str,str|None]], name: str) -> str:
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
        self._current = empty_metadata()
        self._next_data = PageContent.No


    def handle_starttag(self, tag, attrs):
        global _BASE_URL
        check_description = False
        self._cartembed_nesting += 1 if (self._cartembed_nesting > 0) else 0
        
        match tag:
            case 'title':
                self._next_data = PageContent.Title
            case 'script':
                if search_attribute(attrs, 'id') == 'cart_data_script':
                    self._next_data = PageContent.CartData
            case 'span':
                if search_attribute(attrs, 'class') == 'tag':
                    self._next_data = PageContent.Tag
            case 'div':
                if search_attribute(attrs, 'id').startswith('cartembed_'):
                    self._cartembed_nesting = 1
            case 'br':
                check_description = self._loading_description
            case 'h1':
                if self._loading_description and self._tag_cache not in ['h2', 'p']:
                    self._next_data = PageContent.Description
                    check_description = True
            case 'h2':
                if self._loading_description and self._tag_cache != 'p':
                    self._next_data = PageContent.Description
                    check_description = True
            case 'p':
                if self._loading_description:
                    self._next_data = PageContent.Description
            case 'meta':
                if search_attribute(attrs, 'property') == 'og:image':
                    self._current.cover_url = search_attribute(attrs, 'content')
            case 'a':
                href = search_attribute(attrs, 'href')
                if href.endswith('.p8.png'):
                    self._current.cart_url = _BASE_URL + href

        self._tag_cache = tag
        self._loading_description = check_description


    def handle_endtag(self, tag):
        if self._cartembed_nesting > 0:
            self._cartembed_nesting -= 1
            self._loading_description = (self._cartembed_nesting) == 0


    def handle_data(self, data):
        match self._next_data:
            case PageContent.Title:
                self._current.title = data
            case PageContent.CartData:
                release_date_str, developer = parse_cart_data(data)
                self._current.release_date = datetime.strptime(release_date_str, '%Y-%m-%d %H:%M:%S')
                self._current.developer = developer
            case PageContent.Tag:
                match data.strip():
                    case 'singleplayer':
                        self._current.players = 1
                    case 'multiplayer':
                        self._current.players = 2
                    case _:
                        if len(self._current.tag) == 0:
                            self._current.tag = data
            case PageContent.Description:
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


    def get_game_metadata(self, html_content: str) -> GameMetadata:
        self._current = empty_metadata()
        self.feed(html_content)
        return self._current


def get_page_content(id: str) -> str:
    url = _GAME_PAGE_BASE_URL.format(id = id)
    content = urllib.request.urlopen(url).read()
    return content.decode("utf-8")


def get_game_metadata(id: str) -> GameMetadata:
    content = get_page_content(id)
    parser = Pico8HTMLParser()
    return parser.get_game_metadata(content)


def load_list(filepath: str) -> list[GameMetadata]:
    metadata = []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            id = line.split('#')[0].strip()
            metadata.append(get_game_metadata(id))
    return metadata


def main():
    metadata = load_list('tmp/list.txt')
    for game in metadata:
        print_metadata(game)
        print()


if __name__ == '__main__':
    main()