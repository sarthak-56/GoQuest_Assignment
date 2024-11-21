import googleapiclient.discovery
from openpyxl import Workbook
from datetime import datetime

API_KEY = 'AIzaSyA_3mI6rZn6TPgUusWwBhLyHfcIu7w-Qog' 


def fetch_channel_data(channel_url):
    # Extract the handle from the channel URL
    handle = channel_url.split('@')[-1]

    # Build the YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    # Fetch channel details by handle
    search_response = youtube.search().list(
        part="snippet",
        q=f"@{handle}",
        type="channel",
        maxResults=1
    ).execute()

    if not search_response.get('items'):
        raise ValueError("Channel not found.")

    channel_id = search_response['items'][0]['snippet']['channelId']

    # Fetch all videos from the channel
    videos = []
    next_page_token = None
    while True:
        video_response = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in video_response.get("items", []):
            if item["id"]["kind"] == "youtube#video":
                video_id = item["id"]["videoId"]
                video_details = youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    id=video_id
                ).execute()

                video_data = video_details["items"][0]
                videos.append({
                    "video_id": video_id,
                    "title": video_data["snippet"]["title"],
                    "description": video_data["snippet"]["description"],
                    "published_date": video_data["snippet"]["publishedAt"],
                    "view_count": video_data["statistics"].get("viewCount", 0),
                    "like_count": video_data["statistics"].get("likeCount", 0),
                    "comment_count": video_data["statistics"].get("commentCount", 0),
                    "duration": video_data["contentDetails"]["duration"],
                    "thumbnail_url": video_data["snippet"]["thumbnails"]["default"]["url"],
                })

        next_page_token = video_response.get("nextPageToken")
        if not next_page_token:
            break

    # Fetch comments for each video
    comments = []
    for video in videos:
        video_id = video["video_id"]
        comment_response = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            maxResults=100
        ).execute()

        for item in comment_response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "video_id": video_id,
                "comment_id": item["id"],
                "text": comment["textDisplay"],
                "author": comment["authorDisplayName"],
                "published_date": comment["publishedAt"],
                "like_count": comment.get("likeCount", 0),
                "reply_to": None
            })

            # Add replies if available
            if "replies" in item:
                for reply in item["replies"]["comments"]:
                    reply_snippet = reply["snippet"]
                    comments.append({
                        "video_id": video_id,
                        "comment_id": reply["id"],
                        "text": reply_snippet["textDisplay"],
                        "author": reply_snippet["authorDisplayName"],
                        "published_date": reply_snippet["publishedAt"],
                        "like_count": reply_snippet.get("likeCount", 0),
                        "reply_to": item["id"]
                    })

    return videos, comments


def save_to_excel(videos, comments, output_file):
    wb = Workbook()

    # Sheet 1: Video Data
    sheet1 = wb.active
    sheet1.title = "Video Data"
    sheet1.append(["Video ID", "Title", "Description", "Published Date", "View Count", "Like Count", "Comment Count", "Duration", "Thumbnail URL"])
    
    for video in videos:
        sheet1.append([
            video["video_id"],
            video["title"],
            video["description"],
            datetime.strptime(video["published_date"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S"),
            video["view_count"],
            video["like_count"],
            video["comment_count"],
            video["duration"],
            video["thumbnail_url"]
        ])

    # Sheet 2: Comments Data
    sheet2 = wb.create_sheet(title="Comments Data")
    sheet2.append(["Video ID", "Comment ID", "Comment Text", "Author Name", "Published Date", "Like Count", "Reply To"])
    
    for comment in comments:
        sheet2.append([
            comment["video_id"],
            comment["comment_id"],
            comment["text"],
            comment["author"],
            datetime.strptime(comment["published_date"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S"),
            comment["like_count"],
            comment["reply_to"]
        ])

    # Save to Excel file
    wb.save(output_file)