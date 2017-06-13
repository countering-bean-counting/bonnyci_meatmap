# -*- coding: utf-8 -*-

import click
import csv
import json
import os
import requests

import meatmap
from meatmap import meetup_api

DEFAULT_ANSWER = "IBM Employee interested in Data Science"
DEFAULT_PHOTO = 267200376

@click.command()
@click.option('--meetup_api_key', default="NULL",
              help='Meetup API Key')
@click.option('--groups_file', default="",
              help='List of groups to join (csv)')
@click.option('--join_file', default="",
              help='List of groups with join parameters filled out (csv)')
def main(meetup_api_key, groups_file, join_file):

    # params specific for meetup api join request
    #  this is missing "answer_*" because these vary among groups and has to
    #  be extracted later in the process
    join_params = ['group_id',
                   'group_urlname',
                   'intro',
                   'photo_id'
                   ]

    # additional fields for manual verification and archive
    join_columns = []
    join_columns.append(join_params + [
        'questions',  # JSON dump as these vary among groups
        'questions_required',  # might need to manually update if failure
        'photo_required', # might need to manually update if failure
        'join_response' # indicates whether the group was successfully joined
    ])

    join_data = []

    if groups_file:
        pass
        # read in csv with groups list
        f = open(groups_file, 'r')
        file_contents = csv.reader(f, delimiter=',', quotechar='"')
        groups_data = []

        header_row = file_contents.__next__()

        for row in file_contents:
            group_dict = {header_row[i]:row[i]
                          for i in range(0, len(row))}
            groups_data.append(group_dict)

        for group in groups_data:
            join_params_row = {}
            # extract: group_id, group_urlname
            join_params_row['group_id'] = group['id']
            join_params_row['group_urlname'] = group['urlname']
            join_params_row['intro'] = DEFAULT_ANSWER
            join_params_row['photo_id'] = DEFAULT_PHOTO
            join_params_row['join_response'] = ""

            # check if questions are required
            if group['join_info_questions_req'] == 'True':
                join_params_row['questions_required'] = True

                # create the questions parameters using DEFAULT_ANSWER
                try:
                    questions_json = json.loads(
                        group['join_info_questions'].replace("\'", "\""))
                except:
                    print("unable to deserialize %s"
                          % group['join_info_questions'])
                    questions_json = []

                questions = {'answer_%s' % q['id']: DEFAULT_ANSWER
                             for q in questions_json}
                join_params_row['questions'] = json.dumps(questions)
            else:
                join_params_row['questions_required'] = False
                join_params_row['questions'] = "{}"

            # check if photo is required
            if group['join_info_photo_req']:
                join_params_row['photo_required'] = True
            else:
                join_params_row['photo_required'] = False

            join_data.append(join_params_row)

        # write out join_file
        path, groups_filename = os.path.split(groups_file)
        join_file = os.path.join(path, groups_filename + "_join.csv")
        print("writing join data to %s" % join_file)
        join_data_csv = meatmap.build_rows(join_data)
        meatmap.write_csv(file=join_file,
                  data=join_data_csv)

    elif join_file:
        f = open(join_file, 'r')
        join_data_csv = csv.reader(f, delimiter=',', quotechar='"')
        # TODO convert to list of dicts

    if meetup_api_key != 'NULL':
        # check current group membership and skip any that are already joined
        meetup = meetup_api.MeetupAPIClient(
            http_client=requests,
            headers={},
            params={'key': meetup_api_key,
                    'sign': "true",
                    }
        )

        current_groups_resp = meetup.get_entity(entity='groups_self')
        current_groups = {g['urlname']:g for g in current_groups_resp}

        # make join request
        join_data_result = []
        test_counter = 0
        for group in join_data:

            if group['group_urlname'] not in current_groups:
                # build params
                group_join_params = {p:group[p] for p in join_params}
                if len(group['questions']) > 0:
                    questions_json = json.loads(group['questions'])
                    group_join_qs = { k:v for (k,v) in questions_json.items()}
                    group_join_params = {**group_join_params, **group_join_qs}

                # make api request
                join_resp = meetup.post_entity(
                    entity='post_groups_self',
                    endpoint='/%s/members' % group_join_params['group_urlname'],
                    params=group_join_params)

                print(group['group_urlname'])
                print(join_resp)
                group['join_result'] = join_resp
            else:
                print(group['group_urlname'] + " already joined")
                group['join_result'] = "already joined"

            join_data_result.append(group)

        # TODO: support join_file
        groups_filename, suffix = os.path.splitext(groups_file)
        path, end = os.path.split(groups_file)
        join_result_file = os.path.join(path, groups_filename +
                                     "_join_result.csv")
        print("writing join results to %s" % join_result_file)
        join_data_result_csv = meatmap.build_rows(join_data_result)
        meatmap.write_csv(file=join_result_file,
                  data=join_data_result_csv)
    else:
        print("No meetup_api_key specified")


if __name__ == "__main__":
    main()
