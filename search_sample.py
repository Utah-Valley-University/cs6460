import sys
from canvas_api import CanvasAPI

def search_sample():
    canvas = CanvasAPI()
    if not canvas.test_connection(): return

    print("Searching for 'Sample Project' in all pages...")
    pages = canvas.list_pages()
    for page in pages:
        try:
            p = canvas.get_page(page['url'])
            body = p.get('body', '')
            if "Sample Project" in body or "CO2" in body:
                print(f"FOUND in {page['title']} ({page['url']})")
                # Print context
                if "Sample Project" in body:
                    idx = body.find("Sample Project")
                    print(f"  Context: ...{body[idx-50:idx+100]}...")
                if "CO2" in body:
                    idx = body.find("CO2")
                    print(f"  Context (CO2): ...{body[idx-50:idx+100]}...")
        except:
            pass

if __name__ == "__main__":
    search_sample()

