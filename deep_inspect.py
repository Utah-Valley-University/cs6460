import sys
import re
from canvas_api import CanvasAPI

def deep_inspect():
    canvas = CanvasAPI()
    if not canvas.test_connection(): return

    print("\n--- Syllabus Links ---")
    p = canvas.get_page('syllabus')
    body = p.get('body', '')
    # Extract hrefs for Policies and Title IX
    for m in re.finditer(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"[^>]*>(.*?)</a>', body, re.IGNORECASE | re.DOTALL):
        href = m.group(1)
        text = m.group(2)
        if "Policies and Procedures" in text or "Title IX" in text:
            print(f"Text: {text.strip()}\nURL: {href}\n")

    print("\n--- Supplementary Pages ---")
    for url in ['supplimentary-2', 'supplimentary-3']:
        try:
            p = canvas.get_page(url)
            print(f"Page: {p['title']} ({url})")
            print("Body:")
            print(p.get('body', ''))
            print("-" * 20)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    deep_inspect()

