import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def get_chrome_driver(dataDirName, headless=False):
    """
    Sets up webdriver Chrome instance for searching through emails
    :param dataDirName: Data directory name for Chrome instance
    :param headless: Optional headless option
    :return:
    """
    path_to_dir = f"C:/chromeprofiles/{dataDirName}"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"--user-data-dir={path_to_dir}")

    print(f"INFO: Adding experimental options")
    chrome_options.add_experimental_option('w3c', False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    if headless:
        print("INFO: Running in headless mode")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")

    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps["pageLoadStrategy"] = "none"

    print("INFO: Setting Chrome Options.")
    driver = webdriver.Chrome(options=chrome_options, desired_capabilities=caps)
    driver.set_window_size(1000, 1600)

    return driver


class SelemiumPageNavigetor:
    def __init__(self, driver: Chrome):
        self.driver = driver

    def check_page_state(self, time_out=8):
        state = self.driver.execute_script('return document.readyState')
        print(f"INFO: Document state: {state}")
        while state != 'complete' and time_out > 0:
            time.sleep(1)
            print(f"INFO: Waiting for page load to complete. Time left: {time_out}")
            state = self.driver.execute_script('return document.readyState')
            print(f"INFO:Current document state: {state}")
            time_out = time_out - 1

    def refresh_page(self, time_out=30):
        print(f"\nINFO: Refreshing current page!")
        self.driver.set_page_load_timeout(time_out)
        start = time.time()
        try:
            self.driver.refresh()
            print(f"LOG INFO: Page refreshed successfully")
        except TimeoutException as e:
            print(f"ERROR: Timeout occurred trying to get page on first try. Refreshing page and trying again. DETAILS: {e}")
            try:
                print(f"INFO: Trying page load again")
                self.driver.execute_script("window.stop();")
                self.driver.refresh()
            except TimeoutException:
                try:
                    self.driver.execute_script("window.stop();")
                except Exception as e:
                    print(f"ERROR: Driver error: Details {e}")

        self.check_page_state()
        end = time.time()
        total = end - start
        print(f"PAGE refresh took: {total}\n")

    def get_page_source(self, time_out=30):
        htmlPage = "Null"
        self.check_page_state()

        print(f"\nINFO: Getting HTML Page source. Time out: {time_out}")
        self.driver.set_page_load_timeout(time_out)
        try:
            htmlPage = self.driver.page_source
            print(f"LOG INFO: Page source found")
        except TimeoutException as e:
            print(f"ERROR: Timeout occurred trying to get page source on first try. Refreshing page and trying again. DETAILS: {e}")
            try:
                self.driver.execute_script("window.stop();")
                self.driver.refresh()
                htmlPage = self.driver.page_source
            except TimeoutException:
                print(f"LOG INFO: Retry Limit reached! Will stop page loading now")
                try:
                    self.driver.execute_script("window.stop();")
                except Exception as e:
                    print(f"ERROR: Driver error: Details {e}")

        return htmlPage

    def get_page(self, url: str, time_out=30):
        print(f"\nINFO: {url} Will try to get page for at least {time_out} seconds.")
        self.driver.set_page_load_timeout(time_out)
        start = time.time()

        try:
            self.driver.get(url)
            print(f"\nINFO: {url} loaded successfully")
        except TimeoutException as e:
            print(f"ERROR: Timeout occurred trying to get page on first try. Refreshing page and trying again. DETAILS: {e}")
            try:
                print(f"INFO: Trying page load again")
                self.driver.execute_script("window.stop();")
                self.driver.refresh()
            except TimeoutException:
                try:
                    self.driver.execute_script("window.stop();")
                except Exception as e:
                    print(f"ERROR: Driver error: Details {e}")

        self.check_page_state()

        end = time.time()
        total = end - start
        print(f"PAGE LOAD TOOK: {total}\n")

    def get_current_url(self, time_out=30):
        url = "/"
        self.check_page_state()

        print(f"\nINFO: Will try to get current url for at least {time_out} seconds.")
        self.driver.set_page_load_timeout(time_out)

        try:
            url = self.driver.current_url
            print(f"LOG INFO: Current {url} obtained successfully")
        except TimeoutException as e:
            print(f"ERROR: Timeout occurred trying to get current url on first try. Refreshing page and trying again. DETAILS: {e}")
            try:
                self.driver.execute_script("window.stop();")
                self.driver.refresh()
                url = self.driver.current_url
            except TimeoutException:
                print(f"LOG INFO: Retry Limit reached! Will stop page loading now")
                try:
                    self.driver.execute_script("window.stop();")
                except Exception as e:
                    print(f"ERROR: Driver error: Details {e}")
        return url

    def get_page_title(self, time_out=30):
        title = "about:blank"
        self.check_page_state()

        print(f"\nINFO: Will try to get page title for at least {time_out} seconds.")
        self.driver.set_page_load_timeout(time_out)

        try:
            title = self.driver.title
            print(f"LOG INFO: Page title {title} obtained successfully")
        except TimeoutException as e:
            print(f"ERROR: Timeout occurred trying to get current page title on first try. Refreshing page and trying again. DETAILS: {e}")
            try:
                self.driver.execute_script("window.stop();")
                self.driver.refresh()
                url = self.driver.current_url
            except TimeoutException:
                print(f"LOG INFO: Retry Limit reached! Will stop page loading now")
                try:
                    self.driver.execute_script("window.stop();")
                except Exception as e:
                    print(f"ERROR: Driver error: Details {e}")
        return title

    def switchToIframe(self, xpath, time_delay=3.0, pause_after_action=1):
        try:
            wait = WebDriverWait(self.driver, time_delay)
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))
            print(f"LOG INFO: Switched to iframe at {xpath}")
        except Exception as e:
            # traceback.print_exc()
            print(f"ERROR: Error switching to iframe at {xpath}. Details {e}")
            return False
        time.sleep(pause_after_action)
        return True

    def enter_field_value(self, xpath, value, time_delay=3.0, pause_after_action=1):
        try:
            empty_field = WebDriverWait(self.driver, time_delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            sleepTime = time_delay / 2
            time.sleep(sleepTime)
            empty_field.click()
            empty_field.clear()
            empty_field.send_keys(str(value))
            print(f"INFO: Entered value into field at {xpath}")
        except Exception as e:
            print(f"ERROR: First Exception entering value {e}")
            try:
                empty_field = WebDriverWait(self.driver, time_delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                sleepTime = time_delay / 2
                time.sleep(sleepTime)
                empty_field.send_keys(str(value))
                print(f"INFO: Entered value into field at {xpath}")
            except Exception as e_:
                # traceback.print_exc()
                print(f"ERROR: Error entering value for the element given by xpath {xpath}. Details {e_} ")
                return False
        time.sleep(pause_after_action)
        return True

    def sendReturnKey(self, xpath, time_delay=3.0, pause_after_action=1):
        try:
            empty_field = WebDriverWait(self.driver, time_delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            sleepTime = time_delay / 2
            time.sleep(sleepTime)
            empty_field.send_keys(Keys.ENTER)
            print(f"INFO: ENTER Key sent into field at {xpath}")
        except Exception as e:
            # traceback.print_exc()
            print(f"ERROR: Error entering value for the element given by xpath {xpath}. Details {e}")
            return False

        time.sleep(pause_after_action)
        return True

    def click_element(self, xpath, time_delay=3.0, pause_after_action=1):
        try:
            element = WebDriverWait(self.driver, time_delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            sleepTime = time_delay / 2
            time.sleep(sleepTime)
            element.click()
            print(f"INFO: Element at {xpath}  successfully clicked")
            time.sleep(pause_after_action)
        except Exception as e:
            # traceback.print_exc()
            print(f"ERROR: Error clicking element given by xpath {xpath}. Details {e}")
            return False

        return True

    def find_presence_of_element(self, xpath, time_delay=3.0):
        try:
            element = WebDriverWait(self.driver, time_delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            print(f"INFO: Element {element} at {xpath}  present")
        except Exception as e:
            # traceback.print_exc()
            print(f"ERROR: Error finding element given by xpath {xpath}. Details {e}")
            return False

        return True

    def get_element_text(self, xpath, time_delay=3.0):
        try:
            element = WebDriverWait(self.driver, time_delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            element_text = element.text
            print(f"INFO: Text found for element at  {xpath}")
        except Exception as e:
            # traceback.print_exc()
            print(f"ERROR: Errorgetting text for the element given by xpath {xpath}. Details {e}")
            script = "return document.getElementById('hidden_div').innerHTML"
            element_text = None

        return element_text

    def get_number_of_elements(self, xpath, time_delay=3.0):
        time.sleep(time_delay)
        try:
            elements = self.driver.find_elements_by_xpath(xpath)
            numElements = len(elements)
        except:
            return 0

        return numElements

    def getHtmlElementObjectAsText(self, xpath, time_delay=3.0):
        try:
            elementObject = WebDriverWait(self.driver, time_delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            elementObjectText = elementObject.get_attribute("outerHTML")
            print(f"INFO: Found html element at {elementObject}")
        except:
            return None

        return elementObjectText

    def getElementAttributeAsText(self, xpath, attribute_name: str, time_delay=3.0):
        try:
            elementObject = WebDriverWait(self.driver, time_delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            elementObjectAttributeText = elementObject.get_attribute(attribute_name)
        except Exception as e:
            print(
                f"ERROR: Error getting text for the element given by xpath {xpath} or no attribute with name {attribute_name}. Details {e}")
            return None

        return elementObjectAttributeText

    def check_page_loaded(self, page_load_xpath, max_wait_time=20):
        """
        :param page_load_xpath: Xpath of Element that is present for page to be considered fully loaded
        :return:
        """
        start_time = time.time()
        current_page = self.driver.current_url
        print(f"Waiting for set page to load:")
        # CHECK IF PAGE IS LOADED
        pageLoadComplete = self.find_presence_of_element(page_load_xpath, time_delay=max_wait_time)
        if pageLoadComplete is True:
            print(f"INFO: Page loading complete after {time.time() - start_time} seconds")
        else:
            print("WARNING: Page did not load on first try. Waiting")
            pageLoadComplete = self.find_presence_of_element(page_load_xpath, time_delay=max_wait_time)
            if pageLoadComplete is True:
                print(f"INFO: Page fully loaded after {time.time() - start_time} seconds")
            else:
                print(f"ERROR: Page did not load completely. Total wait time: {time.time() - start_time} seconds")

        return pageLoadComplete

    def switchTomainWindow(self):
        handlesList = self.driver.window_handles
        print(f"Window handles active {handlesList}")
        # CHECK IF CURRENT WINDOW IS NOT FIRST WINDOW HANDLE. IF ITS NOT, CLOSE IT.
        try:
            windowHandle = self.driver.current_window_handle
            print(f"Current window handle: {windowHandle}")
            if windowHandle != self.driver.window_handles[0]:
                self.driver.close()
                print("Current window closed.")
        except:
            self.driver.get('about:blank')
            try:
                windowHandle = self.driver.current_window_handle
                print(f"Current window handle: {windowHandle}")
                if windowHandle != self.driver.window_handles[0]:
                    self.driver.close()
                    print("Current window closed.")
            except:
                print("Error Closing window")

        # SWITCH TO THE FIRST WINDOW HANDLE
        try:
            print("Switching to tab with handle id 0 ")
            self.driver.switch_to.window(self.driver.window_handles[0])
        except:
            print("Tab switch failed or already on main tab.")

    def close_all_tabs_and_switch_to_main(self):
        handlesList = self.driver.window_handles
        print(f"Window handles active {handlesList}")
        for window in handlesList:
            if window != handlesList[0]:
                print(f"INFO: Switching to non main window and closing it.")
                self.driver.switch_to.window(window)
                self.driver.close()
                print("INFO: Current window closed.")

        # SWITCH TO THE FIRST WINDOW HANDLE
        try:
            print("Switching to tab with handle id 0 ")
            self.driver.switch_to.window(self.driver.window_handles[0])
        except:
            print("Tab switch failed or already on main tab.")

    def scroll(self, scroll_count_limit=10):
        SCROLL_PAUSE_TIME = 8
        scroll_count = 0

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True and scroll_count <= scroll_count_limit:
            scroll_count = scroll_count + 1
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            print(f"Scroll # {scroll_count} done!")

    def get_curl_formatted_cookies_from_browser(self):
        """
        Each entry in a browser cookie list is a dict with cookie name, value, domain and keys
        For curl cookies, we need just the name and the value of the cookies
        :return:
        """
        cookies_list = self.driver.get_cookies()
        cookies_dict = {}
        for cookie in cookies_list:
            cookies_dict[cookie['name']] = cookie['value']

        return cookies_dict
