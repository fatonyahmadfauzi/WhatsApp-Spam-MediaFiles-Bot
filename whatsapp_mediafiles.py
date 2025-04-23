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
    """Send file through WhatsApp Web"""
    try:
        # Wait for attachment button
        attachment_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@title="Attach"]'))
        )
        attachment_btn.click()
        time.sleep(1)
        
        # Find file input
        document_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//input[@accept="*"]'))
        )
        
        # Send file path
        document_input.send_keys(os.path.abspath(file_path))
        
        # Upload progress
        print("🔼 Uploading", end='', flush=True)
        for _ in range(int(upload_delay)):
            print('.', end='', flush=True)
            time.sleep(1)
        print()
        
        # Send file
        send_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
        )
        send_btn.click()
        
        return True
    except Exception as e:
        print(f"\n❌ Gagal mengirim {os.path.basename(file_path)}: {str(e)[:100]}...")
        return False

def main():
    # Setup Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()

        # Buka WhatsApp Web
        driver.get('https://web.whatsapp.com/')
        print("\nSilakan scan QR code... (Timeout 60 detik)")
        
        # Tunggu sampai login
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Chat list"]'))
        )

        # Input penerima
        name = input('Nama kontak/grup: ')
        user = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[@title="{name}"]'))
        )
        user.click()
        time.sleep(3)

        # Input file-file
        files = []
        print("\nMasukkan path file (ketik 'selesai' jika sudah):")
        while True:
            file_path = input(f"File {len(files)+1}: ").strip('"\'')
            if file_path.lower() == 'selesai':
                if not files:
                    print("⚠️ Minimal 1 file diperlukan!")
                    continue
                break
            if not os.path.exists(file_path):
                print("❌ File tidak ditemukan!")
                continue
            files.append(file_path)

        # Konfigurasi
        count = int(input('Jumlah pengulangan: '))
        gap = float(input('Interval antar pengiriman (detik): '))
        upload_delay = float(input('Waktu upload (detik): '))
        bot_prompt = input('Tambahkan status bot? (Y/N): ').strip().upper()

        # Proses pengiriman
        success_count = 0
        for i in range(1, count + 1):
            print(f"\n📦 Siklus {i}/{count}")
            
            for file_path in files:
                print(f"\n📄 Mengirim {os.path.basename(file_path)}...")
                
                if bot_prompt == 'Y':
                    msg_box = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@role="textbox"]'))
                    )
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    msg_box.send_keys(f"[{timestamp} | File {files.index(file_path)+1}/{len(files)}] ")
                    driver.find_element(By.XPATH, '//span[@data-icon="send"]').click()
                    time.sleep(1)
                
                if send_file_via_whatsapp(driver, file_path, i, count, bot_prompt, upload_delay):
                    success_count += 1
                
                if file_path != files[-1]:  # Jangan tunggu setelah file terakhir
                    time.sleep(gap)
            
            if i < count:
                print(f"\n⏳ Menunggu {gap} detik...")
                time.sleep(gap)

        # Pesan akhir
        if bot_prompt == 'Y':
            msg_box = driver.find_element(By.XPATH, '//div[@role="textbox"]')
            msg_box.send_keys(f"✅ {success_count}/{len(files)*count} file terkirim")
            driver.find_element(By.XPATH, '//span[@data-icon="send"]').click()

        print(f"\n✅ Selesai! Total file terkirim: {success_count}/{len(files)*count}")
        
    finally:
        print("\nMenutup browser dalam 10 detik...")
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":
    main()