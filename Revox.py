import base64, random as rnd, threading as thrd
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchWindowException
from selenium.webdriver.common.keys import Keys
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
from fake_useragent import UserAgent
import csv
from time import sleep

a, b = 1200, 1000
c = []

def d(e):
    with open(e, "r") as f:
        g = f.readlines()
    g = [h.strip() for h in g]
    return g

def i(j):
    with open(j, "r") as k:
        l = k.readlines()
    l = [m.strip() for m in l]
    return l

def n(o):
    with open(o, "r") as p:
        q = p.readlines()
    q = [r.strip() for r in q]
    return q

def s(t, u, v):
    if not t:
        print("No drivers to arrange.")
        return
    w, x = t[0].execute_script("return window.screen.availWidth"), t[0].execute_script("return window.screen.availHeight")
    for y, z in enumerate(t):
        try:
            A, B = (y % u) * a, (y // u) * b
            z.set_window_position(A, B)
            z.set_window_size(a, b)
        except NoSuchWindowException:
            print(f"Window for driver {y} is no longer available. Skipping arrangement.")

def C(D, E, F, G):
    global c
    H = None
    try:
        I = UserAgent()
        J = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        K = ChromeOptions()
        K.add_argument(f"user-agent={J}")
        K.add_extension("OKX.crx")
        K.add_argument("--disable-dev-shm-usage")
        K.add_argument("--disable-software-rasterizer")
        K.add_argument('--log-level=3')
        K.add_argument("--disable-gpu")
        K.add_argument("--disable-infobars")
        K.add_argument("--disable-notifications")
        K.add_argument("--disable-background-networking")
        K.add_argument("--disable-breakpad")
        K.add_argument("--disable-renderer-backgrounding")
        K.add_argument("--force-device-scale-factor=0.4")
        K.add_argument("--no-sandbox")
        K.add_experimental_option("excludeSwitches", ["enable-automation"])
        K.add_argument('--disable-blink-features=AutomationControlled')
        
        L, M = E.split('@')[0], E.split('@')[1]
        L, N = L.split(':')
        O, P = M.split(':')
        
        Q = f"http://{L}:{N}@{O}:{P}"
        
        R = SeleniumAuthenticatedProxy(proxy_url=Q)
        R.enrich_chrome_options(K)
        H = wd.Chrome(chrome_options=K)
        c.append(H)
        s(c, 4, a, b)
        S = H.current_window_handle
        
        T, U = 30, 0
        while len(H.window_handles) < 3 and U < T:
            sleep(1)
            U += 1

        if len(H.window_handles) >= 3:
            H.switch_to.window(H.window_handles[-1])
            for V in H.window_handles:
                if V != S:
                    H.switch_to.window(V)
                    H.close()
                    sleep(0.5)
        
        H.switch_to.window(S)
        H.switch_to.window(H.window_handles[0])
        H.get("chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/home.html#initialize/welcome")
        wait(H, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[3]/div/div[2]/button"
        ))).click()
        sleep(0.5)
        wait(H, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div"
        ))).click()
        wait(H, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div[2]/div/div[2]"
        ))).click()
        wait(H, 5).until(EC.presence_of_element_located((
            By.XPATH, f"/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div/form/div[2]/div/textarea"
        ))).send_keys(D)
        W = wait(H, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'okui-btn') and contains(@class, 'btn-lg') and contains(@class, 'btn-fill-highlight') and contains(@class, 'block') and not(contains(@class, 'btn-disabled')) and not(@disabled)]")))

        W.click()
        wait(H, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/button"
        ))).click()
        wait(H, 200).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Set password')]]")))
        wait(H, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[1]/div[2]/div/div/div/div/input"
        ))).send_keys("WibuCryto6996")
        wait(H, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[3]/div[2]/div/div/div/div/input"
        ))).send_keys("WibuCryto6996")
        sleep(0.5)
        wait(H, 5).until(EC.presence_of_element_located((
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/form/div[5]/div/div[2]/div/div/div/button"
        ))).click()
        wait(H, 10).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Set now')]]")))
        print("Import ví thành công")
        H.get(F)
        wait(H, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'View asset analysis after connecting wallet')]]")))
        wait(H, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div[1]/div[2]/div[2]",
                )
            )
        ).click()
        sleep(1)
        script = """
        document.querySelector("body > w3m-modal").shadowRoot
        .querySelector("wui-flex > wui-card > w3m-router").shadowRoot
        .querySelector("div > w3m-connect-view").shadowRoot
        .querySelector("wui-flex > wui-list-wallet:nth-child(3)").click();
        """
        
        H.execute_script(script)
        T, U = 30, 0
        while len(H.window_handles) < 2 and U < T:
            sleep(1)
            U += 1

        if len(H.window_handles) >= 2:
            H.switch_to.window(H.window_handles[-1])
            wait(H, 30).until(EC.presence_of_element_located((By.XPATH, 
            "//*[text()[contains(.,'Connect account')]]")))
            wait(H, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div/div/div/div[5]/div[2]/button[2]",
                    )
                )
            ).click()
            H.close()
        H.switch_to.window(H.window_handles[0])
        T, U = 30, 0
        while len(H.window_handles) < 2 and U < T:
            sleep(1)
            U += 1

        if len(H.window_handles) >= 2:
            H.switch_to.window(H.window_handles[-1])
            wait(H, 30).until(EC.presence_of_element_located((By.XPATH, 
            "//*[text()[contains(.,'Signature request')]]")))
            wait(H, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div/div/div/div/div[5]/div/button[2]",
                    )
                )
            ).click()
        print("Connect ví thành công")
        H.switch_to.window(H.window_handles[0])
        wait(H, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Daily Credit')]]")))
        H.execute_script("window.open('');")
        H.switch_to.window(H.window_handles[-1])
        H.get("chrome-extension://mcohilncbfahbmgdjkbpemcciiolgcge/popup.html#/home")
        wait(H, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'OP_BNB')]]")))
        print("Ví có OP_BNB")
        H.close()
        H.switch_to.window(H.window_handles[0])
        wait(H, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'gas-only')]]")))
        wait(H, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div[1]/div[3]/div/div/div[4]/div[2]/div",
                )
            )
        ).click()
        T, U = 30, 0
        while len(H.window_handles) < 2 and U < T:
            sleep(1)
            U += 1

        if len(H.window_handles) >= 2:
            H.switch_to.window(H.window_handles[-1])
            wait(H, 30).until(EC.presence_of_element_located((By.XPATH, 
            "//*[text()[contains(.,'Contract interaction')]]")))
            wait(H, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div/div/div/div/div[7]/div/button[2]",
                    )
                )
            ).click()
        print("Claim 20 Credit")
        H.switch_to.window(H.window_handles[0])
        wait(H, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'20/20')]]")))
        wait(H, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div",
                )
            )
        ).click()
        wait(H, 200).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Completed')]]")))
        print("Invited Complete")
        H.get("https://lense.revox.ai/lense")
        wait(H, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Net Worth')]]")))
        try:
            initial_button = wait(H, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div > div.content-box > div > div.card.content-card.fb1 > div.fbh.fbjc.button"))
            )
            H.execute_script("arguments[0].click();", initial_button)
        except Exception as e:
            print(f"Error clicking the initial button: {e}")
            H.quit()
            exit(1)

        try:
            wait(H, 100).until(
                EC.presence_of_element_located((By.XPATH, "//*[text()[contains(.,'Hide')]]"))
            )
        except Exception as e:
            print(f"Error waiting for 'Hide' element: {e}")
            H.quit()
            exit(1)

        selectors = [
            "#app > div > div.content-box > div > div.card.content-card.fb1 > div.card-container.expand > div > div:nth-child(3) > div.lock.fbv.fbje.content > div.center.button.f16",
            "#app > div > div.content-box > div > div.card.content-card.fb1 > div.card-container.expand > div > div:nth-child(4) > div.lock.fbv.fbje.content > div.center.button.f16",
            "#app > div > div.content-box > div > div.card.content-card.fb1 > div.card-container.expand > div > div:nth-child(5) > div.lock.fbv.fbje.content > div.center.button.f16",
            "#app > div > div.content-box > div > div.card.content-card.fb1 > div.card-container.expand > div > div:nth-child(6) > div.lock.fbv.fbje.content > div.center.button.f16"
        ]

        for selector in selectors:
            try:
                element = wait(H, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                H.execute_script("arguments[0].click();", element)
            except Exception as e:
                print(f"An error occurred with selector {selector}: {e}")
        sleep(3)
        print("Analyze DONE") 
        H.get("https://lense.revox.ai/reward")
        wait(H, 100).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'TASK LIST')]]")))
        invite = H.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div")
        
        value = invite.text  
        print("Get Ref Link")
        wait(H, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[3]/div[1]/div[3]/div/div",
                )
            )
        ).click()
        wait(H, 30).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'7-day Check-in Bonus')]]")))
        script = 'document.querySelector("#app > div > div.content-box > div > div > div.fbv.oa > div > div:nth-child(3) > div:nth-child(2) > div.modal > div > div.f16 > div").click()'
        H.execute_script(script)
        print("Claim CheckIn Done")
        wait(H, 30).until(EC.presence_of_element_located((By.XPATH, 
        "//*[text()[contains(.,'Analyse 1 Token')]]")))
        wait(H, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[3]/div[2]/div[3]/div",
                )
            )
        ).click()
        sleep(2)
        print("Claim Daily Analyze")
        wait(H, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[4]/div[7]/div[3]/div",
                )
            )
        ).click()
        sleep(2)
        print("Claim Researcher I")
        fieldnames = ['invite', 'privatekeys']
        rows = [{'invite': value, 'privatekeys': D}]
        with open('NEWSuccessDATA.csv', 'a', encoding='UTF8', newline='') as f1:
            writer = csv.DictWriter(f1, fieldnames=fieldnames)
            writer.writerows(rows)
        
        with open("private_keys.txt", "r") as f2:
            lines = f2.readlines()
        with open("private_keys.txt", "w") as f2:
            for line in lines:
                if line.strip() != D:
                    f2.write(line)
            c.remove(H)
            H.close()
            H.quit()
            H = None
    except NoSuchWindowException:
        print("Caught NoSuchWindowException. Skipping operation.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        with open("fail.txt", "a") as f3:
            f3.write(f"{D}\n")
        with open("private_keys.txt", "r") as f4:
            lines = f4.readlines()
        with open("private_keys.txt", "w") as f4:
            for line in lines:
                if line.strip() != D:
                    f4.write(line)
            c.remove(H)
            H.close()
            H.quit()
            H = None
    finally:
        if H:
            c.remove(H)
            H.close()
            H.quit()
            H = None
        G.release()

def X():
    proxy_file = "proxy.txt"
    private_keys_file = "private_keys.txt"
    linkref_file = "linkref.txt"
    
    proxies = d(proxy_file)
    private_keys = i(private_keys_file)
    links = n(linkref_file)
    
    max_concurrent_tasks = int(input("Nhập số luồng: "))
    semaphore = thrd.Semaphore(max_concurrent_tasks)

    for private_key in private_keys:
        proxy = rnd.choice(proxies)
        link_ref = rnd.choice(links)
        semaphore.acquire()
        thrd.Thread(target=C, args=(private_key, proxy, link_ref, semaphore)).start()

if __name__ == '__main__':
    X()
