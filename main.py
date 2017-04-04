from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import requests
from oauth2client import client
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from requests.adapters import HTTPAdapter

import webbrowser

# do not edit
DEVELOPER_KEY = "AIzaSyB7lBnccMIJwLQJWVtNcdqWo4KtBCDQOzk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
# old client id: 943664900152-7ghb5t5pmh8c9bueoo23bkmutk1vptge.apps.googleusercontent.com
# old secret: wENVvmv0uSErthc219GxssgS

# query = input("Search: ")
# username = input("Google Username: ")
# password = input("Google Password: ")

# webbrowser.open("https://accounts.google.com/o/oauth2/auth?client_id=943664900152-7ghb5t5pmh8c9bueoo23bkmutk1vptge.apps.googleusercontent.com&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://gdata.youtube.com&response_type=code")
# webbrowser.get()
# user_auth_code = input("Paste your code: ")

secrets_flow = client.flow_from_clientsecrets('client_secret.json', scope='https://www.googleapis.com/auth/youtube.readonly',redirect_uri='urn:ietf:wg:oauth:2.0:oob')
secrets_flow.params['access_type'] = 'offline'         # offline access
secrets_flow.params['include_granted_scopes'] = True   # incremental auth

server_flow = OAuth2WebServerFlow(client_id='943664900152-7ghb5t5pmh8c9bueoo23bkmutk1vptge.apps.googleusercontent.com',
                                  client_secret='wENVvmv0uSErthc219GxssgS',
                                  scope='https://www.googleapis.com/auth/youtube.readonly',
                                  redirect_uri='urn:ietf:wg:oauth:2.0:oob')

auth_uri = server_flow.step1_get_authorize_url()
webbrowser.open(auth_uri)
webbrowser.get()
user_auth_code = input("Paste your code: ")

credentials = server_flow.step2_exchange(user_auth_code)

# data = {'code': user_auth_code + '&'+
#         'client_id=943664900152-7ghb5t5pmh8c9bueoo23bkmutk1vptge.apps.googleusercontent.com&' +
#         'client_secret=wENVvmv0uSErthc219GxssgS&' +
#         'redirect_uri=http://localhost/oauth2callback&' +
#         'grant_type=authorization_code'}

# r = requests.post('http://www.googleapis.com/oauth2/v4/token', data)
# print(r.status_code)
# print(r.reason)

# r = requests.post('gdata.youtube.com', code='4/XaJRwp3icDTqSI7gn3VRfFbr6Zr_XGbA3-G3Kbzmku8',
#                  client_id='943664900152-7ghb5t5pmh8c9bueoo23bkmutk1vptge.apps.googleusercontent.com',
#                  client_secret ='wENVvmv0uSErthc219GxssgS',
#                  redirect_uri='http://localhost/oauth2callback',
#                  grant_type='authorization_code')
# r.json()

channel_id = "UCq6VFHwMzcMXbuKyG7SQYIg"
query = "ghost in the shell"

# usable after we integrate OAUTH2
# def get_your_subscriptions(service, part, mine):
#   service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
#
#   results = service.subscriptions().list(
#     mine=mine,
#     part=part
#   ).execute()
#
#   print(results)
#   pass


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results,
        channelId=options.channel_id
    ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (https://www.youtube.com/watch?v=%s)" % (search_result["snippet"]["title"],
                                                                       search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))

    print("Videos:\n", "\n".join(videos), "\n")
    print("Channels:\n", "\n".join(channels), "\n")
    print("Playlists:\n", "\n".join(playlists), "\n")


if __name__ == "__main__":
    argparser.add_argument("--channel-id", help="Channel ID", default=channel_id)
    argparser.add_argument("--q", help="Search term", default=query)
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()

    try:
        # get_your_subscriptions(args, 'snippet,contentDetails', True)
        youtube_search(args)
    except HttpError:
        print("An HTTP error occurred:\n%s" % HttpError.content)
