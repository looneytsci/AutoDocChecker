from selenium.webdriver.safari.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class website_data_parser:
    def __init__(self, driver: WebDriver, url: str, waiter_timeout: int):
        self.driver = driver
        self.url = url
        self.web_driver_wait = WebDriverWait(driver, waiter_timeout)

    def find_simple_element_with_xpath(self, name, xpath) -> WebElement:
        try:
            web_element = self.driver.find_element(By.XPATH, xpath)

            print(f'🟢 {name}: Элемент найден с id {web_element.id}')

            return web_element
        except Exception as error:
            print(f'❌ {name}: Элемент не найден.\n❌ XPATH: {xpath}\n❌ Selenium: {error}')

    def wait_and_find_element(self, name, xpath) -> WebElement:
        try:
            web_element = self.web_driver_wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            print(f'🟢 {name}: Элемент найден с id {web_element.id}')
            return web_element
        except Exception as error:
            print(f'❌ {name}: Элемент не найден.\n❌ XPATH: {xpath}\n❌ Selenium: {error}')
    
    def wait_visibility_and_find_element(self, name, xpath) -> WebElement:
        try:
            web_element = self.web_driver_wait.until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            print(f'🟢 {name}: Элемент найден с id {web_element.id}')
            return web_element
        except Exception as error:
            print(f'❌ {name}: Элемент не найден.\n❌ XPATH: {xpath}\n❌ Selenium: {error}')

    def wait_until_clickable_and_click_element(self, name, css_selector):
        try:
            clickable_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )
            self.driver.execute_script("arguments[0].click();", clickable_element)
            print(f'🟢 {name}: Кликабельный элемент найден с id {clickable_element.id} и успешно кликнут')
        except Exception as error:
            print(f'❌ {name}: Элемент не найден или не кликабелен.\n❌ Selenium: {error}')

    def wait_until_clickable_and_click_element_xpath(self, name, xpath):
        try:
            clickable_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.driver.execute_script("arguments[0].click();", clickable_element)
            print(f'🟢 {name}: Кликабельный элемент найден с id {clickable_element.id} и успешно кликнут')
        except Exception as error:
            print(f'❌ {name}: Элемент не найден или не кликабелен.\n❌ Selenium: {error}')
    
    def find_and_switch_to_new_frame(self, xpath):
        try:
            new_iframe = self.web_driver_wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            self.driver.switch_to.frame(new_iframe)

            print('🟢 iframe: Успешно нашли и переключились на новый фрейм.')
        except Exception as error:
            print(f'❌ iframe: Не удалось переключиться на новый фрейм.\n❌ Selenium: {error}')
    
    def execute_script(self, script, element, name):
        try:
            self.driver.execute_script(script, element)
            print(f'🟢 {name}: Успешно выполнили скрипт')
        except Exception as error:
            print(f'❌ {name}: Не удалось выполнить скрипт.\nSelenium: {error}')

    def check_element_presence(self, name, xpath) -> WebElement:
        try:
            elem = self.web_driver_wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            print(f'ℹ️  {name}: Web элемент найден на экране')

            return elem
        except Exception as e:
            print(f'ℹ️  {name}: Web элемент не найден на экране')
            return None

    def default_context(self):
        self.driver.switch_to.default_content()

    def make_screenshot(self, path):
        self.driver.save_screenshot(path)
        print(f'🟢 Сохранили скриншот по пути {path}')

    def open_url(self, url):
        self.driver.get(url)

    def finish_session(self):
        self.driver.quit()