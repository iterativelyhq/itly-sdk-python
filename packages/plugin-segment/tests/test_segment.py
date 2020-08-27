import time
import unittest
from datetime import datetime, timedelta

from itly.plugin_segment import SegmentPlugin, SegmentOptions
from itly.plugin_segment._segment_client import Request
from itly.sdk import PluginOptions, Environment, Properties, Event


class TestSegment(unittest.TestCase):
    def test_segment(self):
        requests = []
        options = SegmentOptions(
            flush_at=3,
            flush_interval=1000,
            send_request=lambda request: requests.append(request)
        )
        p = SegmentPlugin('My-Key', options)
        assert p.id() == 'segment'
        try:
            p.load(PluginOptions(environment=Environment.DEVELOPMENT))

            now = datetime(year=2020, month=8, day=27, hour=16, minute=41, second=25)

            p.identify("user-1", Properties(item1='value1', item2=2), timestamp=now)

            time.sleep(0.1)
            assert requests == []
            p.alias("user-1", "prev-user-1", timestamp=now)

            time.sleep(0.1)
            assert requests == [
            ]

            p.track("user-2", Event('event-1', Properties(item1='value1', item2=1)), timestamp=now)
            time.sleep(0.1)

            self._clean_requests(requests)
            assert requests == [
                Request(data=[
                    {'integrations': {}, 'anonymousId': None, 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'type': 'identify',
                     'userId': 'user-1', 'traits': {'item1': 'value1', 'item2': 2}},
                    {'integrations': {}, 'previousId': 'prev-user-1', 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}},
                     'userId': 'user-1', 'type': 'alias', 'anonymousId': None},
                    {'integrations': {}, 'anonymousId': None, 'properties': {'item1': 'value1', 'item2': 1}, 'timestamp': '2020-08-27T16:41:25+00:00',
                     'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'userId': 'user-2', 'type': 'track', 'event': 'event-1'}]),
            ]

            p.group("user-2", "group-2", Properties(item1='value2', item2=2), timestamp=now + timedelta(seconds=3))
            time.sleep(0.1)

            self._clean_requests(requests)
            assert requests == [
                Request(data=[
                    {'integrations': {}, 'anonymousId': None, 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'type': 'identify',
                     'userId': 'user-1', 'traits': {'item1': 'value1', 'item2': 2}},
                    {'integrations': {}, 'previousId': 'prev-user-1', 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}},
                     'userId': 'user-1', 'type': 'alias', 'anonymousId': None},
                    {'integrations': {}, 'anonymousId': None, 'properties': {'item1': 'value1', 'item2': 1}, 'timestamp': '2020-08-27T16:41:25+00:00',
                     'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'userId': 'user-2', 'type': 'track', 'event': 'event-1'}]),
            ]

            p.flush()
            time.sleep(0.1)

            self._clean_requests(requests)
            assert requests == [
                Request(data=[
                    {'integrations': {}, 'anonymousId': None, 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'type': 'identify',
                     'userId': 'user-1', 'traits': {'item1': 'value1', 'item2': 2}},
                    {'integrations': {}, 'previousId': 'prev-user-1', 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}},
                     'userId': 'user-1', 'type': 'alias', 'anonymousId': None},
                    {'integrations': {}, 'anonymousId': None, 'properties': {'item1': 'value1', 'item2': 1}, 'timestamp': '2020-08-27T16:41:25+00:00',
                     'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'userId': 'user-2', 'type': 'track', 'event': 'event-1'}]),
                Request(data=[
                    {'integrations': {}, 'anonymousId': None, 'timestamp': '2020-08-27T16:41:28+00:00', 'groupId': 'group-2', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}},
                     'userId': 'user-2', 'traits': {'item1': 'value2', 'item2': 2}, 'type': 'group'}]),
            ]

            p.flush()
            p.flush()

            time.sleep(0.1)
            self._clean_requests(requests)
            assert requests == [
                Request(data=[
                    {'integrations': {}, 'anonymousId': None, 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'type': 'identify',
                     'userId': 'user-1', 'traits': {'item1': 'value1', 'item2': 2}},
                    {'integrations': {}, 'previousId': 'prev-user-1', 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}},
                     'userId': 'user-1', 'type': 'alias', 'anonymousId': None},
                    {'integrations': {}, 'anonymousId': None, 'properties': {'item1': 'value1', 'item2': 1}, 'timestamp': '2020-08-27T16:41:25+00:00',
                     'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'userId': 'user-2', 'type': 'track', 'event': 'event-1'}]),
                Request(data=[
                    {'integrations': {}, 'anonymousId': None, 'timestamp': '2020-08-27T16:41:28+00:00', 'groupId': 'group-2', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}},
                     'userId': 'user-2', 'traits': {'item1': 'value2', 'item2': 2}, 'type': 'group'}]),
            ]

            p.page("user-2", "category-2", "page-3", Properties(item1='value3', item2=3), timestamp=now + timedelta(seconds=7))

            time.sleep(1.1)
            self._clean_requests(requests)
            assert requests == [
                Request(data=[
                    {'integrations': {}, 'anonymousId': None, 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'type': 'identify',
                     'userId': 'user-1', 'traits': {'item1': 'value1', 'item2': 2}},
                    {'integrations': {}, 'previousId': 'prev-user-1', 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}},
                     'userId': 'user-1', 'type': 'alias', 'anonymousId': None},
                    {'integrations': {}, 'anonymousId': None, 'properties': {'item1': 'value1', 'item2': 1}, 'timestamp': '2020-08-27T16:41:25+00:00',
                     'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'userId': 'user-2', 'type': 'track', 'event': 'event-1'}]),
                Request(data=[
                    {'integrations': {}, 'anonymousId': None, 'timestamp': '2020-08-27T16:41:28+00:00', 'groupId': 'group-2', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}},
                     'userId': 'user-2', 'traits': {'item1': 'value2', 'item2': 2}, 'type': 'group'}]),
                Request(data=[{'integrations': {}, 'anonymousId': None, 'properties': {'item1': 'value3', 'item2': 3}, 'timestamp': '2020-08-27T16:41:32+00:00', 'category': 'category-2',
                               'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'userId': 'user-2', 'type': 'page', 'name': 'page-3'}]),
            ]

            p.track("user-2", Event('event-4', Properties(item1='value4', item2=4)), timestamp=now + timedelta(seconds=10))
            p.track("user-1", Event('event-5', Properties(item1='value5', item2=5)), timestamp=now + timedelta(seconds=12))
        finally:
            p.shutdown()

            time.sleep(0.1)
            self._clean_requests(requests)
            assert requests == [
                Request(data=[
                    {'integrations': {}, 'anonymousId': None, 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'type': 'identify',
                     'userId': 'user-1', 'traits': {'item1': 'value1', 'item2': 2}},
                    {'integrations': {}, 'previousId': 'prev-user-1', 'timestamp': '2020-08-27T16:41:25+00:00', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}},
                     'userId': 'user-1', 'type': 'alias', 'anonymousId': None},
                    {'integrations': {}, 'anonymousId': None, 'properties': {'item1': 'value1', 'item2': 1}, 'timestamp': '2020-08-27T16:41:25+00:00',
                     'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'userId': 'user-2', 'type': 'track', 'event': 'event-1'}]),
                Request(data=[
                    {'integrations': {}, 'anonymousId': None, 'timestamp': '2020-08-27T16:41:28+00:00', 'groupId': 'group-2', 'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}},
                     'userId': 'user-2', 'traits': {'item1': 'value2', 'item2': 2}, 'type': 'group'}]),
                Request(data=[{'integrations': {}, 'anonymousId': None, 'properties': {'item1': 'value3', 'item2': 3}, 'timestamp': '2020-08-27T16:41:32+00:00', 'category': 'category-2',
                               'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'userId': 'user-2', 'type': 'page', 'name': 'page-3'}]),
                Request(data=[{'integrations': {}, 'anonymousId': None, 'properties': {'item1': 'value4', 'item2': 4}, 'timestamp': '2020-08-27T16:41:35+00:00',
                               'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'userId': 'user-2', 'type': 'track', 'event': 'event-4'},
                              {'integrations': {}, 'anonymousId': None, 'properties': {'item1': 'value5', 'item2': 5}, 'timestamp': '2020-08-27T16:41:37+00:00',
                               'context': {'library': {'name': 'analytics-python', 'version': '1.2.9'}}, 'userId': 'user-1', 'type': 'track', 'event': 'event-5'}]),
            ]

    @staticmethod
    def _clean_requests(requests):
        for rr in requests:
            for r in rr:
                for request in rr.data:
                    if 'messageId' in request:
                        del request['messageId']
