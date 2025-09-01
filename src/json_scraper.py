import pico_scraper
import json
from dataclasses import asdict
from sys import argv


_JSON_METADATA_STR = '''{{
  "id": {id},
  "title": {title},
  "cart_url": {cart_url},
  "cover_url": {cover_url},
  "developer": {developer},
  "release_date": {release_date},
  "tags": {tags},
  "description": {description}
}}'''


def from_json(json_data):
    data = json.loads(json_data)
    return pico_scraper.GameMetadata(
        data['id'],
        data['title'],
        data['cart_url'],
        data['cover_url'],
        data['developer'],
        data['release_date'],
        data['tags'],
        data['description']
    )


def to_json(metadata):
    json_data = []
    for game in metadata:
        json_data.append(
            _JSON_METADATA_STR.format(
                id = game.id,
                title = json.dumps(game.title),
                cart_url = json.dumps(game.cart_url),
                cover_url = json.dumps(game.cover_url),
                developer = json.dumps(game.developer),
                release_date = json.dumps(game.release_date.strftime('%Y%m%dT%H%M%S')),
                tags = json.dumps(game.tags),
                description = json.dumps(game.description)
            )
        )
    print('[{games}]'.format(
        games = ','.join(json_data)
    ))


def main():
    list_path = argv[1] if len(argv) > 1 else 'tmp/list.txt'
    metadata = pico_scraper.load_list(list_path)
    to_json(metadata)


if __name__ == '__main__':
    main()
