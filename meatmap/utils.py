# -*- coding: utf-8 -*-
# Utility functions for accessing the meetup api and processing api data

import csv
import json
import os
import requests
import sys

from meatmap import meetup_api

csv.field_size_limit(sys.maxsize)
HOME = os.getenv("HOME")


def fetch_data(api_key='',
               folder='',
               entities=[],
               prefix='',
               endpoint='',
               extra_fields=[]  # present in some responses but not others
               ):
    for entity in entities:

        json_file = os.path.join(folder, prefix + entity + '.json')
        csv_file = os.path.join(folder, prefix + entity + '.csv')
        args = {'entity': entity}

        if api_key != "NULL" and api_key:
            meetup = meetup_api.MeetupAPIClient(
                http_client=requests,
                headers={},
                params={'key': api_key,
                        'sign': "true",
                        'page': 200  # TODO if > 200 need to handle offset
                        }
            )

            if endpoint:
                api_url = meetup.meetup_api_base + endpoint
                args['api_url'] = api_url

            resp = meetup.get_entity(**args)

            print("dumping %s results to file %s" % (entity, json_file))
            with open(json_file, 'w') as f:
                try:
                    json.dump(resp, f)
                except:
                    print("unable to serialize %s" % resp)

        # build CSV file
        if api_key == "NULL" or not api_key:
            # if no api key, read resp from meetup_folder
            resp = json.load(open(json_file, 'r'))

        print("writing %s results to csv file %s" % (entity, csv_file))
        resp_sheet = build_rows(data=resp, extra=extra_fields)
        write_csv(file=csv_file,
                  data=resp_sheet)
        return


def get_current_groups(meetup_api_key):

    if meetup_api_key == "NULL":
        print("No meetup api key")
        return {}

    meetup = meetup_api.MeetupAPIClient(
        http_client=requests,
        headers={},
        params={'key': meetup_api_key,
                'sign': "true",
                }
    )

    current_groups_resp = meetup.get_entity(entity='groups_self')
    current_groups = {g['urlname']: g for g in current_groups_resp}
    return current_groups


# TODO: this should be a CSV writer class
def build_rows(data={}, extra=[]):
    sheet = []

    # build the header row
    # meetup api entries have different attributes, make sure we get all of
    # the ones in this set
    # add the "extra" fields explicitly for combining responses for
    # different things that might not have the fields within the same grouping
    header_row_set = set(extra)  # list of column headers
    data_expanded = []  # contains JSON object attributes as top level entries
    for i in data:
        row = {}
        for (key, value) in i.items():
            if isinstance(value, dict):  # special handling for JSON objects
                sub_expanded = {'_'.join([key, k]): value[k]
                                for k in value.keys()}

                # combine the new dict with the current row
                row = {**row, **sub_expanded}
                # add any extra keys to the column heading list
                header_row_set.update(sub_expanded.keys() - header_row_set)
            else:
                row[key] = value
                if key not in header_row_set:
                    header_row_set.update([key])
        data_expanded.append(row)
    header_row = sorted(header_row_set)
    sheet.append(header_row)

    # build the data rows
    data_rows = []
    for i in data_expanded:
        row = []
        for column in header_row:  # get the value if the column exists
            if column in i:
                # check if it's a JSON object, if so then just dump it as JSON
                if isinstance(i[column], dict):
                    row.append(json.dumps(dict(sorted(i[column].items()))))
                else:
                    row.append(i[column])
            else:  # set to null to ensure same number of columns in csv
                row.append("")

        data_rows.append(row)

    sheet += data_rows
    return sheet


def write_csv(file=None, data=[]):
    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        for i in data:
            writer.writerow(i)
    return