# -*- coding: utf-8 -*-


# Class to handle talking to the Meetup.com API
class MeetupAPIClient:
    def __init__(self,
                 params={},
                 headers={},
                 owner='',
                 repo='',
                 http_client=None,
                 meetup_api_base='https://api.meetup.com'):

        self.owner = owner
        self.repo = repo
        self.meetup_api_base = meetup_api_base
        self.http_client = http_client
        self.params = params
        self.headers = headers

        self.endpoint_lookup = {
            'calendar': '/self/calendar/',
            'groups_find_bdd': '/find/groups/',
            'groups_self': '/self/groups/'
        }

        self.params_lookup = {
            'events_past': {'status': 'past',
                            'fields': ["comment_count", "photo_album"]},
            'groups_find_bdd': {'topic_id': 1482432,
                                'radius': "global",
                                'fields': "join_info"}
        }

    def _get(self, url="", params={}):
        response = self.http_client.get(url,
                                        headers=self.headers,
                                        params=params)
        self.resp_headers = response.headers
        return response

    def _post(self, url="", params={}):
        response = self.http_client.post(url,
                                        headers=self.headers,
                                        params=params)
        self.resp_headers = response.headers
        return response

    def _build_params(self, entity):
        if entity in self.params_lookup:
            params = {**self.params_lookup[entity], **self.params}
        else:
            params = self.params

        return params

    def _build_endpoint(self, entity):
        # TODO: this should be a proper warning
        if entity not in self.endpoint_lookup:
            print("no endpoint in lookup and no api_url specified")
            return

        endpoint = self.endpoint_lookup[entity]
        api_url = self.meetup_api_base + endpoint
        return api_url

    def get_entity(self, entity='', api_url=''):

        # TODO: this should be a proper warning
        if not entity:
            print("no entity specified for get_entity()")
            return

        params = self._build_params(entity)

        if not api_url:
            api_url = self._build_endpoint(entity)

        response = self._get(url=api_url, params=params)
        if response.status_code != 200:
            return {'no_%s' % entity: "%s %s" %
                                      (str(response.status_code), response)}
        else:
            return response.json()

    def post_entity(self, entity='', endpoint='', params={}):
        api_url = self._build_endpoint(entity)

        global_params = self._build_params(entity)
        global_params = {**global_params, **params}

        response = self._post(url=api_url, params=global_params)
        if response.status_code != 200:
            return {'%s failed' % entity: "%s %s" %
                                      (
                                      str(response.status_code),
                                      response.content)}
        else:
            return response.json()