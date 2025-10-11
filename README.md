# pico_scraper
## Pico-8 games metadata scraper

This script fetches pico-8 games' metadata from lexaloffle.com and formats them in the desired output.

The current output formats supported are:
- json
- emulationstation (xml gamelist)

### Usage
>python pico_scraper.py [-h] [--cart-dir CART_DIR] [--cover-dir COVER_DIR] [--no-downloads] [--input-file INPUT_FILE] [--output-file OUTPUT_FILE] {json,emulationstation}
>
>positional arguments:
>
>  {json,emulationstation}
>                        The type of output produced.
>
>options:
>
>  -h, --help:            show this help message and exit
>
>  --cart-dir CART_DIR:   The directory where game carts are stored and where they will be downloaded.
>
>  --cover-dir COVER_DIR:
>                        The directory where game covers are stored and where they will be downloaded.
>
>  --no-downloads:        Toggle if you want to provide the cart and/or cover directories but do not want to download anything in them.
>
>  --input-file INPUT_FILE:
>                        The list file with the games to scrape. Each line of the file must contain the game's id. Everything after '#' is ignored. If not provided, stdin is used instead
>
>  --output-file OUTPUT_FILE:
>                        The output file. If not provided, stdout will be used instead.


### Input Example:

> 11722 # Celeste
>
> 49234 # Just One Boss
>
> 86783 # Celeste 2
>
> 100000 # Birds With Guns
>
> 97269 # Terra

Each line of the input file should contain the game id, as it is found in the game's page link.

Example:
> https://www.lexaloffle.com/bbs/?pid=11722

Anythin starting from a '#' character is considered a comment.

Any leading and trailing whitespaces are ignored.

