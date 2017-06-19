# -*- coding: utf-8 -*-

import click

from meatmap import utils

# List of what should be fetched from api
# TODO: these should be set by a file or from cli
ENTITIES = ['calendar']


@click.command()
@click.option('--meetup_api_key', default="NULL",
              help='Meetup API Key')
@click.option('--meetup_folder', default="",
              help='Results output destination')
@click.option('--prefix', default="default_",
              help='Prefix to prepend to output files to differentiate ' \
                   'between api accounts')
def main(meetup_api_key, meetup_folder, prefix):
    utils.fetch_data(api_key=meetup_api_key,
                     folder=meetup_folder,
                     entities=ENTITIES,
                     prefix=prefix)

if __name__ == "__main__":
    main()
