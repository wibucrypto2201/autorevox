from selenium import webdriver as uc
from time import sleep
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
from fake_useragent import UserAgent
import random
import csv
from threading import Semaphore, Thread
import psutil
import os

window_width = 1200
window_height = 1000
webs = []

def load_proxies(file_path):
    with open(file_path, "r") as file:
        proxies = file.readlines()
    proxies = [proxy.strip() for proxy in proxies]
    return proxies

def load_private_keys(file_path):
    with open(file_path, "r") as file:
        private_keys = file.readlines()
    private_keys = [key.strip() for key in private_keys]
    return private_keys

def load_links(file_path):
    with open(file_path, "r") as file:
        links = file.readlines()
    links = [link.strip() for link in links]
    return links

def arrange_windows(drivers, items_per_row, window_width, window_height):
    if not drivers:
        print("No drivers to arrange.")
        return
    screen_width = drivers[0].execute_script("return window.screen.availWidth")
    screen_height = drivers[0].execute_script("return window.screen.availHeight")
    for i, driver in enumerate(drivers):
        try:
            x_position = (i % items_per_row) * window_width
            y_position = (i // items_per_row) * window_height
            driver.set_window_position(x_position, y_position)
            driver.set_window_size(window_width, window_height)
        except NoSuchWindowException:
            print(f"Window for driver {i} is no longer available. Skipping arrangement.")

def kill_processes(web_pid):
    try:
        parent = psutil.Process(web_pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
    except psutil.NoSuchProcess:
        pass

def task(private_key, proxy, link_ref, semaphore):
    global webs
    web = None
    try:
        ua = UserAgent()
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        options = ChromeOptions()
        options.add_argument(f"user-agent={user_agent}")
        options.add_extension("OKX.crx")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument('--log-level=3')
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-breakpad")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--force-device-scale-factor=0.4")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Exclude "enable-automation" switch
        options.add_argument('--disable-blink-features=AutomationControlled')  # Disable blink features
        # Parse the proxy string
        username, password_host_port = proxy.split('@')[0], proxy.split('@')[1]
        username, password = username.split(':')
        host, port = password_host_port.split(':')

        proxy_url = f"http://{username}:{password}@{host}:{port}"

        proxy_helper = SeleniumAuthenticatedProxy(proxy_url=proxy_url)
        proxy_helper.enrich_chrome_options(options)
        web = uc.Chrome(chrome_options=options)
        web_pid = web.service.process.pid
        webs.append(web)
        arrange_windows(webs, 4, window_width, window_height)
        current = web.current_window_handle

        # Wait until 3 windows are open
        max_attempts = 30
        attempts = 0
        while len(web.window_handles) < 3 and attempts < max_attempts:
            sleep(1)
            attempts += 1

        if len(web.window_handles) >= 3:
            web.switch_to.window(web.window_handles[-1])
            for handle in web.window_handles:
                if handle != current:
                    web.switch_to.window(handle)
                    web.close()
                    sleep(0.5)

        web.switch_to.window(current)
        web.switch_to.window(web.window_handles[0])
        web.get("chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/home.html#initialize/welcome")
        wait(web, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div[2]/button"
        ))).click()
        sleep(0.5)
        wait(web, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div"
        ))).click()
        wait(web, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div[2]/div/div[2]"
        ))).click()
        wait(web, 5).until(EC.presence_of_element_located((
            By.XPATH, f"/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div/form/div[2]/div/textarea"
        ))).send_keys(private_key)
        button = wait(web, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'okui-btn') and contains(@class, 'btn-lg') and contains(@class, 'btn-fill-highlight') and contains(@class, 'block') and not(contains(@class, 'btn-disabled')) and not(@disabled)]")))

        # Once the button is found and enabled, click it
        button.click()
        wait(web, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/button"
        ))).click()
        wait(web, 200).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Set password')]]")))
        wait(web, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[1]/div[2]/div/div/div/div/input"
        ))).send_keys("WibuCryto6996")
        wait(web, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[3]/div[2]/div/div/div/div/input"
        ))).send_keys("WibuCryto6996")
        sleep(0.5)
        wait(web, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[5]/div/div[2]/div/div/div/button"
        ))).click()
        wait(web, 10).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Set now')]]"))) 
        print("Import ví thành công")
        web.get(link_ref)
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'View asset analysis after connecting wallet')]]"))) 
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div[1]/div[2]/div[2]",
                )
            )
        ).click()
        #OKX
        sleep(1)
        script = """
        document.querySelector("body > w3m-modal").shadowRoot
        .querySelector("wui-flex > wui-card > w3m-router").shadowRoot
        .querySelector("div > w3m-connect-view").shadowRoot
        .querySelector("wui-flex > wui-list-wallet:nth-child(3)").click();
        """

        web.execute_script(script)
        max_attempts = 30
        attempts = 0
        while len(web.window_handles) < 2 and attempts < max_attempts:
            sleep(1)
            attempts += 1

        if len(web.window_handles) >= 2:
            web.switch_to.window(web.window_handles[-1])
            wait(web, 30).until(EC.presence_of_element_located((By.XPATH, 
            "//*[text()[contains(.,'Connect account')]]"))) 
            wait(web, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div/div/div/div[5]/div[2]/button[2]",
                    )
                )
            ).click()
            web.close()
        web.switch_to.window(web.window_handles[0])
        max_attempts = 30
        attempts = 0
        while len(web.window_handles) < 2 and attempts < max_attempts:
            sleep(1)
            attempts += 1

        if len(web.window_handles) >= 2:
            web.switch_to.window(web.window_handles[-1])
            wait(web, 30).until(EC.presence_of_element_located((By.XPATH, 
            "//*[text()[contains(.,'Signature request')]]"))) 
            wait(web, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div/div/div/div/div[5]/div/button[2]",
                    )
                )
            ).click()
        print("Connect ví thành công")
        web.switch_to.window(web.window_handles[0])
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Daily Credit')]]"))) 
        web.execute_script("window.open('');")
        web.switch_to.window(web.window_handles[-1])
        web.get("chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/popup.html#/home")
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'OP_BNB')]]"))) 
        print("Ví có OP_BNB")
        web.close()
        web.switch_to.window(web.window_handles[0])
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'gas-only')]]"))) 
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div[1]/div[3]/div/div/div[4]/div[2]/div",
                )
            )
        ).click()
        max_attempts = 30
        attempts = 0
        while len(web.window_handles) < 2 and attempts < max_attempts:
            sleep(1)
            attempts += 1

        if len(web.window_handles) >= 2:
            web.switch_to.window(web.window_handles[-1])
            wait(web, 30).until(EC.presence_of_element_located((By.XPATH, 
            "//*[text()[contains(.,'Contract interaction')]]"))) 
            wait(web, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div/div/div/div.div[7]/div/button[2]",
                    )
                )
            ).click()
        print("Claim 20 Credit")
        web.switch_to.window(web.window_handles[0])
        wait(web, 30).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'7-day Check-in Bonus')]]"))) 
        script = 'document.querySelector("#app > div.modal > div > div.f16 > div").click()'
        web.execute_script(script)
        print("Claim CheckIn Done")
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'20/20')]]"))) 
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div",
                )
            )
        ).click()
        wait(web, 200).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Completed')]]"))) 
        print("Invited Complete")
        web.get("https://lense.revox.ai/lense")
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Net Worth')]]"))) 
        try:
            initial_button = wait(web, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.content-box > div > div.card.content-card.fb1 > div.fbh.fbjc.button"))
            )
            web.execute_script("arguments[0].click();", initial_button)
        except Exception as e:
            print(f"Error clicking the initial button: {e}")
            web.quit()
            kill_processes(web_pid)
            exit(1)

        # Wait until the 'Hide' element is present
        try:
            wait(web, 100).until(
                EC.presence_of_element_located((By.XPATH, "//*[text()[contains(.,'Hide')]]"))
            )
        except Exception as e:
            print(f"Error waiting for 'Hide' element: {e}")
            web.quit()
            kill_processes(web_pid)
            exit(1)

        # Define the selectors
        selectors = [
            "#app > div > div.content-box > div > div.card.content-card.fb1 > div.card-container.expand > div > div:nth-child(3) > div.lock.fbv.fbje.content > div.center.button.f16",
            "#app > div > div.content-box > div > div.card.content-card.fb1 > div.card-container.expand > div > div:nth-child(4) > div.lock.fbv.fbje.content > div.center.button.f16",
            "#app > div > div.content-box > div > div.card.content-card.fb1 > div.card-container.expand > div > div:nth-child(5) > div.lock.fbv.fbje.content > div.center.button.f16",
            "#app > div > div.content-box > div > div.card.content-card.fb1 > div.card-container.expand > div > div:nth-child(6) > div.lock.fbv.fbje.content > div.center.button.f16"
        ]

        # Wait for each element to be clickable and then click them
        for selector in selectors:
            try:
                element = wait(web, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                web.execute_script("arguments[0].click();", element)
            except Exception as e:
                print(f"An error occurred with selector {selector}: {e}")
        sleep(3)
        print("Analyze DONE") 
        web.get("https://lense.revox.ai/reward")
        wait(web, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'TASK LIST')]]"))) 
        invite = web.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div")

        # Lấy giá trị của phần tử (có thể là text hoặc thuộc tính)
        value = invite.text  
        print("Get Ref Link")

        wait(web, 30).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Today')]]"))) 
        web.refresh()
        wait(web, 30).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Analyse 1 Token')]]"))) 
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[3]/div[2]/div/div[3]/div",
                )
            )
        ).click()
        sleep(2)
        web.refresh()
        print("Claim Daily Analyze")
        wait(web, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[4]/div[7]/div[3]/div",
                )
            )
        ).click()
        print("Claim Researcher I")
        wait(web, 30).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'300')]]"))) 
        print("DONE")

        fieldnames = ['invite', 'privatekeys']
        rows = [{'invite': value, 'privatekeys': private_key}]
        with open('NEWSuccessDATA.csv', 'a', encoding='UTF8', newline='') as f1:
            writer = csv.DictWriter(f1, fieldnames=fieldnames)
            writer.writerows(rows)
        
        # Remove successful private key from the file
        with open("private_keys.txt", "r") as file:
            lines = file.readlines()
        with open("private_keys.txt", "w") as file:
            for line in lines:
                if line.strip() != private_key:
                    file.write(line)
            webs.remove(web)
            web.close()
            web.quit()
            web = None
    except NoSuchWindowException:
        print("Caught NoSuchWindowException. Skipping operation.")
        # Write the failed private key to fail.txt
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Write the failed private key to fail.txt
        with open("fail.txt", "a") as file:
            file.write(f"{private_key}\n")
        # Handle other exceptions accordingly
        with open("private_keys.txt", "r") as file:
            lines = file.readlines()
        with open("private_keys.txt", "w") as file:
            for line in lines:
                if line.strip() != private_key:
                    file.write(line)
            webs.remove(web)
            web.close()
            web.quit()
            web = None
    finally:
        if web:
            webs.remove(web)
            web.close()
            web.quit()
            web = None
        semaphore.release()
        kill_processes(web_pid)  # Ensure processes are killed after each task

def main():
    proxy_file = "proxy.txt"
    private_keys_file = "private_keys.txt"
    linkref_file = "linkref.txt"
    
    proxies = load_proxies(proxy_file)
    private_keys = load_private_keys(private_keys_file)
    links = load_links(linkref_file)
    
    max_concurrent_tasks = int(input("Nhập số luồng: "))
    semaphore = Semaphore(max_concurrent_tasks)

    for private_key in private_keys:
        proxy = random.choice(proxies)
        link_ref = random.choice(links)
        semaphore.acquire()
        Thread(target=task, args=(private_key, proxy, link_ref, semaphore)).start()

if __name__ == '__main__':
    main()
