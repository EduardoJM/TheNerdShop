import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class NotificationsConsumer(WebsocketConsumer):
    def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = 'user_%s' % self.user_id

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = text_data_json['data']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                "type": 'send_notification',
                "data": data
            }
        )

    def send_notification(self, notification_data):
        self.send(text_data=json.dumps(notification_data))
