from enum import Enum
from dataclasses import dataclass
import urllib.request
from html.parser import HTMLParser


__BASE_URL = 'https://www.lexaloffle.com/bbs/?pid={id}'


class PageContent(Enum):
    No = 0
    Title = 1
    CartData = 2


@dataclass
class GameMetadata:
    title: str
    developer: str
    release_date: str


def empty_metadata() -> GameMetadata:
    return GameMetadata('', '', '')


def parse_cart_data(cart_data: str) -> tuple[str, str]:
    check_data = False
    for line in cart_data.splitlines():
        if check_data:
            parts = line.strip().split(',')
            return parts[6], parts[8]

        if line.strip() == 'pdat=[':
            check_data = True
    return '', ''


class Pico8HTMLParser(HTMLParser):

    _current: GameMetadata
    _next_data: PageContent


    def __init__(self):
        HTMLParser.__init__(self)
        self._current = empty_metadata()
        self._next_data = PageContent.No


    def handle_starttag(self, tag, attrs):
        match tag:
            case 'title':
                self._next_data = PageContent.Title
            case 'script':
                for attr in attrs:
                    if attr[0] == 'id' and attr[1] == 'cart_data_script':
                        self._next_data = PageContent.CartData


    def handle_endtag(self, tag):
        pass


    def handle_data(self, data):
        match self._next_data:
            case PageContent.Title:
                self._current.title = data
            case PageContent.CartData:
                release_date, developer = parse_cart_data(data)
                self._current.release_date = release_date
                self._current.developer = developer

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
    url = __BASE_URL.format(id = id)
    content = urllib.request.urlopen(url).read()
    return content.decode("utf-8")


def get_game_metadata(id: str) -> GameMetadata:
    content = get_page_content(id)
    parser = Pico8HTMLParser()
    return parser.get_game_metadata(content)


def main():
    metadata = get_game_metadata('100000')
    print(metadata.title)
    print(metadata.release_date)
    print(metadata.developer)

if __name__ == '__main__':
    main()