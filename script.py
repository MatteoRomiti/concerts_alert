import time
import datetime
import facebook
import requests
import private

city_of_interest = 'Paris' # where the event should be
events_of_interest = [] # all the available events in city_of_interest, list of [artist_name, start_time]
all_musics_name_id = [] # list of [artist_name, artist_id] 
# today_date = datetime.datetime.now().strftime("%Y-%m-%d")
current_timestamp = time.time()
graph = facebook.GraphAPI(access_token=private.token)
musics = graph.get_connections("me", "music") # my likes about music

print "Retrieving all your Music Likes..."
while(True):
	try:
		for music in musics['data']:
			all_musics_name_id.append([music['name'].encode('utf-8'), music['id'].encode('utf-8')])
		# Attempt to make a request to the next page of data, if it exists.
		musics=requests.get(musics['paging']['next']).json()
	except KeyError:
		# When there are no more pages (['paging']['next']), break from the
		# loop and end the script.
		break
print "Done."

print "Looking for interesting events in " + city_of_interest + "..."
for n in range(len(all_musics_name_id)): # loop over all the artists
# for n in range(30): # loop over all the artists
	artist_name = all_musics_name_id[n][0]
	artist_id = all_musics_name_id[n][1]
	# print '-'*10 + 'Artist: ' + artist_name + '-'*10
	artist_events = graph.get_object(artist_id, fields='events') # get all the events for one artist
	if 'events' in artist_events.keys(): # some artists do not have "events" section

		for event_number in range(len(artist_events['events']['data'])): # loop over all the events of one artist
			event_city = 'Not Available'
			event_date = 'Not Available'
			event_start_timestamp = 0 # when the event is not available, it'll be considered as past
			try:
				event_city = artist_events['events']['data'][event_number]['place']['location']['city']					
				# print "City: " + event_city
			except: 
				pass
				# print "No city available for this event"
			try:
				event_date = artist_events['events']['data'][event_number]['start_time'][:10] # TODO1: take care of the time
				event_start_timestamp = time.mktime(datetime.datetime.strptime(event_date, "%Y-%m-%d").timetuple())
				# print "Date: " + event_date
			except: 
				pass
				# print "No city start time for this event"
			if event_city == city_of_interest and current_timestamp < (event_start_timestamp+86400): # why +86400? maybe you want to know if you just missed an event, but also because of TODO1
				events_of_interest.append([artist_name, event_date])

	else:
		pass
		# print "No public events on Facebook for this artist"
print "Done."

print "Your interesting events:"
for event in events_of_interest:
	print "-"*20
	print "Artist: " + event[0]
	print "Date: " + event[1][:10]