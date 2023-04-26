import json

import os

from pprint import pprint

from datetime import datetime

import requests


import googleapiclient.discovery
import googleapiclient.errors

API_KEY = os.getenv('API_KEY')



class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__title = ''
        self.__video_count = None
        self.__subscribers_count = None
        self.__views_count = None
        self.__url = ''
        self.__description = ''

    def __str__(self):
        """Возвращает название и ссылку на канал"""
        return f"{self.title} ({self.url})"

    def __eq__(self, other):
        """Возвращает проверку на равенство
          каналов по количеству подписчиков"""
        return self.subscriber_count == other.subscriber_count

    def __add__(self, other):
        """Возвращае  сложение
    количества подписчиков на каналах"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """Возвращае  вычитание
    количества подписчиков на каналах"""
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other):
        """Возвращает проверку меньше ли один канал
           другого канала по количеству подписчиков"""
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """Возвращает проверку меньше или равен один канал
              другого канала по количеству подписчиков"""
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        """Возвращает проверку больше ли один канал
         другого канала по количеству подписчиков"""
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """Возвращает проверку больше или равен один канал
             другого канала по количеству подписчиков"""
        return self.subscriber_count >= other.subscriber_count

    @classmethod
    def get_service(cls):
        """Метод возвращающий объект для работы с YouTube API"""
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

        object_API = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=API_KEY)
        return object_API
    def get_info(self):
        """Получает словарь с информацией о канале"""
        id_channel = self.__channel_id

        youtube = self.get_service()
        # создание запроса
        request = youtube.channels().list(
            id=id_channel,
            part="snippet,statistics"
        )
        #получение нужной информации от запроса
        response = request.execute()
        #выводим информацию в виде словаря
        return response

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_info()

        self.printj(channel)

    def to_json(self, path: str):
        """Сохраняет в файл значения атрибутов
                 экземпляра  Channel"""
        #получаем информацию, которую дожны записать
        Channel_dict={}
        Channel_dict['channel_id'] = self.channel_id
        Channel_dict['title'] = self.title
        Channel_dict['videoCount'] = self.video_count
        Channel_dict['subscribers_count'] = self.subscriber_count
        Channel_dict['view_count'] = self.view_count
        Channel_dict['url'] = self.url
        Channel_dict['description'] = self.description
        # записываем информацию в файл
        with open(path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(Channel_dict, indent=2, ensure_ascii=False))


    @property
    def title (self):
        """Получает ифнормацию о названии канала и
                  возвращает это название"""
        temp_direct = self.get_info()
        self.__title = temp_direct['items'][0]['snippet']['title']
        return self.__title

    @property
    def description(self):
        """Получает ифнормацию об описании канала и
                  возвращает это описание"""
        temp_direct = self.get_info()
        self.__description = temp_direct['items'][0]['snippet']['description']
        return self.__description

    @property
    def video_count(self):
        """Возвращает это количество видео на канале"""
        temp_direct = self.get_info()
        self.__video_count = int(temp_direct['items'][0]['statistics']['videoCount'])
        return self.__video_count

    @property
    def url(self):
        """Возвращает URL адресс канала"""
        self.__url = 'https://www.youtube.com/channel/' + self.__channel_id
        return self.__url

    @property
    def subscriber_count(self):
        """Метод получающий инфорамцию о количестве подписчиков,
                и возвращающий количество подписчиков"""
        temp_direct = self.get_info()
        self.__subscribers_count = int(temp_direct['items'][0]['statistics']['subscriberCount'])
        return self.__subscribers_count

    @property
    def view_count(self):
        """Метод получающий инфорамцию о количестве просмотров,
              и возвращающий количество просмотров"""
        temp_direct = self.get_info()
        self.__views_count = int(temp_direct['items'][0]['statistics'][
            'viewCount'])
        return self.__views_count

    @property
    def channel_id(self):
        """Возвращает ID канала на youtube"""
        return self.__channel_id