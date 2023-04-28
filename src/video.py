import json

import os

import googleapiclient.discovery
import googleapiclient.errors

API_KEY = os.getenv('API_KEY')

class Video:

    def __init__(self, id_video):
        """Конструктор класса Video"""

        self.__id_video = id_video
        self.__name_video = '' #название видео
        self.__url_video = ''  # ссылка на видео
        self.__view_count = 0  # кол-во просмотров
        self.__like_count = 0  # кол-во видео

    def __repr__(self):
        """ Возвращает иформацию о классе для отладки"""
        return f"""{self.name_video}  имеет url : {self.url_video}
             просмотров {self.view_count} лайков {self.like_count}"""

    def __str__(self):
        """Возвращает иформацию о классе для пользователя"""
        return self.name_video
    @classmethod
    def get_service (cls):
        """Возвращает объект для работы с youtube"""
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

        object_API = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=API_KEY)
        return object_API


    def get_info(self):
        """Получает информацию о видео"""
        youtube = self.get_service()
        video_response = youtube.videos().list(
            part='snippet,statistics,contentDetails,topicDetails',
            id=self.id_video
            ).execute()
        return video_response

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    @property
    def id_video(self):
        """Возвращает id видео"""
        return self.__id_video

    @property
    def view_count (self):
        """Возвращает это количество просмотров видео"""
        temp_direct = self.get_info()
        self.__view_count = int(
            temp_direct['items'][0]['statistics']['viewCount'])
        return self.__view_count

    @property
    def url_video (self):
        """Возвращает URL адресс видео"""
        self.__url_video = 'www.youtube.com/watch?v=' + self.__id_video
        return self.__url_video

    @property
    def like_count(self):
        """Возвращает кол-во лайков """
        temp_direct = self.get_info()
        self.__like_count = int(
            temp_direct['items'][0]['statistics']['likeCount'])
        return self.__like_count

    @property
    def name_video(self):
        """Получает информацию о названии видео
        возвращает название видео"""
        temp_direct = self.get_info()
        self.__name_video = temp_direct['items'][0]['snippet']['title']
        return self.__name_video

class PLVideo(Video):

    def __init__(self, id_video, id_playlist):
        """Конструктор класса PLVideo"""

        super().__init__(id_video)
        self.__id_playlist = id_playlist

    def __str__(self):
        return self.name_video