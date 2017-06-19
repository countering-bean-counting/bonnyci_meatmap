# -*- coding: utf-8 -*-

import click
import csv
import os

from meatmap import utils

# List of what should be fetched from api
# TODO: these should be set by a file or from cli
ENTITIES = ['events_past']
EXTRA_FIELDS = ['duration',
                'how_to_find_us',
                'manual_attendance_count',
                'rsvp_limit',
                'rsvp_close_offset',
                'rsvp_open_offset',
                'venue_address_2',
                'venue_phone',
                'venue_state',
                'venue_zip']


@click.command()
@click.option('--meetup_api_key', default="NULL",
              help='Meetup API Key')
@click.option('--meetup_folder', default="",
              help='Results output destination')
@click.option('--no_fetch', default=True,
              help="Don't fetch past events from the API, combine existing "
                   "files only")
@click.option('--prefix', default="",
              help="prepend to output file per group set (eg, big_data_devs")
def main(meetup_api_key, meetup_folder, no_fetch, prefix):

    # get current groups
    current_groups = utils.get_current_groups(meetup_api_key)

    # for each group in the list, get events
    for group in current_groups.keys():
        args = { 'folder': meetup_folder,
                 'entities': ENTITIES,
                 'prefix': group + '_',
                 'endpoint': "/%s/events" % group,
                 'extra_fields': EXTRA_FIELDS}

        # get the data from the api, otherwise just rebuild individual csvs
        # from the existing json files
        if no_fetch == "False":
            args['api_key'] = meetup_api_key,

        # save as json and csv, prefix = urlname
        utils.fetch_data(**args)

    # combine individual files into a single csv file
    for entity in ENTITIES:
        csv_combined = []
        print("Combining csv files for %s " % entity)

        for group in current_groups.keys():
            csv_filename = group + '_' + entity + '.csv'
            csv_file = os.path.join(meetup_folder, csv_filename)
            print("Reading in %s " % csv_file)

            # read in csv file contents
            try:
                f = open(csv_file, 'r')
                file_contents = csv.reader(f, delimiter=',', quotechar='"')

            except FileNotFoundError:
                print("%s not found" % csv_file)
                continue

            # if this is the first entry, keep the header row
            # add the group_urlname to identify which group the event goes with
            next_row = file_contents.__next__()
            if len(csv_combined) == 0:
                header_row = next_row
                header_row += ["group_urlname"]
                csv_combined.append(header_row)

            for row in file_contents:
                row += [group]
                csv_combined.append(row)

        # write out combined file
        combined_csv_file = os.path.join(meetup_folder,
                                         prefix + entity + '.csv')
        with open(combined_csv_file, 'w') as f:
            print("Writing combined csv file %s " % combined_csv_file)
            writer = csv.writer(f, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
            for row in csv_combined:
                writer.writerow(row)



if __name__ == "__main__":
    main()
