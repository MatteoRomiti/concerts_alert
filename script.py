import facebook
import requests
user_id = '1504466901'
token = 'EAACEdEose0cBAI5OO1mqhCignGj9mk6xqnjy2ua07ZBH1x79BGXWiKVLk7NPJaeWIFMLxK4cBFbluOJnKhCZBeoK5XGDtw8LmU2Taq3pl5SnY2QT8AAbzpGZCpjKYf5KIMuWQnRsHgkTOtQKtRTKspOlXu8ZB5OHfbNNMiILj8m7PWZCG3A2s6kcBsOhC8xoZD'

graph = facebook.GraphAPI(access_token=token)

all_musics_name_id = []

# Wrap this block in a while loop so we can keep paginating requests until
# finished.
musics = graph.get_connections("me", "music")
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
artist = 'PISETZKY'
limit = 5
# for n in range(len(all_musics_name_id)):
# for n in range(limit):
# 	print(all_musics_name_id[n])

artist_events = graph.get_object('480455975379128', fields='events')
# artist_events_list = [event['name'] for event in artist_events['events']]
print(artist_events.keys())
# print(artist_events['events']['data'][0])
