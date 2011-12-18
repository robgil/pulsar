'''tests the HttpClient in pulsar.net.client.'''
from pulsar.net import HttpClient, HttpClients
from pulsar.utils.test import test

from .http import BIN_HOST

HTTPBIN_URL = 'http://' + BIN_HOST + '/'
HTTPSBIN_URL = 'https://'+ BIN_HOST + '/'

def httpbin(*suffix):
    """Returns url for HTTPBIN resource."""
    return HTTPBIN_URL + '/'.join(suffix)


def httpsbin(*suffix):
    """Returns url for HTTPSBIN resource."""
    return HTTPSBIN_URL + '/'.join(suffix)


class TestStandardHttpClient(test.TestCase):
    client = 1
    
    def setUp(self):
        proxy = self.worker.cfg.http_proxy
        proxy_info = {}
        if proxy:
            proxy_info['http'] = proxy
        self.r = HttpClient(type = self.client, proxy_info = proxy_info)
         
    def test_http_200_get(self):
        r = self.r.get(httpbin())
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.response, 'OK')
        self.assertTrue(r.content)
        self.assertEqual(r.url,httpbin())
        
    def test_http_400_get(self):
        '''Bad request 400'''
        r = self.r.get(httpbin('status', '400'))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.response, 'Bad Request')
        self.assertEqual(r.content,b'')
        self.assertRaises(r.HTTPError, r.raise_for_status)
        
    def test_http_404_get(self):
        '''Not Found 404'''
        r = self.r.get(httpbin('status', '404'))
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.response, 'Not Found')
        self.assertEqual(r.content,b'')
        self.assertRaises(r.HTTPError, r.raise_for_status)
        
        
@test.skipUnless(2 in HttpClients,'httplib2 not installed.')
class TestHttpClient2(TestStandardHttpClient):
    client = 2