import os
import unittest
import appv03
import pytest

class MyTestCase(unittest.TestCase):

    def setUp(self):
        appv03.app.testing = True
        self.app = appv03.app.test_client()

    def tearDown(self):
		pass
    #sample get with no parameters - testing for text in a HTML page
    #def test_dogview(self):
    #    response = self.app.get('/', follow_redirects=True)
    #    self.assertEqual(response.status_code, 200)
    #    self.assertIn(b'Dell Technologies', response.data)
        
    #Sample get with parameters
    def test_dogview(self):
        parameters = {'DogID': '1234abcd'} # These are Sydney Coordinates :)
        response = self.app.get('/api/v1/dog/view', follow_redirects=True, query_string=parameters)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fido', response.data)

    def test_dogadd(self):
        response = self.app.post('/api/v1/dog/add', data=dict(DogID='1234abcd',DogName='Fido'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SUCCESS', response.data)

    def test_dogdelete(self):
        parameters = {'DogID': '1234abcd'}
        response = self.app.delete('/api/v1/dog/delete', query_string=parameters)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SUCCESS', response.data)

    def test_dogupdate(self):
        response = self.app.put('/api/v1/dog/update', data=dict(DogID='1234abcd',DogName='Fido'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SUCCESS', response.data)
