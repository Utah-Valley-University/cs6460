import sys
from canvas_api import CanvasAPI

def list_all():
    canvas = CanvasAPI()
    if not canvas.test_connection(): return

    print("\n--- All Pages ---")
    pages = canvas.list_pages()
    for p in pages:
        print(f"Page: {p['title']} (URL: {p['url']})")

    print("\n--- All Modules ---")
    modules = canvas.list_modules(include=['items'])
    for m in modules:
        print(f"Module: {m['name']} (ID: {m['id']})")
        for item in m.get('items', []):
            print(f"  - {item['title']} (Type: {item['type']}, ID: {item['id']})")

if __name__ == "__main__":
    list_all()

