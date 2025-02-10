from playwright.sync_api import sync_playwright
from PIL import Image
import io
import time
import os

def take_reddit_screenshot(url, output_path='./Assets/reddit_screenshot.png'):
    # Ensure the Assets directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            color_scheme='light'
        )
        
        page = context.new_page()
        
        try:
            page.goto(url, timeout=60000)  # Increased timeout to 60 seconds
            time.sleep(2)  # Give the page a moment to load
            
            try:
                page.click('button:has-text("Accept all cookies")', timeout=5000)
            except:
                pass
            
            # Wait for the main post element first
            post_selector = 'shreddit-post'
            page.wait_for_selector(post_selector, timeout=30000)  # Increased timeout to 30 seconds
            
            # Now look for our specific elements within the post
            post = page.query_selector(post_selector)
            if not post:
                raise Exception("Could not find the post element")

            # Take screenshots of each section, with more flexible selectors
            credit_bar = post.query_selector('[slot="credit-bar"], [data-testid="post-container"] header')
            title = post.query_selector('[slot="title"], h1, [data-testid="post-title"]')
            post_container = post.query_selector('.shreddit-post-container, [data-testid="post-container"] footer')

            if not all([credit_bar, title, post_container]):
                raise Exception("Could not find all required post elements")

            # Convert screenshots to PIL Images
            credit_bytes = credit_bar.screenshot()
            title_bytes = title.screenshot()
            container_bytes = post_container.screenshot()

            credit_img = Image.open(io.BytesIO(credit_bytes))
            title_img = Image.open(io.BytesIO(title_bytes))
            container_img = Image.open(io.BytesIO(container_bytes))

            # Calculate total height needed
            total_height = credit_img.height + title_img.height + container_img.height
            max_width = max(credit_img.width, title_img.width, container_img.width)

            # Create new image with combined height
            combined_img = Image.new('RGB', (max_width, total_height), 'white')

            # Paste images one below another
            y_offset = 0
            for img in [credit_img, title_img, container_img]:
                combined_img.paste(img, (0, y_offset))
                y_offset += img.height

            # Save combined image
            combined_img.save(output_path)
            browser.close()
            return output_path
            
        except Exception as e:
            print(f"Screenshot Error: {str(e)}")
            if 'browser' in locals():
                browser.close()
            return None  # Return None explicitly on error
        
        finally:
            if 'browser' in locals():
                browser.close()
