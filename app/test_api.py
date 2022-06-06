"""Test the API."""

import requests

from unittest import TestCase

# Test class for Todo API
class TestTodoApi(TestCase):
    """Test the API."""

    # Define the base URL
    base_url = 'http://127.0.0.1:5000/todo'

    # Test the GET endpoint
    def test_get_todos(self):
        """Test the GET endpoint."""
        # Send a GET request to the base URL
        response = requests.get(self.base_url)
        # Check the status code
        self.assertEqual(response.status_code, 200)
        print("Test the GET endpoint completed")

    # Test the POST endpoint
    def test_add_todo(self):
        """Test the POST endpoint."""
        # Send a POST request to the base URL
        response = requests.post(self.base_url, json={
            'title': 'Test',
            'description': 'Test description'
        })
        # Check the status code
        self.assertEqual(response.status_code, 201)
        # Check the response data
        self.assertEqual(response.json(), {
            'id': response.json()['id'],
            'title': 'Test',
            'description': 'Test description',
            'completed': False,
            'date_created': response.json()['date_created']
        })
        print("Test the Post endpoint completed")
    
    # Test the PUT endpoint
    def test_update_todo(self):
        """Test the PUT endpoint."""
        # Send a POST request to the base URL
        response = requests.post(self.base_url, json={
            'title': 'Test',
            'description': 'Test description'
        })
        # Check the status code
        self.assertEqual(response.status_code, 201)
        # Check the response data
        self.assertEqual(response.json(), {
            'id': response.json()['id'],
            'title': 'Test',
            'description': 'Test description',
            'completed': False,
            'date_created': response.json()['date_created']
        })
        # Send a PUT request to the base URL
        response = requests.put(self.base_url + '/' + str(response.json()['id']) , json={
            'title': 'Test',
            'description': 'Test description',
            'completed': True
        })
        # Check the status code
        self.assertEqual(response.status_code, 200)
        # Check the response data
        self.assertEqual(response.json(), {
            'id': response.json()['id'],
            'title': 'Test',
            'description': 'Test description',
            'completed': True,
            'date_created': response.json()['date_created']
        })
        print("Test the PUT endpoint completed")
    
    # Test the DELETE endpoint
    def test_delete_todo(self):
        """Test the DELETE endpoint."""
        # Send a POST request to the base URL
        response = requests.post(self.base_url, json={
            'title': 'Test',
            'description': 'Test description'
        })
        # Check the status code
        self.assertEqual(response.status_code, 201)
        # Check the response data
        self.assertEqual(response.json(), {
            'id': response.json()['id'],
            'title': 'Test',
            'description': 'Test description',
            'completed': False,
            'date_created': response.json()['date_created']
        })
        # Send a DELETE request to the base URL
        response = requests.delete(self.base_url + '/' + str(response.json()['id']))
        # Check the status code
        self.assertEqual(response.status_code, 200)
        # Check the response data
        self.assertEqual(response.json(), {
            'id': response.json()['id'],
            'title': 'Test',
            'description': 'Test description',
            'completed': False,
            'date_created': response.json()['date_created']
        })
        print("Test the DELETE endpoint completed")

    # Test the GET endpoint with a bad ID
    def test_get_todo_bad_id(self):
        """Test the GET endpoint with a bad ID."""
        # Send a GET request to the base URL
        response = requests.get(self.base_url + '/0')
        # Check the status code
        self.assertEqual(response.status_code, 404)
        # Check the response data
        self.assertEqual(response.json(), {'error': 'Not found'})
    

if __name__ == '__main__':
    tester = TestTodoApi()
    tester.test_get_todos()
    tester.test_add_todo()
    tester.test_update_todo()
    tester.test_delete_todo()
    tester.test_get_todo_bad_id()
