import math
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# disable webdriver-manager logs
logging.getLogger('WDM').setLevel(logging.NOTSET)
res = ''


@pytest.fixture(scope="class")
def browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


class TestLinks:
    global res
    lessons = ['236905', '236896', '236897', '236898', '236899', '236903', '236904', '236895']
    logged_in = False

    @pytest.fixture(autouse=True)
    def setup_method(self, browser):
        if not TestLinks.logged_in:
            browser.implicitly_wait(25)
            browser.get("https://stepik.org/lesson/236895/step/1")
            # Locate and click the login button
            login_button = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.navbar__auth_login')))
            browser.execute_script("arguments[0].click();", login_button)
            # Wait for the signin window to be visible
            signin_window = WebDriverWait(browser, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.auth-widget')))
            # Find and fill the email input
            email_input = WebDriverWait(signin_window, 20).until(
                EC.presence_of_element_located((By.ID, 'id_login_email')))
            email_input.send_keys('anvar-k_91@mail.ru')
            # Find and fill the password input
            password_input = WebDriverWait(signin_window, 20).until(
                EC.presence_of_element_located((By.ID, 'id_login_password')))
            password_input.send_keys('}nSvqk6kYhy7]N;')
            # Find and click the login button inside the signin window
            login_button = WebDriverWait(signin_window, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'sign-form__btn')))
            browser.execute_script("arguments[0].click();", login_button)
            time.sleep(10)
            TestLinks.logged_in = True

    @pytest.mark.parametrize('lesson', lessons)
    def test_open_link_and_submit_answer(self, browser, lesson):
        link = f"https://stepik.org/lesson/{lesson}/step/1"
        # Open the link in a new tab
        browser.execute_script(f"window.open('{link}', '_blank');")
        # Switch to the newly opened tab
        browser.switch_to.window(browser.window_handles[-1])
        self.ans_tst(browser)

    def ans_tst(self, browser):
        browser.implicitly_wait(15)

        # Send result
        result_form = browser.find_element(By.TAG_NAME, "textarea")

        # Scroll the textarea into view
        browser.execute_script("arguments[0].scrollIntoView(true);", result_form)

        result_form.send_keys(str(math.log(int(time.time() + 2.5))))

        # Wait for the submit button to be clickable
        submit = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'submit-submission')))

        # Click submit
        submit.click()
        time.sleep(15)
        print("here999")
        # Wait for the answer to be visible
        answer = WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'smart-hints__hint')))
        ans_text = answer.text

        with open("output.txt", "a") as output_file:
            output_file.write(f"Key999 : {ans_text}\n")  # Write the value of 'smart-hints__hint' to the file

        print(f"Key99 : {ans_text}")  # Print the value of 'smart-hints__hint'

        # Re-locate the submit button after the page is refreshed
        submit = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'submit-submission')))
        submit.click()

        if ans_text != 'Correct!':
            res += ans_text  # res007 value
        assert ans_text == 'Correct!'


if __name__ == '__main__':
    pytest.main()
    time.sleep(30)  # Adjust the sleep duration before closing the browser
    print("Key88" + res)  # Print the value of 'smart-hints__hint'
