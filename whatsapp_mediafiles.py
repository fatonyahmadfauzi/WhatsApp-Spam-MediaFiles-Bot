import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

def send_file_via_whatsapp(driver, file_path, count=None, total=None, bot_prompt='N', upload_delay=3):
    """Send file through WhatsApp Web with current interface"""
    try:
        # Wait for attachment button to be clickable (new WhatsApp interface)
        attachment_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@title="Attach"]'))
        )
        attachment_btn.click()
        time.sleep(1)
        
        # Find the document input (hidden file input)
        document_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//input[@accept="*"]'))
        )
        
        # Send the absolute file path
        abs_path = os.path.abspath(file_path)
        document_input.send_keys(abs_path)
        
        # Wait for upload
        print("🔼 Uploading", end='', flush=True)
        for _ in range(int(upload_delay)):
            print('.', end='', flush=True)
            time.sleep(1)
        print()
        
        # Wait for send button (new WhatsApp interface)
        send_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
        )
        send_btn.click()
        
        return True
    
    except Exception as e:
        print(f"\n❌ Failed to send file: {str(e)[:100]}...")
        return False

def main():
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # For debugging (remove in production)
    # options.add_argument('--auto-open-devtools-for-tabs')
    # options.add_experimental_option("detach", True)

    try:
        # Setup Chrome WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()

        # Open WhatsApp Web
        driver.get('https://web.whatsapp.com/')
        print("\n\nPlease scan the QR code within 60 seconds...")
        
        # Wait for QR code scan (check for side panel)
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Chat list"]'))
            )
            print("✅ QR code scanned successfully")
        except:
            print("❌ QR code not scanned in time")
            driver.quit()
            return

        # Get user input
        name = input('Enter the name of user or group: ')
        file_path = input('Drag file here or type path: ').strip('"\'')
        if not os.path.exists(file_path):
            print("❌ File not found!")
            driver.quit()
            return

        count = int(input('Enter how many times to send the file: '))
        gap = float(input('Interval (in seconds) between sends: '))
        upload_delay = float(input('Upload delay (in seconds): '))
        bot_prompt = input('Add bot prompt? (Y/N): ').strip().upper()

        # Find and click chat with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                user = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, f'//span[@title="{name}"]'))
                )
                user.click()
                print("✅ Chat selected successfully")
                time.sleep(3)  # Wait for chat to load
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"[!] Could not find chat '{name}' after {max_retries} attempts. Error: {e}")
                    driver.quit()
                    return
                print(f"⚠️ Retrying chat selection ({attempt + 1}/{max_retries})...")
                time.sleep(2)

        # Send files with better error handling
        success_count = 0
        for i in range(1, count + 1):
            print(f"\n♻️ Attempt {i}/{count}")
            
            try:
                # Send status message if bot prompt enabled
                if bot_prompt == 'Y':
                    msg_box = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@role="textbox" and @contenteditable="true"]'))
                    )
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    status_msg = f"[{timestamp} | {i}/{count}] "
                    
                    # Clear and send status message
                    msg_box.click()
                    driver.execute_script("arguments[0].innerHTML = '';", msg_box)
                    msg_box.send_keys(status_msg)
                    
                    # Send the status message
                    send_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
                    )
                    send_btn.click()
                    time.sleep(1)
                
                # Send the file
                if send_file_via_whatsapp(driver, file_path, i, count, bot_prompt, upload_delay):
                    success_count += 1
                    print(f"✅ Success (Total: {success_count})")
                else:
                    print("❌ Failed - retrying chat selection")
                    # Try re-selecting chat
                    driver.find_element(By.XPATH, f'//span[@title="{name}"]').click()
                    time.sleep(3)
                
                # Wait between sends if not last iteration
                if i < count:
                    print(f"⏳ Waiting {gap} seconds...")
                    time.sleep(gap)
                    
            except KeyboardInterrupt:
                print("\n⏹️ Stopped by user")
                break
            except Exception as e:
                print(f"⚠️ Unexpected error: {str(e)[:100]}...")
                # Try refreshing the chat
                driver.find_element(By.XPATH, f'//span[@title="{name}"]').click()
                time.sleep(3)

        # Final message if any files were sent
        if bot_prompt == 'Y' and success_count > 0:
            try:
                msg_box = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@role="textbox" and @contenteditable="true"]'))
                )
                msg_box.send_keys(f"✅ Sent {success_count}/{count} files")
                driver.find_element(By.XPATH, '//span[@data-icon="send"]').click()
            except Exception as e:
                print(f"⚠️ Couldn't send final message: {e}")

        print(f"\n📊 Final result: {success_count}/{count} files sent")
        
    finally:
        # Ensure browser closes even if error occurs
        if 'driver' in locals():
            print("Closing browser in 10 seconds...")
            time.sleep(10)
            driver.quit()

if __name__ == "__main__":
    main()