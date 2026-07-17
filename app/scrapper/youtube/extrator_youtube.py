from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os
from ..extrator import ExtratorBase
from datetime import datetime

load_dotenv()


class YouTubeExtractor(ExtratorBase):

    def __init__(self):
        api_key = os.getenv("API_KEY_YOUTUBE")
        self.youtube = build(
            "youtube",
            "v3",
            developerKey=api_key
        )

    def iso_to_timestamp(self,date):
        return int(
            datetime.fromisoformat(
                date.replace("Z", "+00:00")
            ).timestamp()
        )
    
    def format_youtube_date(self, date):
        return datetime.strptime(
            date,
            "%d/%m/%Y"
        ).strftime(
            "%Y-%m-%dT00:00:00Z"
        )

    def get_comments(self, video, max_results=5):

        request = self.youtube.commentThreads().list(
            part="snippet",
            videoId=video["external_id"],
            maxResults=max_results,
            textFormat="plainText"
        )

        try:
            response = request.execute()

        except HttpError as e:

            if (
                e.resp.status == 403
                and "commentsDisabled" in str(e)
            ):
                return []

            if (
                e.resp.status == 404
                and "videoNotFound" in str(e)
            ):
                return []

            raise


        posts = []

        for item in response["items"]:

            snippet = item["snippet"]["topLevelComment"]["snippet"]

            posts.append(
                {
                    "external_id": item["snippet"]["topLevelComment"]["id"],
                    "parent_external_id": video["external_id"],
                    "text": snippet["textDisplay"],
                    "url": f"https://www.youtube.com/watch?v={video['external_id']}",
                    "images": [],
                    "videos": [],
                    "E_text": None,
                    "E_images": None,
                    "E_videos": None,
                    "data_post": self.iso_to_timestamp(snippet["publishedAt"]),
                    "created_utc": self.iso_to_timestamp(snippet["publishedAt"]),
                    "user": snippet["authorDisplayName"],
                    "type": "youtube_comment",
                    "channel_id": snippet["authorChannelId"]["value"],
                    "channel_name": snippet["authorDisplayName"]
                }
            )

        return posts
    
    def get_channel_id(self, channel_name):

        request = self.youtube.search().list(
            part="snippet",
            q=channel_name,
            type="channel",
            maxResults=1
        )

        response = request.execute()

        items = response.get("items", [])

        if not items:
            raise ValueError(f"Canal '{channel_name}' não encontrado.")

        return items[0]["snippet"]["channelId"]


    def create_video_post(self, video):

        timestamp = int(
            datetime.fromisoformat(
                video["publishedAt"].replace("Z", "+00:00")
            ).timestamp()
        )

        return {
            "external_id": video["external_id"],
            "parent_external_id": None,
            "text": video["description"],
            "url": f"https://www.youtube.com/watch?v={video['external_id']}",
            "images": [
                video["thumbnail"]
            ],
            "videos": [],
            "E_text": None,
            "E_images": None,
            "E_videos": None,
            "data_post": timestamp,
            "created_utc": timestamp,
            "user": video["channelTitle"],
            "type": "youtube_video",
            "channel_id": video.get("channel_id"),
            "channel_name": video["channelTitle"]
        }


    def extrair_hot(self, max_videos=5, max_comments=5):

        request = self.youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            relevanceLanguage="pt",
            regionCode="BR",
            maxResults=max_videos
        )

        response = request.execute()

        posts = []

        for item in response["items"]:

            video = {
                "external_id": item["id"],
                "description": item["snippet"]["description"],
                "publishedAt": item["snippet"]["publishedAt"],
                "channelTitle": item["snippet"]["channelTitle"],
                "channel_id": item["snippet"]["channelId"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            }


            posts.append(
                self.create_video_post(video)
            )

            posts.extend(
                self.get_comments(video, max_comments)
            )

        return posts



    def extrair_new(
        self,
        query,
        published_after,
        published_before,
        max_videos=5,
        max_comments=5
    ):

        published_after = self.format_youtube_date(
            published_after
        )

        published_before = self.format_youtube_date(
            published_before
        )
        request = self.youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            order="date",
            publishedAfter=published_after,
            publishedBefore=published_before,
            maxResults=max_videos,
            relevanceLanguage="pt",
            regionCode="BR"
        )

        response = request.execute()

        posts = []

        for item in response["items"]:

            video = {
                "external_id": item["id"]["videoId"],
                "description": item["snippet"]["description"],
                "publishedAt": item["snippet"]["publishedAt"],
                "channelTitle": item["snippet"]["channelTitle"],
                "channel_id": item["snippet"]["channelId"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            }


            posts.append(
                self.create_video_post(video)
            )

            posts.extend(
                self.get_comments(video, max_comments)
            )

        return posts



    def extrair_canal(self, nome_canal, max_videos=5, max_comments=5):

        channel_id = self.get_channel_id(nome_canal)

        request = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            type="video",
            order="date",
            maxResults=max_videos
        )

        response = request.execute()

        posts = []

        for item in response["items"]:

            video = {
                "external_id": item["id"]["videoId"],
                "description": item["snippet"]["description"],
                "publishedAt": item["snippet"]["publishedAt"],
                "channelTitle": item["snippet"]["channelTitle"],
                "channel_id": item["snippet"]["channelId"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
            }


            posts.append(
                self.create_video_post(video)
            )

            posts.extend(
                self.get_comments(video, max_comments)
            )

        return posts