import os
import sys
# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
import unittest

class TestImagePaths(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_register_missing_path_normalization(self):
        # Case 1: Absolute path with Windows backslashes
        abs_path = r"C:\Users\pawan\SNPSU\Projects\ReuniteAI\images\temp\test.jpg"
        
        # We need to bypass login redirect for testing
        with self.client.session_transaction() as sess:
            sess['user_email'] = 'test@example.com'
            sess['role'] = 'user'
            
        response = self.client.get(f'/register_missing?image_path={abs_path}')
        self.assertEqual(response.status_code, 200)
        
        # Verify the path is normalized to relative and uses forward slashes in HTML
        content = response.data.decode('utf-8')
        self.assertIn('img src="/images/temp/test.jpg"', content)
        print("SUCCESS: Normalized absolute Windows path to relative URL path.")

    def test_register_missing_relative_already(self):
        # Case 2: Path already relative but maybe with backslashes
        rel_path = r"images\temp\test.jpg"
        
        with self.client.session_transaction() as sess:
            sess['user_email'] = 'test@example.com'
            sess['role'] = 'user'
            
        response = self.client.get(f'/register_missing?image_path={rel_path}')
        self.assertEqual(response.status_code, 200)
        
        content = response.data.decode('utf-8')
        self.assertIn('img src="/images/temp/test.jpg"', content)
        print("SUCCESS: Normalized relative backslash path to forward slash URL path.")

if __name__ == "__main__":
    unittest.main()
