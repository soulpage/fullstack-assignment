import unittest
from app import app

class TestRagEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_generate_rag(self):
        rv = self.app.post('/rag/generate', json={'prompt': 'Test prompt'})
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Generated text based on', rv.data)

if __name__ == '__main__':
    unittest.main()
