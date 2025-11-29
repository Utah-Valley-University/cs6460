#!/usr/bin/env python3
"""
Check for broken links in the Canvas course by scanning pages and assignments.
Validates internal Canvas links using the API and external links using HTTP requests.
"""

import sys
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from canvas_api import CanvasAPI

class LinkValidator:
    def __init__(self):
        self.canvas = CanvasAPI()
        self.broken_links = []
        self.checked_links = {} # url -> error or None
        self.canvas_domain = urlparse(self.canvas.api_url).netloc

    def check_external_url(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
            
            if response.status_code == 405 or response.status_code == 403:
                response = requests.get(url, headers=headers, timeout=10, stream=True)
                response.close()
            
            if response.status_code >= 400:
                return f"Status {response.status_code}"
        except requests.RequestException as e:
            return str(e)
        return None

    def check_internal_link(self, url):
        """Validate internal Canvas links using the API."""
        parsed = urlparse(url)
        path = parsed.path
        
        # Check if link points to a different course
        course_match = re.search(r'/courses/(\d+)', path)
        if course_match:
            link_course_id = course_match.group(1)
            # Compare as strings to avoid type mismatch issues
            if str(link_course_id) != str(self.canvas.course_id):
                return f"Points to different course (ID: {link_course_id})"
        
        # Extract IDs using regex
        # Patterns:
        # /courses/:course_id/pages/:slug
        # /courses/:course_id/modules/:module_id
        # /courses/:course_id/assignments/:assignment_id
        # /courses/:course_id/files/:file_id
        # /files/:file_id
        
        try:
            if '/pages/' in path:
                match = re.search(r'/pages/([^/]+)', path)
                if match:
                    slug = unquote(match.group(1))
                    try:
                        page = self.canvas.get_page(slug)
                        if not page.get('published', True) and page.get('published') is not None:
                            return "Page not published"
                        return None
                    except Exception:
                        return "Page not found (404)"
            
            elif '/modules/' in path:
                match = re.search(r'/modules/(\d+)', path)
                if match:
                    module_id = match.group(1)
                    try:
                        module = self.canvas.get_module(module_id)
                        if not module.get('published', True) and module.get('published') is not None:
                            return "Module not published"
                        return None
                    except Exception:
                        return "Module not found (404)"

            elif '/assignments/' in path:
                match = re.search(r'/assignments/(\d+)', path)
                if match:
                    assign_id = match.group(1)
                    try:
                        assignment = self.canvas.get_assignment(assign_id)
                        if not assignment.get('published', True) and assignment.get('published') is not None:
                            return "Assignment not published"
                        return None
                    except Exception:
                        return "Assignment not found (404)"

            elif '/files/' in path:
                match = re.search(r'/files/(\d+)', path)
                if match:
                    file_id = match.group(1)
                    try:
                        file_obj = self.canvas.get_file(file_id)
                        if file_obj.get('locked_for_user', False) or file_obj.get('hidden', False) or file_obj.get('locked', False):
                            return "File is locked or hidden"
                        return None
                    except Exception:
                        return "File not found (404)"
            
            # If we can't parse it specifically, warn but don't fail? 
            # Or assume it's a generic page we can't validate easily via API.
            return "Cannot validate internal link via API"
            
        except Exception as e:
            return f"Validation error: {str(e)}"

    def check_url(self, url):
        if url in self.checked_links:
            return self.checked_links[url]

        parsed = urlparse(url)
        
        if parsed.netloc == self.canvas_domain:
            print(f"Checking Internal: {url} ...", end='\r')
            error = self.check_internal_link(url)
        else:
            print(f"Checking External: {url} ...", end='\r')
            error = self.check_external_url(url)
        
        self.checked_links[url] = error
        return error

    def scan_content(self, html_content, source_name, source_url):
        if not html_content:
            return

        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href')
            if href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                continue
            
            full_url = href
            if href.startswith('/'):
                 full_url = f"{self.canvas.api_url}{href}"
            elif not href.startswith(('http://', 'https://')):
                continue

            error = self.check_url(full_url)
            if error:
                # If internal link couldn't be validated, we might want to ignore "Cannot validate..." messages
                # to reduce noise, or show them as warnings.
                if error == "Cannot validate internal link via API":
                    continue # Skip these for now to focus on real errors

                self.broken_links.append({
                    'source': source_name,
                    'source_url': source_url,
                    'link': full_url,
                    'text': link.get_text(strip=True) or '[No Text]',
                    'error': error
                })

    def run(self):
        print(f"Connecting to Canvas ({self.canvas.api_url})...")
        if not self.canvas.test_connection():
            print("Failed to connect to Canvas.")
            return

        course_id = self.canvas.course_id
        print(f"Scanning course {course_id}...")

        # Scan Pages
        print("Fetching Pages...")
        try:
            pages = self.canvas.list_pages()
            print(f"Found {len(pages)} pages.")
            for page in pages:
                page_url = page['url']
                try:
                    full_page = self.canvas.get_page(page_url)
                    self.scan_content(full_page.get('body'), f"Page: {page['title']}", full_page.get('html_url'))
                except Exception as e:
                    print(f"Error processing page {page['title']}: {e}")
        except Exception as e:
            print(f"Error listing pages: {e}")

        # Scan Assignments
        print("\nFetching Assignments...")
        try:
            assignments = self.canvas.list_assignments()
            print(f"Found {len(assignments)} assignments.")
            for assign in assignments:
                self.scan_content(assign.get('description'), f"Assignment: {assign['name']}", assign.get('html_url'))
        except Exception as e:
            print(f"Error listing assignments: {e}")

        # Report
        print("\n" + "="*60)
        print("MISSING RESOURCES / BROKEN LINKS REPORT")
        print("="*60)
        
        try:
            with open("broken_links.md", "w", encoding="utf-8") as f:
                f.write("# Missing Resources / Broken Links Report\n\n")
                
                if not self.broken_links:
                    print("No broken links found.")
                    f.write("No broken links found.\n")
                else:
                    for item in self.broken_links:
                        # Print to console
                        print(f"\nSource: {item['source']}")
                        print(f"Source URL: {item['source_url']}")
                        print(f"Link Text: {item['text']}")
                        print(f"Broken URL: {item['link']}")
                        print(f"Error: {item['error']}")
                        print("-" * 40)
                        
                        # Write to file
                        f.write(f"## Issue in {item['source']}\n")
                        f.write(f"- **Source URL**: [{item['source']}]({item['source_url']})\n")
                        f.write(f"- **Link Text**: {item['text']}\n")
                        f.write(f"- **Broken URL**: {item['link']}\n")
                        f.write(f"- **Error**: {item['error']}\n\n")
            
            print(f"\nReport saved to broken_links.md")

        except Exception as e:
            print(f"Error writing report file: {e}")

if __name__ == "__main__":
    validator = LinkValidator()
    validator.run()
