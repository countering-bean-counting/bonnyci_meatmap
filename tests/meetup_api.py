import unittest
from unittest.mock import patch

from meatmap import meetup_api


class MockMeetupAPIClient:
    def __init__(self):
        self.groups = [{
                "score": 1,
                "id": 9516272,
                "name": "Big Data Developers in London",
                "link": "https://www.meetup.com/Big-Data-Analytics-in-London/",
                "urlname": "Big-Data-Analytics-in-London",
                "description": "<p>Foo</p>",
                "created": 1374780559000,
                "city": "London",
                "country": "GB",
                "localized_country_name": "United Kingdom",
                "state": "17",
                "join_mode": "open",
                "visibility": "public",
                "lat": 51.51,
                "lon": -0.08,
                "members": 6013,
                "organizer": {
                    "id": 200241805,
                    "name": "Nancy Berlin",
                    "bio": "",
                    "photo": {
                        "id": 259100946,
                        "highres_link": "highres_259100946.jpeg",
                        "photo_link": "member_259100946.jpeg",
                        "thumb_link": "thumb_259100946.jpeg",
                        "type": "member",
                        "base_url": "https://secure.meetupstatic.com"
                        }
                },
                "who": "Data Mashers",
                "group_photo": {
                    "id": 363299282,
                    "highres_link": "highres_363299282.jpeg",
                    "photo_link": "600_363299282.jpeg",
                    "thumb_link": "thumb_363299282.jpeg",
                    "type": "event",
                    "base_url": "https://secure.meetupstatic.com"
                    },
                "timezone": "Europe/London",
                "next_event": {
                    "id": "240025089",
                    "name": "Java & the GPU - all you need to know",
                    "yes_rsvp_count": 63,
                    "time": 1495732500000,
                    "utc_offset": 3600000
                    },
                "category": {
                    "id": 34,
                    "name": "Tech",
                    "shortname": "Tech",
                    "sort_name": "Tech"
                    }
            }
        ]


class TestMeetupAPIClient(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _get(self, mock_data, status_code=200):
        with patch('requests.Request') as mock:
            http_fake = mock.return_value
            http_fake.get.return_value = type('obj', (object,),
                                              {"json": lambda: mock_data,
                                               "status_code": status_code,
                                               "headers": {}})
            return http_fake

    def test_get_entity(self):
        mock_groups = MockMeetupAPIClient().groups
        http_fake = self._get(mock_groups)
        meetup = meetup_api.MeetupAPIClient(http_client=http_fake)
        groups = meetup.get_entity('groups_find_bdd')

        # check that our return structure is keyed on event type
        print(groups[0]['name'])
        self.assertEqual(groups[0]['name'], "Big Data Developers in London",
                         msg="%s not in response " % mock_groups[0]['name'])
        self.assertEqual(len(groups), 1)

        # TODO fix this
        got = groups[0]
        expected = mock_groups[0]

        for e in expected:
            # check that we didn't drop any fields
            self.assertTrue(e in got, msg="missing %s" % e)
            # check that the values we expected got set
            self.assertEqual(expected[e], got[e], msg="%s value "
                             "didn't match: expected %s, got %s" %
                                                      (e, expected[e], got[e]))

        # check that we didn't pick up any extra values
        self.assertEqual(sorted(expected.keys()), sorted(got.keys()),
                         msg="found extra values")


if __name__ == '__main__':
    unittest.main()
