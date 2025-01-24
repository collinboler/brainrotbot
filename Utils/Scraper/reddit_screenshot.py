from playwright.sync_api import sync_playwright

def take_reddit_screenshot(url, output_path='./Assets/reddit_screenshot.png'):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) #to see the browser window, set headless=False
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            color_scheme='light'
        )
        
        page = context.new_page()
        
        try:
            page.goto(url, timeout=60000)
            try:
                page.click('button:has-text("Accept all cookies")', timeout=5000) #accepting cookies if exists
            except:
                pass
            
            #selecting the content of the post, have the modify this if want to select the comments
            post_selector = 'shreddit-post'
            page.wait_for_selector(post_selector)

            post_element = page.query_selector(post_selector)
            post_element.screenshot(path=output_path) #taking a screenshot of the post

            # Close the browser
            browser.close()
            return output_path
            
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            browser.close()
