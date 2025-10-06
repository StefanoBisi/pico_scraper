from sys import argv
from dataclasses import dataclass


@dataclass
class EmulationstationFormatter:

    cart_dir: str
    cover_dir: str

    __DUMMY_XML_OPEN = '<?xml version="1.0"?>\n<gameList>'
    __DUMMY_XML_GAME = '''
    <game>
        <path>{cart}</path>
    	<name>{name}</name>
    	<desc>{description}</desc>
    	<image>{cover}</image>
    	<releasedate>{release_date}</releasedate>
    	<developer>{developer}</developer>
    	<publisher>Lexaloffe</publisher>
    	<genre>{tag}</genre>
    	<players>{players_nr}</players>
    </game>'''
    __DUMMY_XML_CLOSE = '\n</gameList>'

    def format_game(self, game):
        cart_path = f'{self.cart_dir}{game.title}.p8.png'
        cover_path = f'{self.cover_dir}{game.title}.png'

        return self.__DUMMY_XML_GAME.format(
            cart = cart_path,
            name = game.title,
            description = game.description,
            cover = cover_path,
            release_date = game.release_date.strftime('%Y%m%dT%H%M%S'),
            developer = game.developer,
            tag = ','.join(game.tags),
            players_nr = 2 if 'multiplayer' in game.tags else 1
        )    

    def format(self, metadata):
        gamelist = self.__DUMMY_XML_OPEN
        for game in metadata:
            gamelist += self.format_game(game)
        gamelist += self.__DUMMY_XML_CLOSE
        return gamelist
