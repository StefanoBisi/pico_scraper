from sys import argv
import picoscraper


def load_list(filepath):
    metadata = []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            id = line.split('#')[0].strip()
            metadata.append(picoscraper.get_game_metadata(id))
    return metadata


def main():
    list_path = argv[1] if len(argv) > 1 else 'tmp/list.txt'
    metadata = load_list(list_path)
    picoscraper.emulationstation_formatter(metadata)


if __name__ == '__main__':
    main()
