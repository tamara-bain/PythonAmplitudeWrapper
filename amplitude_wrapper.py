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

    HTTP_URL = "https://api.amplitude.com/2/httpapi"
    IDENTIFY_URL = "https://api.amplitude.com/identify"
    EVENT_DATA_URL = 'https://amplitude.com/api/2/events/segmentation'

    def __init__(self):
        self.api_key = _get_env_variable("AMPLITUDE_API_KEY")
        self.secret_key = _get_env_variable("AMPLITUDE_API_SECRET_KEY")
        self.api_key_data = ("api_key", self.api_key)

    def __send_event(self, event):
        data = {
            "api_key": self.api_key,
            "events": [event]
        }
        try:
            result = requests.post(self.HTTP_URL, data=json.dumps(data), timeout=5)
        except requests.exceptions.ReadTimeout:
            return False
        return result

    def __send_user_properties(self, identification):
        data = []
        data.append(self.api_key_data)
        data.append(('identification', json.dumps([identification])))
        try:
            result = requests.post(self.IDENTIFY_URL, data=data, timeout=5)
        except requests.exceptions.ReadTimeout:
            return False
        return result

    def __build_event(self, user_id=None, event_name=None, device_id=None):
        props = {
            "event_type": event_name,
            'event_properties': {},
            'user_properties': {}
        }

        if device_id is not None:
            props['device_id'] = device_id

        if user_id is not None:
            props['user_id'] = user_id.lower()

        return props

    def __build_user_properties(self, user_id, amplitude_properties=None, properties=None):
        """
        Amplitude properties are amplitude specific user properties like
        'device_id', 'country'
        """

        user_props = {
            "user_id": user_id.lower(),
        }

        if amplitude_properties is not None:
            user_props.update(amplitude_properties)

        if properties is not None:
            user_props["user_properties"] = properties

        return user_props

    def __add_event_properties(self, event, event_properties):
        event['event_properties'] = event_properties

    def __add_user_properties(self, event, user_properties):
        event['user_properties'] = user_properties

    def __add_amplitude_properties(self, event, amplitude_properties):
        event.update(amplitude_properties)

    def identify(self, user_amplitude_id, amplitude_properties=None, user_properties=None):
        data = self.__build_user_properties(user_amplitude_id, amplitude_properties=amplitude_properties, properties=user_properties)
        return self.__send_user_properties(data)

    def send_event(self, user_amplitude_id, event_name, event_properties=None, user_properties=None, amplitude_properties=None):
        event = self.__build_event(event_name=event_name, user_id=user_amplitude_id)

        if event_properties is not None:
            self.__add_event_properties(event, event_properties)

        if user_properties is not None:
            self.__add_user_properties(event, user_properties)

        if amplitude_properties is not None:
            self.__add_amplitude_properties(event, amplitude_properties)

        result = self.__send_event(event)
        return result

    def send_revenue_event(self, user_amplitude_id, event_name, price, quantity, productId, event_properties=None, user_properties=None, amplitude_properties=None):
        event = self.__build_event(event_name=event_name, user_id=user_amplitude_id)

        if event_properties is not None:
            self.__add_event_properties(event, event_properties)

        if user_properties is not None:
            self.__add_user_properties(event, user_properties)

        if amplitude_properties is not None:
            self.__add_amplitude_properties(event, amplitude_properties)

        event['quantity'] = quantity
        event['price'] = price
        event['productId'] = productId

        result = self.__send_event(event)
        return result

    def send_anonymous_event(self, device_id, event_name, event_properties=None):
        event = self.__build_event(device_id=device_id, event_name=event_name)

        if event_properties is not None:
            self.__add_event_properties(event, event_properties)

        result = self.__send_event(event)
        return result

    def set_user_properties(self, user_amplitude_id, user_properties, amplitude_properties=None):
        data = self.__build_user_properties(user_amplitude_id, properties=user_properties, amplitude_properties=amplitude_properties)
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
