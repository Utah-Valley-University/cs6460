#!/usr/bin/env python3
"""
Canvas LMS API Client
Provides methods to interact with Canvas LMS for content generation.
"""

import os
import requests
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CanvasAPI:
    """Client for interacting with Canvas LMS API."""
    
    def __init__(self, api_url: Optional[str] = None, api_token: Optional[str] = None, course_id: Optional[str] = None):
        """
        Initialize Canvas API client.
        
        Args:
            api_url: Canvas instance URL (e.g., https://uvu.instructure.com)
            api_token: Canvas API access token
            course_id: Default course ID to use
        """
        self.api_url = api_url or os.getenv('CANVAS_API_URL', '').rstrip('/')
        self.api_token = api_token or os.getenv('CANVAS_API_TOKEN', '')
        self.course_id = course_id or os.getenv('CANVAS_COURSE_ID', '')
        
        if not self.api_url:
            raise ValueError("Canvas API URL is required. Set CANVAS_API_URL environment variable.")
        if not self.api_token:
            raise ValueError("Canvas API token is required. Set CANVAS_API_TOKEN environment variable.")
        
        self.base_url = f"{self.api_url}/api/v1"
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an API request to Canvas."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Start with default headers
        headers = self.headers.copy()
        
        # For PUT/POST requests with data, use form-encoded format
        # Canvas API expects form-encoded data for updates (assignment[due_at] format)
        if method in ('PUT', 'POST') and 'data' in kwargs:
            # Remove Content-Type header to let requests set it for form-encoded
            if 'Content-Type' in headers and headers['Content-Type'] == 'application/json':
                del headers['Content-Type']
        
        # Merge any headers passed in kwargs
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        
        # Use the merged headers
        kwargs['headers'] = headers
        
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    
    def get_course(self, course_id: Optional[str] = None) -> Dict[str, Any]:
        """Get course information."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        response = self._request('GET', f'/courses/{course_id}')
        return response.json()
    
    def list_pages(self, course_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all pages in a course."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        # Handle pagination
        pages = []
        url = f'/courses/{course_id}/pages'
        params = {'per_page': 100}
        
        while True:
            response = self._request('GET', url, params=params)
            data = response.json()
            pages.extend(data)
            
            if 'next' in response.links:
                url = response.links['next']['url'].replace(self.base_url, '')
                # Clear params as they are included in the next link
                params = {}
            else:
                break
                
        return pages
    
    def get_page(self, page_url: str, course_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a specific page by URL."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        response = self._request('GET', f'/courses/{course_id}/pages/{page_url}')
        return response.json()
    
    def create_page(self, page_url: str, title: str, body: str, 
                   published: bool = True, course_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new page in Canvas.
        
        Args:
            page_url: URL slug for the page (e.g., 'module-1-overview')
            title: Page title
            body: HTML content for the page body
            published: Whether the page should be published
            course_id: Course ID (uses default if not provided)
        """
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        data = {
            'wiki_page[title]': title,
            'wiki_page[body]': body,
            'wiki_page[published]': published
        }
        
        response = self._request('POST', f'/courses/{course_id}/pages', data=data)
        return response.json()
    
    def update_page(self, page_url: str, title: Optional[str] = None, 
                   body: Optional[str] = None, published: Optional[bool] = None,
                   course_id: Optional[str] = None) -> Dict[str, Any]:
        """Update an existing page."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        data = {}
        if title:
            data['wiki_page[title]'] = title
        if body:
            data['wiki_page[body]'] = body
        if published is not None:
            data['wiki_page[published]'] = published
        
        response = self._request('PUT', f'/courses/{course_id}/pages/{page_url}', data=data)
        return response.json()
    
    def upload_file(self, file_path: str, parent_folder_path: str = '', 
                   course_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file to Canvas.
        
        Args:
            file_path: Path to the file to upload
            parent_folder_path: Folder path in Canvas (e.g., 'course files/module01')
            course_id: Course ID (uses default if not provided)
        """
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        # Step 1: Request upload URL
        filename = os.path.basename(file_path)
        params = {
            'name': filename,
            'size': os.path.getsize(file_path),
            'content_type': 'application/pdf' if filename.endswith('.pdf') else 'application/octet-stream',
            'parent_folder_path': parent_folder_path
        }
        
        response = self._request('POST', f'/courses/{course_id}/files', params=params)
        upload_data = response.json()
        
        # Step 2: Upload the file
        with open(file_path, 'rb') as f:
            files = {'file': f}
            upload_response = requests.post(
                upload_data['upload_url'],
                files=files,
                data=upload_data['upload_params']
            )
            upload_response.raise_for_status()
        
        return upload_response.json()
    
    def get_file(self, file_id: int, course_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a specific file information."""
        # File access usually requires just the file ID, but checking in course context is safer if restricted
        # However, /api/v1/files/:id is the standard endpoint
        response = self._request('GET', f'/files/{file_id}')
        return response.json()

    def list_assignment_groups(self, course_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all assignment groups in a course."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        response = self._request('GET', f'/courses/{course_id}/assignment_groups')
        return response.json()
    
    def list_modules(self, course_id: Optional[str] = None, include: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        List all modules in a course.
        
        Args:
            course_id: Course ID
            include: List of additional data to include (e.g., ['items', 'content_details'])
        """
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        # Handle pagination
        modules = []
        url = f'/courses/{course_id}/modules'
        params = {'per_page': 100}
        
        if include:
            params['include[]'] = include
        
        while True:
            response = self._request('GET', url, params=params)
            data = response.json()
            modules.extend(data)
            
            if 'next' in response.links:
                url = response.links['next']['url'].replace(self.base_url, '')
                params = {} # params are in the next url
            else:
                break
                
        return modules

    def get_module(self, module_id: int, course_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a specific module."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        response = self._request('GET', f'/courses/{course_id}/modules/{module_id}')
        return response.json()

    def list_assignments(self, course_id: Optional[str] = None, 
                        include: Optional[List[str]] = None,
                        assignment_group_id: Optional[int] = None,
                        bucket: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all assignments in a course.
        Note: In Canvas, this includes regular assignments, quizzes, and discussions.
        
        Args:
            course_id: Course ID
            include: List of additional data to include (e.g., ['assignment_visibility', 'overrides'])
            assignment_group_id: Filter by assignment group ID
            bucket: Filter by bucket ('past', 'overdue', 'undated', 'ungraded', 'unsubmitted', 'upcoming', 'future')
        """
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        params = {}
        if include:
            params['include[]'] = include
        if assignment_group_id:
            params['assignment_group_id'] = assignment_group_id
        if bucket:
            params['bucket'] = bucket
        
        # Include search_all to get all assignments regardless of state
        # This ensures we get unpublished assignments too
        params['search_all'] = True
        
        # Canvas API may paginate - get all pages
        all_assignments = []
        page = 1
        per_page = 100
        
        while True:
            page_params = params.copy()
            page_params['page'] = page
            page_params['per_page'] = per_page
            
            try:
                response = self._request('GET', f'/courses/{course_id}/assignments', params=page_params)
                assignments = response.json()
            except Exception as e:
                # If pagination fails, try without pagination params
                if page == 1:
                    response = self._request('GET', f'/courses/{course_id}/assignments', params=params)
                    return response.json()
                else:
                    break
            
            if not assignments:
                break
                
            all_assignments.extend(assignments)
            
            # Check if there are more pages (Canvas uses Link header or returns fewer items)
            if len(assignments) < per_page:
                break
                
            page += 1
            
            # Safety limit to prevent infinite loops
            if page > 100:
                break
        
        return all_assignments
    
    def list_quizzes(self, course_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all quizzes in a course."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        response = self._request('GET', f'/courses/{course_id}/quizzes')
        return response.json()
    
    def list_discussions(self, course_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all discussions in a course."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        response = self._request('GET', f'/courses/{course_id}/discussion_topics')
        return response.json()
    
    def update_quiz(self, quiz_id: int, due_at: Optional[str] = None,
                   lock_at: Optional[str] = None, unlock_at: Optional[str] = None,
                   course_id: Optional[str] = None) -> Dict[str, Any]:
        """Update a quiz."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        data = {}
        if due_at is not None:
            data['quiz[due_at]'] = due_at
        if lock_at is not None:
            data['quiz[lock_at]'] = lock_at
        if unlock_at is not None:
            data['quiz[unlock_at]'] = unlock_at
        
        response = self._request('PUT', f'/courses/{course_id}/quizzes/{quiz_id}', data=data)
        return response.json()
    
    def update_discussion(self, topic_id: int, due_at: Optional[str] = None,
                         lock_at: Optional[str] = None, unlock_at: Optional[str] = None,
                         course_id: Optional[str] = None) -> Dict[str, Any]:
        """Update a discussion topic."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        data = {}
        if due_at is not None:
            data['assignment[due_at]'] = due_at
        if lock_at is not None:
            data['assignment[lock_at]'] = lock_at
        if unlock_at is not None:
            data['assignment[unlock_at]'] = unlock_at
        
        response = self._request('PUT', f'/courses/{course_id}/discussion_topics/{topic_id}', data=data)
        return response.json()
    
    def get_assignment(self, assignment_id: int, course_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a specific assignment."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        response = self._request('GET', f'/courses/{course_id}/assignments/{assignment_id}')
        return response.json()
    
    def update_assignment(self, assignment_id: int, name: Optional[str] = None,
                         due_at: Optional[str] = None, lock_at: Optional[str] = None,
                         unlock_at: Optional[str] = None, description: Optional[str] = None,
                         points_possible: Optional[float] = None,
                         course_id: Optional[str] = None) -> Dict[str, Any]:
        """Update an existing assignment."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        data = {}
        if name:
            data['assignment[name]'] = name
        if due_at is not None:
            data['assignment[due_at]'] = due_at
        if lock_at is not None:
            data['assignment[lock_at]'] = lock_at
        if unlock_at is not None:
            data['assignment[unlock_at]'] = unlock_at
        if description is not None:
            data['assignment[description]'] = description
        if points_possible is not None:
            data['assignment[points_possible]'] = points_possible
        
        response = self._request('PUT', f'/courses/{course_id}/assignments/{assignment_id}', data=data)
        return response.json()
    
    def create_assignment(self, name: str, submission_types: List[str] = ['online_text_entry'],
                         points_possible: float = 100.0, due_at: Optional[str] = None,
                         description: str = '', course_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new assignment."""
        course_id = course_id or self.course_id
        if not course_id:
            raise ValueError("Course ID is required")
        
        data = {
            'assignment[name]': name,
            'assignment[submission_types][]': submission_types,
            'assignment[points_possible]': points_possible,
            'assignment[description]': description
        }
        
        if due_at:
            data['assignment[due_at]'] = due_at
        
        response = self._request('POST', f'/courses/{course_id}/assignments', data=data)
        return response.json()
    
    def test_connection(self) -> bool:
        """Test the API connection."""
        try:
            if not self.course_id:
                # Try to get user info instead
                response = self._request('GET', '/users/self')
                user = response.json()
                print(f"Connected to Canvas as: {user.get('name', 'Unknown')}")
                return True
            else:
                course = self.get_course()
                print(f"Connected to course: {course.get('name', 'Unknown')}")
                return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False


if __name__ == "__main__":
    # Test the connection
    try:
        canvas = CanvasAPI()
        canvas.test_connection()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nPlease set up your .env file with:")
        print("  CANVAS_API_URL=https://your-school.instructure.com")
        print("  CANVAS_API_TOKEN=your_token_here")
        print("  CANVAS_COURSE_ID=your_course_id")

