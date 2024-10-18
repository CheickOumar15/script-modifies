from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore
import time

class Main:
    def __init__(self):
        self.options = ChromeOptions()
        self.options.add_argument("--headless")  # Mode headless pour Termux
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = Chrome(executable_path=ChromeDriverManager().install(), options=self.options)

        self.xpaths = [
            "/html/body/div[6]/div/div[2]/div/div/div[2]/div/button",  # followers
            # ...
            "/html/body/div[6]/div/div[2]/div/div/div[8]/div/button"  # livestream
        ]
        self.xpathsWithAd = [
            # Liste d'éléments XPath avec publicité
        ]
        # Autres attributs similaires (enter_video_url, timer_text, etc.)
        self.discord = "https://discord.gg/DnwnCrvZv8"
        self.option = 0

    def wait_for_page_to_load(self):
        self.check_if_website_loaded('ua-check', "[+] Page is Ready!", "[-] 001 Error - Cant connect to web service", 10)

    def wait_for_captcha_solve(self):
        print("[~] Waiting For CAPTCHA to solve")
        self.check_if_website_loaded('row', "[+] CAPTCHA solved successfully!\n", "[-] 002 Error - CAPTCHA took too long OR no webservice detected", 100)

    def check_button_status(self, xpath):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            if element.is_enabled():
                return f"{Fore.GREEN}[ONLINE]{Fore.RESET}"
            else:
                return f"{Fore.RED}[OFFLINE]{Fore.RESET}"
        except TimeoutException:
            print("[-] 003 Error - Fatal error while generating list")
            quit()

    def display_button_list(self):
        text = "[~] Decide which bot you want [1 to 8]\n"
        for i in range(7):
            text = text + "[" + str(i+1) + "] " + self.xpathnames[i] + " " + self.check_button_status(self.xpaths[i]) + "\n" 
        text = text + f"[8] Discord {Fore.GREEN}[ONLINE]{Fore.RESET}"
        print(text)

    def click_button(self, number_option):
        try:
            xpath = self.xpaths[number_option - 1]
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            if element.is_enabled():
                element.click()
            else:
                print("[-] 004 Error - Offline OR Number not found")
                quit()
        except TimeoutException:
            print("[-] 005 Error - Offline OR Number not found OR Network error")
            quit()

    def user_input_option(self):
        self.option = int(input())
        if self.option == 8:
            self.driver.get(self.discord)
        else:
            self.click_button(self.option)

    def check_if_website_loaded(self, path, message, error_message, delay):
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, path)))
            print(message)
        except TimeoutException:
            print(error_message)
            quit()

    def get_insert_tiktok_link(self):
        print("[~] Send the Tiktok Link")
        tiktok_link = input()
        try:
            myElem = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, self.enter_video_url[self.option-1])))
            print("\n[+] Loading input Field")
            myElem.send_keys(str(tiktok_link))
        except TimeoutException:
            print("[-] 006 Error - Cant Find Input Field")
            quit()

    def send(self):
        try:
            search_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.search_button[self.option-1])))
            search_button.click()
            send_button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.send_button[self.option-1])))
            send_button.click()
            print("[+] Loaded Everything successfully! Bot is running now.")
        except TimeoutException:
            print("[-] 008 Error - Send Key not Found")
            quit()

    def main(self):
        self.driver.get("https://zefoy.com/")
        print("[~] Bot Loading, please wait!")
        self.wait_for_page_to_load()
        self.wait_for_captcha_solve()
        self.display_button_list()
        self.user_input_option()
        self.get_insert_tiktok_link()
        self.send()
        self.driver.quit()

if __name__ == "__main__":
    main = Main()
    main.main()
