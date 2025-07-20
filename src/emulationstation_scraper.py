import pico_scraper
from sys import argv
import urllib3

#20010619T000000
def download_image(url, save_as):
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
    </game>'''
__DUMMY_XML_CLOSE = '</gameList>'



def main():
    list_path = argv[1] if len(argv) > 1 else 'tmp/list.txt'
    metadata = pico_scraper.load_list(list_path)

    gamelist = __DUMMY_XML_OPEN
    for game in metadata:
        cart_path = f'/home/pi/RetroPie/roms/pico8/{game.title}.p8.png'
        download_image(game.cart_url, cart_path)

        cover_path = '/home/pi/.emulationstation/downloaded_images/pico8'
        download_image(game.cover_url, cover_path)

        gamelist += __DUMMY_XML_GAME.format(
            cart = cart_path,
            name = game.title,
            description = game.description,
            cover = cover_path,
            release_data = game.release_date.strftime('%Y%m%dT%H%M%S'),
            developer = game.developer,
            tag = game.tag,
            players_nr = game.players
        )
    gamelist += __DUMMY_XML_CLOSE
    print (gamelist)


if __name__ == '__main__':
    main()