from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

# do not edit
DEVELOPER_KEY = "AIzaSyB7lBnccMIJwLQJWVtNcdqWo4KtBCDQOzk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# query = input("Search: ")
# username = input("Google Username: ")
# password = input("Google Password: ")

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
        get_your_subscriptions(args, 'snippet,contentDetails', True)
        youtube_search(args)
    except HttpError:
        print("An HTTP error occurred:\n%s" % HttpError.content)
