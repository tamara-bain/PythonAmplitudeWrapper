#!/usr/local/bin/python3

import unittest
import requests
from mock import patch
import json

from amplitude_wrapper import AmplitudeWrapper

def get_fake_response():
    response = requests.models.Response()
    response.status_code = 200
    return response

class AmplitudeWrapperTest(unittest.TestCase):

    @patch.object(requests, 'post')
    def test_send_event(self, mock_post):
        mock_post.return_value = get_fake_response()
        wrapper = AmplitudeWrapper()
        result = wrapper.send_event('test@test.com', 'click-button', {'COLOR': 'BLUE'})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(mock_post.call_count, 1)

    @patch.object(requests, 'post')
    def test_send_revenue_event(self, mock_post):
        mock_post.return_value = get_fake_response()
        wrapper = AmplitudeWrapper()
        result = wrapper.send_revenue_event('test@test.com', 'click-button', 10.00, 1, 'test-product', {'COLOR': 'BLUE'})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(mock_post.call_count, 1)

    @patch.object(requests, 'post')
    def test_set_user_properties(self, mock_post):
        mock_post.return_value = get_fake_response()

        wrapper = AmplitudeWrapper()
        result = wrapper.set_user_properties('test@test.com', {'COUNTRY': 'CANADA'})
        self.assertEqual(result.status_code, 200, msg=result.text)
        self.assertEqual(mock_post.call_count, 1)

    @patch.object(requests, 'post')
    def test_identify(self, mock_post):
        mock_post.return_value = get_fake_response()

        wrapper = AmplitudeWrapper()
        result = wrapper.identify('test@test.com', {'country': 'Canada', 'device_id': 'test'}, {'USER_PROP_1': 1})
        self.assertEqual(result.status_code, 200, msg=result.text)
        self.assertEqual(mock_post.call_count, 1)

    @patch.object(requests, 'post')
    def test_sending_same_event_twice_should_send_different_events(self, mock_post):
        mock_post.return_value = get_fake_response()

        wrapper = AmplitudeWrapper()
        result1 = wrapper.send_event('test@test.com', 'click-button', {'COLOR': 'BLUE'})
        result2 = wrapper.send_event('test@test.com', 'load-page', {'COLOR': 'BLUE'})
        self.assertEqual(result1.status_code, 200, msg=result1.text)
        self.assertEqual(result2.status_code, 200, msg=result2.text)
        event_type = json.loads(mock_post.call_args_list[0][1]['data'])['events'][0]['event_type']
        event_type2 = json.loads(mock_post.call_args_list[1][1]['data'])['events'][0]['event_type']
        self.assertNotEqual(event_type, event_type2)

    def test_get_unique_event_count_per_day(self):
        wrapper = AmplitudeWrapper()
        result = wrapper.get_unique_event_count_per_day('button-clicked', 10)


