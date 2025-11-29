import sys
from canvas_api import CanvasAPI

def inspect_specific():
    canvas = CanvasAPI()
    if not canvas.test_connection(): return

    # 1. Inspect Syllabus Page
    print("\n--- Inspecting Syllabus ---")
    try:
        page = canvas.get_page('syllabus')
        print(f"Title: {page['title']}")
        body = page.get('body', '')
        print(f"Body length: {len(body)}")
        if "Policies and Procedures" in body:
            print("  FOUND 'Policies and Procedures'")
            idx = body.find("Policies and Procedures")
            print(f"  Context: ...{body[idx-50:idx+100]}...")
        if "Title IX" in body:
             print("  FOUND 'Title IX'")
             idx = body.find("Title IX")
             print(f"  Context: ...{body[idx-50:idx+100]}...")
    except Exception as e:
        print(f"Error fetching Syllabus: {e}")

    # 2. Inspect Supplementary Pages
    print("\n--- Inspecting Supplementary Pages ---")
    for url in ['supplimentary-2', 'supplimentary-3']:
        try:
            page = canvas.get_page(url)
            print(f"Page: {page['title']} ({url})")
            body = page.get('body', '')
            targets = ["Machine Learning (Supplementary Materials).ppt", "Sample Neural Network.py"]
            for t in targets:
                if t in body:
                    print(f"  FOUND {t}")
                    idx = body.find(t)
                    print(f"  Context: ...{body[idx-100:idx+100]}...")
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # 3. Search all pages for "Sample Project Report" and others
    print("\n--- Searching All Pages ---")
    pages = canvas.list_pages()
    targets = [
        "Sample Project Report",
        "Perceptrons",
        "Neural Networks",
        "Ethics of AI"
    ]
    
    for page in pages:
        # Check title
        for t in targets:
            if t in page['title']:
                print(f"Title Match for '{t}': {page['title']} ({page['url']})")
        
        # Check body
        try:
            p_full = canvas.get_page(page['url'])
            body = p_full.get('body', '')
            for t in targets:
                if t in body:
                    print(f"Body Match for '{t}' in {page['title']} ({page['url']})")
                    idx = body.find(t)
                    print(f"  Context: ...{body[idx-50:idx+50]}...")
        except Exception as e:
            pass

if __name__ == "__main__":
    inspect_specific()

