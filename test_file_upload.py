import unittest
from app import app

class TestFileUploadEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_upload_file(self):
        rv = self.app.post('/file', data={'file': 'test.txt'})
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'File uploaded successfully', rv.data)

if __name__ == '__main__':
    unittest.main()
