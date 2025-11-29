import os
import sys
from canvas_api import CanvasAPI

def investigate():
    try:
        canvas = CanvasAPI()
        if not canvas.test_connection():
            print("Failed to connect to Canvas.")
            return
    except Exception as e:
        print(f"Error initializing Canvas API: {e}")
        return

    print("Fetching course info...")
    course = canvas.get_course()
    print(f"Course: {course.get('name')}")
    
    print("Fetching modules and items...")
    modules = canvas.list_modules(include=['items'])
    
    print("Fetching pages...")
    pages = canvas.list_pages()
    
    print("Fetching assignments...")
    assignments = canvas.list_assignments()

    containers = [
        "Watch & Read | Constraint Satisfaction",
        "Sample Project Report",
        "Supplementary Materials Copy",
        "Supplementary Materials",
        "Watch & Read | Perceptrons",
        "Watch & Read | Neural Networks",
        "Watch & Read | Ethics of AI"
    ]
    
    print("\n--- Investigating Containers ---\n")

    # Check Syllabus
    print(f"Checking Syllabus...")
    syllabus_body = course.get('syllabus_body', '')
    if syllabus_body:
        print(f"  Syllabus body length: {len(syllabus_body)}")
        # Check for specific broken links in syllabus
        if "Policies and Procedures" in syllabus_body:
            print("  Found 'Policies and Procedures' in Syllabus.")
        if "Title IX" in syllabus_body:
             print("  Found 'Title IX' in Syllabus.")
    else:
        print("  Syllabus body is empty.")

    # Check Pages for containers
    for page in pages:
        title = page['title']
        if any(c in title for c in containers):
            print(f"FOUND Page: {title} (URL: {page['url']})")
            # Fetch full content
            try:
                full_page = canvas.get_page(page['url'])
                body = full_page.get('body', '')
                print(f"  Body length: {len(body)}")
                print(f"  Body preview: {body[:200]}...")
                # Check for links in this page
                # Dump links if possible or just search for keywords
            except Exception as e:
                print(f"  Error fetching page content: {e}")

    # Check Modules for containers
    for module in modules:
        for item in module.get('items', []):
            title = item['title']
            if any(c in title for c in containers):
                print(f"FOUND Module Item: {title} (Type: {item['type']}, ID: {item['id']})")
                if item['type'] == 'Page':
                     print(f"  Points to Page URL: {item.get('page_url')}")
                elif item['type'] == 'File':
                     print(f"  Points to File URL: {item.get('url')}")
                elif item['type'] == 'ExternalUrl':
                     print(f"  External URL: {item.get('external_url')}")

    # Check Assignments for containers
    for assign in assignments:
        name = assign['name']
        if any(c in name for c in containers):
            print(f"FOUND Assignment: {name} (ID: {assign['id']})")
            desc = assign.get('description', '')
            print(f"  Description length: {len(desc)}")

if __name__ == "__main__":
    investigate()
