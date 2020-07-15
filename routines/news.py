#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from .abstract import AbstractRoutine, convertToJSON, convertFromJSON
from wilma_connector.wilma_client import WilmaClient
from wilma_connector.fcm_client import FCMClient


class News(AbstractRoutine):
    def __init__(self):
        super().__init__("news")

    def check(self, wilmaserver, wilmasession, push_id, user_id):
        wilma_client = WilmaClient(wilmaserver, wilmasession)
        fcm_client = FCMClient()
        news = wilma_client.getNews()
        if news.is_error():
            return news
        offline_data_pt = self.get_file(push_id, push_id, user_id)
        user_object = {'user_id': user_id.split("_")[0], 'user_type': user_id.split("_")[1], 'server': wilmaserver}
        if offline_data_pt is not None:
            offline_data = convertFromJSON(offline_data_pt)
            for l_obs in news.get_news():
                found = False
                for o_obs in offline_data:
                    if o_obs['Id'] == l_obs['Id']:
                        found = True
                        break
                if not found:
                    push_content = {'type': 'notification', 'data': self.name, 'payload': l_obs}
                    push_content.update(user_object)
                    fcm_client.sendPush(push_id, push_content)
        self.save_file(convertToJSON(news.get_news()), push_id, push_id, user_id)
        return None
