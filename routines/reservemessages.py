#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from .abstract import AbstractRoutine, convertToJSON, convertFromJSON
from wilma_connector.wilma_client import WilmaClient
from wilma_connector.fcm_client import FCMClient


def sendMsg(message, user_object, push_id, fcm_client):
    push_content = {'type': 'notification', 'data': "reserve_message", 'payload': message}
    push_content.update(user_object)
    fcm_client.sendPush(push_id, push_content)

def optimizeMessage(msg):
    template = {
        "Id": "",
        "Replies": 0,
        "Status": 0
    }
    if "Id" in msg:
        template["Id"] = msg["Id"]
    if "Replies" in msg:
        template["Replies"] = msg["Replies"]
    if "Status" in msg:
        template["Status"] = msg["Status"]
    return template


class ReserveMessages(AbstractRoutine):
    def __init__(self):
        super().__init__("reservemessages")

    def check(self, wilmaserver, wilmasession, push_id, user_id):
        wilma_client = WilmaClient(wilmaserver, wilmasession)
        fcm_client = FCMClient()
        messages = wilma_client.getMessages()
        if messages.is_error():
            return messages
        optimizedMessages = []
        for msg in messages.get_messages():
            optimizedMessages.append(optimizeMessage(msg))
        offline_data_pt = self.get_file(push_id, push_id, user_id)
        user_object = {'user_id': user_id.split("_")[0], 'user_type': user_id.split("_")[1], 'server': wilmaserver}
        if offline_data_pt is not None:
            offline_data = convertFromJSON(offline_data_pt)
            for l_msg in optimizedMessages:
                found = False
                replyCountChanged = False
                for o_msg in offline_data:
                    if o_msg['Id'] == l_msg['Id']:
                        found = True
                        if "Status" in l_msg and l_msg['Status'] == 1:
                            if "Replies" in l_msg and ((not "Replies" in o_msg and "Replies" in l_msg) or l_msg['Replies'] > o_msg['Replies']):
                                replyCountChanged = True
                                break
                if not found:
                    sendMsg(l_msg, user_object, push_id, fcm_client)
                elif replyCountChanged:
                    sendMsg(l_msg, user_object, push_id, fcm_client)

        self.save_file(convertToJSON(optimizedMessages), push_id, push_id, user_id)
        return None
