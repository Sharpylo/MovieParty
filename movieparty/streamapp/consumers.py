from channels.generic.websocket import AsyncWebsocketConsumer
import json


class MovieConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.movie = self.scope['url_route']['kwargs']['pk']
        self.movie_id = str(self.movie)
        await self.accept()

        await self.channel_layer.group_add(
            self.movie_id,
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.movie_id,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'time' in text_data_json:
            current_time = text_data_json['time']
            await self.channel_layer.group_send(
                self.movie_id,
                {
                    'type': 'sync_time',
                    'time': current_time
                }
            )
        elif 'action' in text_data_json:
            action = text_data_json['action']
            await self.channel_layer.group_send(
                self.movie_id,
                {
                    'type': action
                }
            )

    async def play(self, event):
        await self.send(text_data=json.dumps({
            'action': 'play'
        }))

    async def pause(self, event):
        await self.send(text_data=json.dumps({
            'action': 'pause'
        }))

    async def sync_time(self, event):
        time = event['time']
        await self.send(text_data=json.dumps({
            'time': time
        }))
