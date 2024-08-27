try:
    import json
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
except ImportError as e:
    input(f"Import Error: {e}")
    quit()
    

def open_links_and_handle_captcha(json_file_path):
    # Load JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract links with 'mal' tag
    mal_links = []
    def find_mal_links(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'mal':
                    if isinstance(value, str) and value.startswith("http"):
                        mal_links.append(value)
                else:
                    find_mal_links(value)
        elif isinstance(obj, list):
            for item in obj:
                find_mal_links(item)

    find_mal_links(data)

    # Set up the browser (Chrome in this example)
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Login 
    login_url = "https://myanimelist.net/login.php"
    driver.get(login_url)
    input("Press Enter Once you have logged in...")
    
    
    # Open each link, handle CAPTCHA, click the button, wait, and close the tab
    for link in mal_links:
        driver.get(link)
        try:
            
            # Check if CAPTCHA button is present
            captcha_button = driver.find_elements(By.CLASS_NAME, 'amzn-captcha-verify-button')
            if captcha_button:
                print(f"CAPTCHA detected on {link}. Please solve it manually."); print(f"CAPTCHA detected on {link}. Please solve it manually."); print(f"CAPTCHA detected on {link}. Please solve it manually.")
                input("Press ENTER to continue...")  # Wait for 15 seconds for manual solving, adjust as needed
            else:
                # Find the target button and click it
                button = driver.find_element(By.CLASS_NAME, 'btn-user-status-add-list')
                if button:
                    button.click()
                    time.sleep(1.5)
                    print(f"Completed {mal_links[link]} out of {len(mal_links-1)}")
                else:
                    print(f"Button not found on {link}. Skipping.")  
        except Exception as e:
            print(f"An error occurred on {link}: {e}")
        finally:
            driver.execute_script("window.close()")

    print("FINISHED!")
    driver.quit()

if __name__ == "__main__":
    json_file_path = 'export.json'  # Replace with your actual JSON file path
    open_links_and_handle_captcha(json_file_path)
