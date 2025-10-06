from . import GameMetadata
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
    return GameMetadata(
        data['id'],
        data['title'],
        data['cart_url'],
        data['cover_url'],
        data['developer'],
        data['release_date'],
        data['tags'],
        data['description']
    )


class JsonFormatter:

    def format_game(self, game):
        return _JSON_METADATA_STR.format(
            id = game.id,
            title = json.dumps(game.title),
            cart_url = json.dumps(game.cart_url),
            cover_url = json.dumps(game.cover_url),
            developer = json.dumps(game.developer),
            release_date = json.dumps(game.release_date.strftime('%Y%m%dT%H%M%S')),
            tags = json.dumps(game.tags),
            description = json.dumps(game.description)
        )
    
    def format(self, metadata):
        json_data = []
        for game in metadata:
            json_data.append(self.format_game(game))
        return '[{games}]'.format(games = ','.join(json_data))
