import sys
import picoscraper
import argparse
from enum import Enum
import urllib3
import os


class OutputType(Enum):
    json = 'json'
    emulationstation = 'emulationstation'

    def __str__(self):
        return self.value


def get_args():
    parser = argparse.ArgumentParser(prog = 'pico_scraper')
    parser.add_argument('--cart-dir', default='', help='The directory where game carts are stored and where they will be downloaded.')
    parser.add_argument('--cover-dir', default='', help='The directory where game covers are stored and where they will be downloaded.')
    parser.add_argument('--no-downloads', action='store_true', help='''Toggle if you want to provide the cart and/or cover directories
                        but do not want to download anything in them.''')
    parser.add_argument('--input-file', default='', help='''The list file with the games to scrape.
                        Each line of the file must contain the game's id.
                        Everything after '#' is ignored.
                        If not provided, stdin will be used instead''')
    parser.add_argument('--output-file', default='', help='The output file. If not provided, stdout will be used instead.')
    parser.add_argument('output_type', type = OutputType, choices=list(OutputType), help='The type of output produced.')
    return parser.parse_args(sys.argv[1:])


def check_existence(path):
    if not os.path.exists(path):
        sys.stderr.write(f'Error: {path} does not exist.\n')
        exit(1)


def check_permission(path):
    if not os.path.exists(path):
        return
    if not (os.access(path, os.R_OK) and os.access(path, os.W_OK)):
        sys.stderr.write(f'Error: No read/write permissions for {path}\n')
        exit(1)


def check_dir(path):
    check_existence(path)
    if not os.path.isdir(path):
        sys.stderr.write(f'Error: {path} is not a directory.\n')
        exit(1)
    check_permission(path)


def check_args(args):
    if args.cart_dir:
        args.cart_dir = args.cart_dir.rstrip('/')
        check_dir(args.cart_dir)
    if args.cover_dir:
        args.cover_dir = args.cover_dir.rstrip('/')
        check_dir(args.cover_dir)
    
    if args.input_file:
        check_existence(args.input_file)
        check_permission(args.input_file)
    
    if args.output_file:
        check_permission(args.output_file)


def load_file(filepath):
    metadata = []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            id = line.split('#')[0].strip()
            metadata.append(picoscraper.get_game_metadata(id))
    return metadata


def load_stdin():
    metadata = []
    for line in sys.stdin:
        id = line.split('#')[0].strip()
        metadata.append(picoscraper.get_game_metadata(id))
    return metadata


def download_image(url, save_as):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    with open(save_as, 'wb') as file:
        file.write(response.data)


def main():
    args = get_args()
    check_args(args)

    metadata = load_file(args.input_file) \
                if len(args.input_file) > 0 \
                else load_stdin()
    
    for game in metadata:
        if len(args.cart_dir) > 0 and not args.no_downloads:
            if len(game.cart_url) == 0:
                sys.stderr.write(f'Error: Missing cart url for {game.title}.\n')
                exit(1)
            download_image(game.cart_url, f'{args.cart_dir}/{game.title}.p8.png')
        if len(args.cover_dir) > 0 and not args.no_downloads:
            if len(game.cart_url) == 0:
                sys.stderr.write(f'Error: Missing cover url for {game.title}.\n')
                exit(1)
            download_image(game.cover_url, f'{args.cover_dir}/{game.title}.png')

    output = ''
    if args.output_type == OutputType.emulationstation:
        formatter = picoscraper.EmulationstationFormatter(args.cart_dir, args.cover_dir)
        output = formatter.format(metadata)
    elif args.output_type == OutputType.json:
        formatter = picoscraper.JsonFormatter()
        output = formatter.format(metadata)
        pass

    if args.output_file:
        with open(args.output_file, 'w') as outf:
            outf.write(output)
    else:
        print(output)

if __name__ == '__main__':
    main()
