import sys
import picoscraper
import argparse
from enum import Enum
import urllib3


class OutputType(Enum):
    json = 'json'
    emulationstation = 'emulationstation'

    def __str__(self):
        return self.value


def _getArgs():
    parser = argparse.ArgumentParser(prog = 'pico_scraper')
    parser.add_argument('--cart-dir', default='')
    parser.add_argument('--cover-dir', default='')
    parser.add_argument('--no-downloads', action='store_true')
    parser.add_argument('--input-file', default='')
    parser.add_argument('output_type', type = OutputType, choices=list(OutputType))
    return parser.parse_args(sys.argv[1:])


def _load_file(filepath):
    metadata = []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            id = line.split('#')[0].strip()
            metadata.append(picoscraper.get_game_metadata(id))
    return metadata


def _load_stdin():
    metadata = []
    for line in sys.stdin:
        id = line.split('#')[0].strip()
        metadata.append(picoscraper.get_game_metadata(id))
    return metadata


def _download_image(url, save_as):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    with open(save_as, 'wb') as file:
        file.write(response.data)


def main():
    args = _getArgs()
    metadata = _load_file(args.input_file) \
                if len(args.input_file) > 0 \
                else _load_stdin()
    
    for game in metadata:
        if len(args.cart_dir) > 0 and not args.no_downloads:
            _download_image(game.cart_url, f'{args.cart_dir}{game.title}.p8.png')
        if len(args.cover_dir) > 0 and not args.no_downloads:
            _download_image(game.cover_url, f'{args.cover_dir}{game.title}.png')

    if args.output_type == OutputType.emulationstation:
        formatter = picoscraper.EmulationstationFormatter(args.cart_dir, args.cover_dir)
        print(formatter.format(metadata))
    elif args.output_type == OutputType.json:
        formatter = picoscraper.JsonFormatter()
        print(formatter.format(metadata))
        pass


if __name__ == '__main__':
    main()
