# -*- coding: utf-8 -*-

"""UnitTests for airwaveapiclient."""

import unittest
from httmock import all_requests, response, HTTMock
from airwaveapiclient import AirWaveAPIClient


# pylint: disable=unused-argument
# pylint: disable=too-many-instance-attributes
# pylint: disable=protected-access
class AirWaveAPIClientUnitTests(unittest.TestCase):

    """Class AirWaveAPIClientUnitTests.

    Unit test for airwaveapiclient.

    """

    def setUp(self):
        """Setup."""
        self.username = 'username'
        self.password = 'password'
        self.url = 'https://192.168.1.1'

        self.obj = AirWaveAPIClient(username=self.username,
                                    password=self.password,
                                    url=self.url)

        with HTTMock(AirWaveAPIClientUnitTests.content_login):
            self.res = self.obj.login()

    def tearDown(self):
        """Tear down."""
        self.obj.logout()

    def test_init(self):
        """Test init."""
        self.assertEqual(self.obj.username, self.username)
        self.assertEqual(self.obj.password, self.password)
        self.assertEqual(self.obj.url, self.url)
        self.assertNotEqual(self.obj.session, None)

    def test_api_path(self):
        """Test API path."""
        path = 'ap_list.xml'
        url = self.obj.api_path(path)
        self.assertEqual(url, '%s/%s' % (self.url, path))

    def test_id_params(self):
        """Test ID Params."""
        ap_ids = [1, 2, 3]
        params = self.obj.id_params(ap_ids)
        self.assertEqual(params, 'id=1&id=2&id=3')

    def test_urlencode(self):
        """Test urlencode."""
        params = {'mac': '12:34:56:78:90:AB'}
        res = self.obj.urlencode(params)
        self.assertEqual(res, 'mac=12%3A34%3A56%3A78%3A90%3AAB')

    def test_login(self):
        """Test login."""
        self.assertEqual(self.res.status_code, 200)

    def test_logout(self):
        """Test logout."""
        self.assertEqual(self.obj.logout(), None)

    def test_ap_list(self):
        """Test ap_list."""
        path_ap_list = 'ap_list.xml'

        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            res = self.obj.ap_list()
        self.assertEqual(res.status_code, 200)

        url = '%s/%s' % (self.url, path_ap_list)
        self.assertEqual(res.url, url)

        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            ap_ids = [1, 2, 3]
            res = self.obj.ap_list(ap_ids)
        self.assertEqual(res.status_code, 200)

        params = self.obj.id_params(ap_ids)
        url = '%s/%s?%s' % (self.url, path_ap_list, params)
        self.assertEqual(res.url, url)

    def test_ap_detail(self):
        """Test ap_detail."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            ap_id = 1
            res = self.obj.ap_detail(ap_id)
        self.assertEqual(res.status_code, 200)

        path_ap_detail = 'ap_detail.xml'
        ap_ids = [ap_id]
        params = self.obj.id_params(ap_ids)
        url = '%s/%s?%s' % (self.url, path_ap_detail, params)
        self.assertEqual(res.url, url)

    def test_client_detail(self):
        """Test client detail."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            mac = '12:34:56:78:90:AB'
            params = {'mac': mac}
            params = self.obj.urlencode(params)
            res = self.obj.client_detail(mac)
        self.assertEqual(res.status_code, 200)

        path_client_detail = 'client_detail.xml'
        url = '%s/%s?%s' % (self.url, path_client_detail, params)
        self.assertEqual(res.url, url)

    def test_rogue_detail(self):
        """Test rogue detail."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xml):
            ap_id = 1
            params = {'id': ap_id}
            params = self.obj.urlencode(params)
            res = self.obj.rogue_detail(ap_id)
        self.assertEqual(res.status_code, 200)

        path_rogue_detail = 'rogue_detail.xml'
        url = '%s/%s?%s' % (self.url, path_rogue_detail, params)
        self.assertEqual(res.url, url)

    def test_report_list(self):
        """Test report list."""
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xhtml):
            res = self.obj.report_list()
        self.assertEqual(res.status_code, 200)

        path_report_list = 'nf/reports_list'
        params = {'format': 'xml'}
        params = self.obj.urlencode(params)
        url = '%s/%s?%s' % (self.url, path_report_list, params)
        self.assertEqual(res.url, url)

        reports_search_title = 'Weeky Report'
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xhtml):
            res = self.obj.report_list(reports_search_title)
        self.assertEqual(res.status_code, 200)

        params = {'format': 'xml',
                  'reports_search_title': reports_search_title}
        params = self.obj.urlencode(params)
        url = '%s/%s?%s' % (self.url, path_report_list, params)
        self.assertEqual(res.url, url)

    def test_report_detail(self):
        """Test report detail."""
        report_id = 1
        with HTTMock(AirWaveAPIClientUnitTests.content_api_xhtml):
            res = self.obj.report_detail(report_id)
        self.assertEqual(res.status_code, 200)

        path_report_detail = 'nf/report_detail'
        params = {'format': 'xml', 'id': report_id}
        params = self.obj.urlencode(params)
        url = '%s/%s?%s' % (self.url, path_report_detail, params)
        self.assertEqual(res.url, url)

    def test_graph_url(self):
        """Test graph base method."""
        params = {'id': 1,
                  'start': 3600,
                  'end': 0,
                  'type': 'type_name'}
        graph_url = self.obj._AirWaveAPIClient__graph_url(params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'end=-0s&id=1&start=-3600s&type=type_name')
        self.assertEqual(graph_url, url)

    def test_ap_base_url(self):
        """Test AP base graph url method."""
        type_name = 'type_name'
        params = {'ap_id': 1, 'radio_index': 1, 'start': 3600}
        graph_url = self.obj.ap_base_url(type_name, **params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'end=-0s&id=1&radio_index=1&start=-3600s&type=type_name')
        self.assertEqual(graph_url, url)

    def test_ap_client_count_graph_url(self):
        """Test AP client count graph url method."""
        params = {'ap_id': 1, 'radio_index': 1, 'start': 3600}
        graph_url = self.obj.ap_client_count_graph_url(**params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'end=-0s&id=1&radio_index=1&start=-3600s&type=ap_client_count')
        self.assertEqual(graph_url, url)

    def test_ap_bandwidth_graph_url(self):
        """Test AP bandwidth graph url method."""
        params = {'ap_id': 1, 'radio_index': 1, 'start': 3600}
        graph_url = self.obj.ap_bandwidth_graph_url(**params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'end=-0s&id=1&radio_index=1&start=-3600s&type=ap_bandwidth')
        self.assertEqual(graph_url, url)

    def test_dot11_counters_graph_url(self):
        """Test AP dot11 counters graph url method."""
        params = {'ap_id': 1, 'radio_index': 1, 'start': 3600}
        graph_url = self.obj.dot11_counters_graph_url(**params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'end=-0s&id=1&radio_index=1&start=-3600s&type=dot11_counters')
        self.assertEqual(graph_url, url)

    def test_radio_base_url(self):
        """Test radio base graph url method."""
        type_name = 'type_name'
        params = {'ap_uid': "01:23:45:67:89:AB",
                  'radio_index': 1,
                  'radio_interface': 1,
                  'start': 3600}
        graph_url = self.obj.radio_base_url(type_name, **params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'ap_uid=01%3A23%3A45%3A67%3A89%3AAB&'
               'end=-0s&radio_index=1&radio_interface=1&'
               'start=-3600s&type=type_name')
        self.assertEqual(graph_url, url)

    def test_radio_channel_graph_url(self):
        """Test radio channel graph url method."""
        params = {'ap_uid': "01:23:45:67:89:AB",
                  'radio_index': 1,
                  'radio_interface': 1,
                  'start': 3600}
        graph_url = self.obj.radio_channel_graph_url(**params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'ap_uid=01%3A23%3A45%3A67%3A89%3AAB&'
               'end=-0s&radio_index=1&radio_interface=1&'
               'start=-3600s&type=radio_channel')
        self.assertEqual(graph_url, url)

    def test_radio_noise_graph_url(self):
        """Test radio noise graph url method."""
        params = {'ap_uid': "01:23:45:67:89:AB",
                  'radio_index': 1,
                  'radio_interface': 1,
                  'start': 3600}
        graph_url = self.obj.radio_noise_graph_url(**params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'ap_uid=01%3A23%3A45%3A67%3A89%3AAB&'
               'end=-0s&radio_index=1&radio_interface=1&'
               'start=-3600s&type=radio_noise')
        self.assertEqual(graph_url, url)

    def test_radio_power_graph_url(self):
        """Test radio power graph url method."""
        params = {'ap_uid': "01:23:45:67:89:AB",
                  'radio_index': 1,
                  'radio_interface': 1,
                  'start': 3600}
        graph_url = self.obj.radio_power_graph_url(**params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'ap_uid=01%3A23%3A45%3A67%3A89%3AAB&'
               'end=-0s&radio_index=1&radio_interface=1&'
               'start=-3600s&type=radio_power')
        self.assertEqual(graph_url, url)

    def test_radio_errors_graph_url(self):
        """Test radio errors graph url method."""
        params = {'ap_uid': "01:23:45:67:89:AB",
                  'radio_index': 1,
                  'radio_interface': 1,
                  'start': 3600}
        graph_url = self.obj.radio_errors_graph_url(**params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'ap_uid=01%3A23%3A45%3A67%3A89%3AAB&'
               'end=-0s&radio_index=1&radio_interface=1&'
               'start=-3600s&type=radio_errors')
        self.assertEqual(graph_url, url)

    def test_radio_goodput_graph_url(self):
        """Test radio goodput graph url method."""
        params = {'ap_uid': "01:23:45:67:89:AB",
                  'radio_index': 1,
                  'radio_interface': 1,
                  'start': 3600}
        graph_url = self.obj.radio_goodput_graph_url(**params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'ap_uid=01%3A23%3A45%3A67%3A89%3AAB&'
               'end=-0s&radio_index=1&radio_interface=1&'
               'start=-3600s&type=radio_goodput')
        self.assertEqual(graph_url, url)

    def test_channel_utilization_graph_url(self):
        """Test channel utilization graph url method."""
        params = {'ap_uid': "01:23:45:67:89:AB",
                  'radio_index': 1,
                  'radio_interface': 1,
                  'start': 3600}
        graph_url = self.obj.channel_utilization_graph_url(**params)
        url = ('https://192.168.1.1/nf/rrd_graph?'
               'ap_uid=01%3A23%3A45%3A67%3A89%3AAB&'
               'end=-0s&radio_index=1&radio_interface=1&'
               'start=-3600s&type=channel_utilization')
        self.assertEqual(graph_url, url)

    @staticmethod
    @all_requests
    def content_login(url, request):
        """Test content for login."""
        cookie_key = 'Mercury::Handler::AuthCookieHandler_AMPAuth'
        cookie_val = '01234567890abcdef01234567890abcd'
        headers = {'Set-Cookie': '%s=%s;' % (cookie_key, cookie_val)}
        content = '<html>html content.</html>'
        return response(status_code=200,
                        content=content,
                        headers=headers,
                        request=request)

    @staticmethod
    @all_requests
    def content_api_xml(url, request):
        """Test content for api xml."""
        headers = {'content-type': 'application/xml'}
        content = 'xml string'
        return response(status_code=200,
                        content=content,
                        headers=headers,
                        request=request)

    @staticmethod
    @all_requests
    def content_api_xhtml(url, request):
        """Test content for api xhtml."""
        headers = {'content-type': 'application/xhtml'}
        content = 'xhtml string'
        return response(status_code=200,
                        content=content,
                        headers=headers,
                        request=request)
