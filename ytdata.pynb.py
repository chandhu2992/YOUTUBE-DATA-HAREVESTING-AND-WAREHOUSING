#pip installing google api 
pip install google-api-python-client

# %%
import googleapiclient.discovery

# %%
api_service_name = "youtube" 
api_version = "v3" 

# %%
api_key="AIzaSyBmYd2AH1Yhvn0yIbf1rExtP4dbe8RVCBA"


# %%
youtube = googleapiclient.discovery.build(api_service_name,api_version,developerKey=api_key)

# %%
request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id="UCsg785FQn_egpJITE9mfwiQ"
    )
response = request.execute()

# %%
def channel_data(c_id):
    request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=c_id
    )
    response = request.execute()
    data = {"channel_name":response['items'][0]['snippet']['title'],
        "channel_desc":response['items'][0]['snippet']['description'],
        "channel_pub":response['items'][0]['snippet']['publishedAt'],
        "channel_plid":response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
        "channel_vc":response['items'][0]['statistics']['viewCount'],
           "channel_sub":response['items'][0]['statistics']['subscriberCount'],
           "channel_tview":response['items'][0]['statistics']['viewCount']
    }
    return data

# %%
channel_data('UCgHmVF2DHE6JI90x0NwESuQ')

# %%
channel_data('UCBi8ZssYZLRNVJRw8JnbHcA')

# %%
channel_data('UCpsAztg-D_oTAeyqWPbV4Yg')

# %%
channel_data('UCqtvt4VFJcE3Q9VbcK9BqQA')

# %%
channel_data('UC3yMSdKWJoaE7xqiRY8eJgQ')


# %%
channel_data('UCB8-hkVDaGM0rMZewIIKG5Q')

# %%
channel_data('UCqNH56x9g4QYVpzmWTzqVYg')

# %%
channel_data('UCWFcHQ1T207uOu4RucvauhA')

# %%
channel_data('UCCq1xDJMBRF61kiOgU90_kw')

# %%
channel_data('UC7ZEIf22kp0AEpvx3OLiX-g')

# %%
#to get the video id
def get_channel_videos(channel_id):
    video_ids = []
    # get Uploads playlist id
    res = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None
    
    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id, 
                                           part='snippet', 
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        
        for i in range(len(res['items'])):
            video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = res.get('nextPageToken')
        
        if next_page_token is None:
            break
    return video_ids

# %%
get_channel_videos('UC7ZEIf22kp0AEpvx3OLiX-g')

# %%
# FUNCTION TO GET VIDEO DETAILS
def get_video_details(v_ids):
    video_stats = []
    
    for i in range(0, len(v_ids), 50):
        response = youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=','.join(v_ids[i:i+50])).execute()
        for video in response['items']:
            video_details = dict(Channel_name = video['snippet']['channelTitle'],
                                Channel_id = video['snippet']['channelId'],
                                Video_id = video['id'],
                                Title = video['snippet']['title'],
                                Tags = video['snippet'].get('tags'),
                                Thumbnail = video['snippet']['thumbnails']['default']['url'],
                                Description = video['snippet']['description'],
                                Published_date = video['snippet']['publishedAt'],
                                Duration = video['contentDetails']['duration'],
                                Views = video['statistics']['viewCount'],
                                Likes = video['statistics'].get('likeCount'),
                                Comments = video['statistics'].get('commentCount'),
                                Favorite_count = video['statistics']['favoriteCount'],
                                Definition = video['contentDetails']['definition'],
                                Caption_status = video['contentDetails']['caption']
                               )
            video_stats.append(video_details)
    return video_stats

# %%


# %%
# FUNCTION TO GET COMMENT DETAILS
def get_comments_details(v_id):
    comment_data = []
    try:
        next_page_token = None
        while True:
            response = youtube.commentThreads().list(part="snippet,replies",
                                                    videoId=v_id,
                                                    maxResults=100,
                                                    pageToken=next_page_token).execute()
            for cmt in response['items']:
                data = dict(Comment_id = cmt['id'],
                            Video_id = cmt['snippet']['videoId'],
                            Comment_text = cmt['snippet']['topLevelComment']['snippet']['textDisplay'],
                            Comment_author = cmt['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            Comment_posted_date = cmt['snippet']['topLevelComment']['snippet']['publishedAt'],
                            Like_count = cmt['snippet']['topLevelComment']['snippet']['likeCount'],
                            Reply_count = cmt['snippet']['totalReplyCount']
                           )
                comment_data.append(data)
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return comment_data



