#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from .abstract import AbstractRoutine, convertToJSON, convertFromJSON, filterItemsByDate
from wilma_connector.wilma_client import WilmaClient
from wilma_connector.fcm_client import FCMClient

OBS_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"

class Observations(AbstractRoutine):
    def __init__(self):
        super().__init__("observations")

    def check(self, wilmaserver, wilmasession, push_id, user_id):
        wilma_client = WilmaClient(wilmaserver, wilmasession)
        fcm_client = FCMClient()
        obs = wilma_client.get_observations()
        if obs.is_error():
            return obs

        # Filter observations to exclude false-positive notifications
        filteredObs = filterItemsByDate(obs.get_observations(), "TimeStamp", OBS_TIMESTAMP_FORMAT)

        offline_data_pt = self.get_file(push_id, push_id, user_id)
        user_object = {'user_id': user_id.split("_")[0], 'user_type': user_id.split("_")[1], 'server': wilmaserver}
        if offline_data_pt is not None:
            offline_data = filterItemsByDate(convertFromJSON(offline_data_pt), "TimeStamp", OBS_TIMESTAMP_FORMAT)
            for l_obs in filteredObs:
                found = False
                for o_obs in offline_data:
                    if o_obs['Id'] == l_obs['Id']:
                        found = True
                        break
                if not found:
                    # Including this boolean for Wilma Plus to show "Clarify lesson note" button in the notification
                    l_obs['allowSaveExcuse'] = obs.isExcusesAllowed()
                    push_content = {'type': 'notification', 'data': self.name, 'payload': l_obs}
                    push_content.update(user_object)
                    fcm_client.sendPush(push_id, push_content)
        self.save_file(convertToJSON(filteredObs), push_id, push_id, user_id)
        return None
