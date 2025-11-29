import sys
from canvas_api import CanvasAPI

def inspect():
    try:
        canvas = CanvasAPI()
        if not canvas.test_connection():
            return
    except Exception as e:
        print(f"Error: {e}")
        return

    print("Fetching all pages...")
    pages = canvas.list_pages()
    print(f"Total pages found: {len(pages)}")
    
    targets = [
        "gc190ae4cad9e2b291fb3a44d35dc2bda",
        "CO2_Emission_Forecasting_for_Living_Standards_in_Smart_Cities.pdf",
        "Multi-layer_Perceptron_based_Photovoltaic_Forecasting_for_Rooftop_PV_Applications_in_Smart_Grid.pdf",
        "Machine Learning (Supplementary Materials).ppt",
        "Sample Neural Network.py",
        "Policies and Procedures",
        "Title IX",
        "L16 Perceptrons.pptx",
        "L17 Neural Networks I.pptx",
        "L18 Neural Networks II.pptx",
        "Ethics of AI.pptx"
    ]

    # Specific pages to inspect fully if found
    target_page_titles = [
        "Sample Project Report",
        "Supplementary Materials Copy",
        "Supplementary Materials",
        "Week 12: Watch & Read | Perceptrons",
        "Week 13: Watch & Read | Neural Networks",
        "Week 14: Watch & Read | Ethics of AI"
    ]

    found_pages = {}

    for page in pages:
        title = page['title']
        # Check if this is a target page
        for t in target_page_titles:
            if t in title:
                found_pages[title] = page['url']
        
        # Fetch body to search for targets
        # Note: fetching all bodies might be slow, but necessary
        # Optimization: Only fetch if title matches or we are searching
    
    print("\n--- Target Pages Found ---")
    for title, url in found_pages.items():
        print(f"Found: {title} -> {url}")
        
        try:
            p = canvas.get_page(url)
            body = p.get('body', '')
            print(f"  Scanning content of {title}...")
            
            for target in targets:
                if target in body:
                    print(f"    MATCH: {target}")
                    # Print context
                    idx = body.find(target)
                    start = max(0, idx - 100)
                    end = min(len(body), idx + len(target) + 100)
                    print(f"    Context: ...{body[start:end]}...")
                    
                    # If it's a file link, look for the href
                    # Extract href manually if needed
            print("-" * 20)
        except Exception as e:
            print(f"  Error fetching {title}: {e}")

if __name__ == "__main__":
    inspect()
