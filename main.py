import httplib2
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client import client

import webbrowser

# do not edit
DEVELOPER_KEY = "AIzaSyB7lBnccMIJwLQJWVtNcdqWo4KtBCDQOzk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def make_flow():
    # creates a flow. flow is an object Google uses to manage API requests
    server_flow = client.flow_from_clientsecrets('client_secret.json',
                                                 scope='https://www.googleapis.com/auth/youtube.readonly',
                                                 redirect_uri='urn:ietf:wg:oauth:2.0:oob')
    server_flow.params['access_type'] = 'offline'           # offline access
    server_flow.params['include_granted_scopes'] = 'true'   # incremental auth

    # authorizes app to request API for user without user needing to get a key
    auth_uri = server_flow.step1_get_authorize_url()
    webbrowser.open(auth_uri)
    webbrowser.get()
    user_auth_code = input("Paste your code: ")

    # turns user's auth code into credentials we can use on their behalf
    # refresh token is used to get new credentials without prompting for user auth again
    # flow automatically sends refresh tokens as long as app runs & user access not revoked
    credentials = server_flow.step2_exchange(user_auth_code)
    http_auth = credentials.authorize(httplib2.Http())

    # builds the youtube object with all proper authentication
    # this is used for all API calls
    doottube = build('youtube', 'v3', http=http_auth)
    return doottube


def print_results(results):
    for item in results.get("items", []):
        channelid = item['snippet']['resourceId']['channelId']
        print(channelid)


def get_your_subscriptions():
    results = tube.subscriptions().list(
        mine='true',
        part='snippet'
    ).execute()

    channel_ids = {}

    for item in results.get("items", []):
        channel_title = item['snippet']['title']
        channel_id = item['snippet']['resourceId']['channelId']
        channel_ids[channel_id] = channel_title

    print(len(channel_ids), "subscriptions\n")
    return channel_ids


def youtube_search(subscriptions):
    for channel_id in subscriptions.keys():
        search_response = tube.search().list(
            q=query,
            part="id,snippet",
            maxResults='3',
            channelId=channel_id
        ).execute()

        videos = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                videos.append("%s (https://www.youtube.com/watch?v=%s)" % (search_result["snippet"]["title"],
                                                                           search_result["id"]["videoId"]))

        print("=== " + subscriptions[channel_id] + " ===")
        for video in videos:
            print("-" + video)
        print("")


if __name__ == "__main__":
    tube = make_flow()

    while True:
        query = input("Search: ")
        if query == 'quit':
            break
        try:
            user_subscriptions = get_your_subscriptions()
            youtube_search(user_subscriptions)
        except HttpError:
            print("An HTTP error occurred:\n%s" % HttpError.content)