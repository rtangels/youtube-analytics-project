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
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        id_channel = self.channel_id
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=API_KEY)

        request = youtube.channels().list(
            id=id_channel,
            part="snippet"
        )

        response = request.execute()
        for data_key in response:
            print(f"{data_key}: {response[data_key]}")

