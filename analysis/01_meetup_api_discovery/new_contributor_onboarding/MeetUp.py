import MeetUp_Info as mac
import meetup.api

def get_events(*requirements):
	return (meetup.api.GetEvents(requirements))


if ___name___ == '__main__':
	print(get_events("Big Data Developers"))