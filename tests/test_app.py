from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os
import unittest
from app import app

class ReuniteAITests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'test_secret_key'
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ReuniteAI', response.data)

    def test_login_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)

    def test_404_page(self):
        response = self.app.get('/nonexistent_route')
        self.assertEqual(response.status_code, 404)
        
    def test_signup_route_get(self):
        # Should now render login.html as per our fix
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)

if __name__ == "__main__":
    unittest.main()
