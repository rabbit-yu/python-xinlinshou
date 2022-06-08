import time
from selenium import webdriver
from selenium.webdriver.support import wait
from selenium.webdriver.common.by import By


class SeleniumGetCookies:
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd

        # 配置chrome，绕过检测
        option = webdriver.ChromeOptions()
        # option.binary_location = "./chrome/chrome.exe"
        # option.add_argument('--headless')    # 无头模式
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=option)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                          get: () => undefined
                        })
                      """
        })

        self.driver.maximize_window()
        self.driver.get('https://ppstore.jd.com/login')

    def login(self):
        iframe = self.driver.find_element(By.CSS_SELECTOR, '.A2AhqhRW9FTmOn7kyXl2x')
        self.driver.switch_to.frame(iframe)

        # 输入账号密码登录
        self.driver.find_element(By.CSS_SELECTOR, '#loginname').send_keys(self.user)
        self.driver.find_element(By.CSS_SELECTOR, '#nloginpwd').send_keys(self.pwd)
        self.driver.find_element(By.CSS_SELECTOR, '#paipaiLoginSubmit').click()

    # 检测是否登录成功
    def inspect_login(self):
        # self.driver.switch_to.default_content()
        wait.WebDriverWait(self.driver, 100).until(
            lambda x: x.find_element(By.CSS_SELECTOR, '.menu-item-text'))

    # 加载cookies给requests
    def load_to_requests(self):
        selenium_cookies = self.driver.get_cookies()
        return selenium_cookies

    def run(self):
        self.login()
        self.inspect_login()
        time.sleep(1)
        selenium_cookies = self.load_to_requests()
        self.driver.close()
        self.driver.quit()
        return selenium_cookies
