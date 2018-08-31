import requests
import json
import os
from datetime import datetime, timedelta

__all__ = ['AmplitudeWrapper']

def _get_env_variable(var_name):
    """
    Get the secret variable or return explicit exception.
    """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable.".format(var_name)
        raise KeyError(error_msg)

class AmplitudeWrapper:

    HTTP_URL = "https://api.amplitude.com/httpapi"
    IDENTIFY_URL = "https://api.amplitude.com/identify"
    EVENT_DATA_URL = 'https://amplitude.com/api/2/events/segmentation'

    def __init__(self, properties={}):
        self.api_key = _get_env_variable("AMPLITUDE_API_KEY")
        self.secret_key = _get_env_variable("AMPLITUDE_API_SECRET_KEY")
        self.api_key_data = ("api_key", self.api_key)
        self.global_properties = properties

    def __send_event(self, event, post_async=False):
        self.__update_with_global_event_properties(event)
        data = []
        data.append(self.api_key_data)
        data.append(('event', json.dumps([event])))
        result = requests.post(self.HTTP_URL, data=data)
        return result

    def __send_user_properties(self, identification):
        data = []
        data.append(self.api_key_data)
        data.append(('identification', json.dumps([identification])))
        result = requests.post(self.IDENTIFY_URL, data=data)
        return result

    def __build_event(self, user_id, event_name):
        return {
            "user_id": user_id.lower(),
            "event_type": event_name,
            'event_properties': {}
        }

    def __build_user_properties(self, user_id, properties):
        return {
            "user_id": user_id.lower(),
            "user_properties": properties,
        }

    def __add_event_properties(self, event, event_properties):
        event['event_properties'] = event_properties

    def __update_with_global_event_properties(self, event):
            self.global_properties.update(event['event_properties'])
            event['event_properties'] = self.global_properties

    def send_event(self, user_amplitude_id, event_name, event_properties=None):
        event = self.__build_event(user_amplitude_id, event_name)

        if event_properties is not None:
            self.__add_event_properties(event, event_properties)

        result = self.__send_event(event)
        return result

    def set_user_properties(self, user_amplitude_id, user_properties):
        data = self.__build_user_properties(user_amplitude_id, user_properties)
        return self.__send_user_properties(data)

    def get_unique_event_count_per_day(self, event_name, number_of_days, end=None):

        if end is None:
            end = datetime.now() + timedelta(days=1)
        else:
            end = end + timedelta(days=1)

        start = (datetime.now() - timedelta(days=number_of_days - 1)).strftime('%Y%m%d')
        end = end.strftime('%Y%m%d')

        params = (
            ('e', json.dumps({
                "event_type": event_name
            })),
            ('m', 'uniques'),
            ('start', start),
            ('end', end),
        )

        result = requests.get(self.EVENT_DATA_URL, params=params,
                              auth=(self.api_key, self.secret_key))

        try:
            if (len(result.json()['data']['series'])):
                return result.json()['data']['series'][0][:-1]
            return [0 for i in range(number_of_days)]
        except json.decoder.JSONDecodeError:
            return None






