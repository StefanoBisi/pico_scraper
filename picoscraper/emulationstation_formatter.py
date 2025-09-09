from sys import argv
import urllib3

def _download_image(url, save_as):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    with open(save_as, 'wb') as file:
        file.write(response.data)


__DUMMY_XML_OPEN = '<?xml version="1.0"?>\n<gameList>'
__DUMMY_XML_GAME = '''<game>
        <path>{cart}</path>
    	<name>{name}</name>
    	<desc>{description}</desc>
    	<image>{cover}</image>
    	<releasedate>{release_date}</releasedate>
    	<developer>{developer}</developer>
    	<publisher>Lexaloffe</publisher>
    	<genre>{tag}</genre>
    	<players>{players_nr}</players>
    </game>
'''
__DUMMY_XML_CLOSE = '</gameList>'


def emulationstation_formatter(metadata, download_images = False):
    gamelist = __DUMMY_XML_OPEN
    for game in metadata:
        cart_path = f'/home/pi/RetroPie/roms/pico8/{game.title}.p8.png'
        cover_path = f'/home/pi/.emulationstation/downloaded_images/pico8/{game.title}.png'
        if download_images:
            _download_image(game.cart_url, cart_path)
            _download_image(game.cover_url, cover_path)

        gamelist += __DUMMY_XML_GAME.format(
            cart = cart_path,
            name = game.title,
            description = game.description,
            cover = cover_path,
            release_date = game.release_date.strftime('%Y%m%dT%H%M%S'),
            developer = game.developer,
            tag = ','.join(game.tags),
            players_nr = 2 if 'multiplayer' in game.tags else 1
        )
    gamelist += __DUMMY_XML_CLOSE
    print (gamelist)
