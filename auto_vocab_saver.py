from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from google import genai
import random
import time
import re

# Set your Google Gemini API key here
client = genai.Client(api_key="your-api-key-here")

# Set the path to GeckoDriver
gecko_path = "/usr/local/bin/geckodriver"
service = Service(gecko_path)
options = Options()

# Set mobile user-agent for better compatibility
options.set_preference(
    "general.useragent.override",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
)

# Launch the browser
driver = webdriver.Firefox(service=service, options=options)

# Open the HDUHelp vocabulary site
driver.get("https://skl.hduhelp.com/#/english/list")

# Your login credentials
username = "your-student-id"
password = "your-password"

# Mode: "test" for self-practice, "exam" for exam mode
MODE = "test"  # or "exam"

# Maximum wait time for elements to load (in seconds)
WAIT_TIME = 10

# XPaths dictionary to manage different modes
XPATHS = {
    "start_mode": {
        "test": "/html/body/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div[1]/span",
        "exam": "/html/body/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div[2]/span",
    },
    "start_button": {
        "test": "/html/body/div[1]/div/div/div[3]/div/div[2]/div[2]/div/button",
        "exam": "/html/body/div[1]/div/div/div[3]/div/div[2]/div[2]/div/button",
    },
    "exam_start_confirm": "/html/body/div[4]/div[2]/button[2]",
}

# Wait for elements with timeout using WebDriverWait
def wait_and_find_element(by, value, timeout=WAIT_TIME):
    """Wait for the element to appear and return it."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


# Login process
try:
    username_input = wait_and_find_element(By.NAME, "username")
    username_input.send_keys(username)

    password_input = wait_and_find_element(
        By.XPATH, "//input[@type='password' and @placeholder='请输入密码']"
    )
    password_input.send_keys(password)

    login_button = wait_and_find_element(By.CLASS_NAME, "login-button")
    login_button.click()
    print("Login successful!")

except TimeoutException:
    print("Error: Login elements not found!")
    driver.quit()
    exit()

time.sleep(1)

# Select mode: test or exam
try:
    select_mode = wait_and_find_element(By.XPATH, XPATHS["start_mode"][MODE])
    select_mode.click()

    start_button = wait_and_find_element(By.XPATH, XPATHS["start_button"][MODE])
    start_button.click()
    print(f"{MODE.capitalize()} mode selected!")

    # If in exam mode, confirm exam start
    if MODE == "exam":
        try:
            start_exam_button = WebDriverWait(driver, WAIT_TIME).until(
                EC.element_to_be_clickable((By.XPATH, XPATHS["exam_start_confirm"]))
            )
            start_exam_button.click()
            print("Exam mode started successfully!")
        except TimeoutException:
            print("Error: Unable to start exam mode!")
            driver.quit()
            exit()
    time.sleep(1)

except TimeoutException:
    print("Error: Unable to select mode or start the test!")
    driver.quit()
    exit()

index = 0

# Main loop for answering questions
while True:
    try:
        # Get question number
        number_element = wait_and_find_element(
            By.XPATH, "/html/body/div/div/div/div[3]/div/div[2]/div/div[1]/span[1]"
        )
        number_text = number_element.text.strip()
        match = re.search(r"\d+", number_text)
        if match:
            current_number = int(match.group())
            index = current_number
        else:
            print("Unable to recognize question number text, skipping.")

        # Get the question and options
        word_element = wait_and_find_element(
            By.XPATH, "/html/body/div/div/div/div[3]/div/div[2]/div/div[1]/span[2]"
        )
        word_text = word_element.text.strip()

        optionA_element = wait_and_find_element(
            By.XPATH, "/html/body/div/div/div/div[3]/div/div[3]/div/div[1]/div[1]/span"
        )
        optionA_text = optionA_element.text.strip()

        optionB_element = wait_and_find_element(
            By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[3]/div/div[2]/div[1]/span"
        )
        optionB_text = optionB_element.text.strip()

        optionC_element = wait_and_find_element(
            By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[3]/div/div[3]/div[1]/span"
        )
        optionC_text = optionC_element.text.strip()

        optionD_element = wait_and_find_element(
            By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[3]/div/div[4]/div[1]/span"
        )
        optionD_text = optionD_element.text.strip()

        # Prepare the question prompt for Gemini
        prompt = f"""
        请根据以下英语题目选择最正确的选项：
        题目：{word_text}
        A. {optionA_text}
        B. {optionB_text}
        C. {optionC_text}
        D. {optionD_text}
        请告诉我最正确的选项, 只输出选项字母即可（A/B/C/D）。
        """

        # Get the answer from Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite", contents=prompt
        )

        answer = response.text.strip().upper()
        # Click the correct answer
        if answer == "A":
            optionA_element.click()
        elif answer == "B":
            optionB_element.click()
        elif answer == "C":
            optionC_element.click()
        elif answer == "D":
            optionD_element.click()
        else:
            options = [optionA_element, optionB_element, optionC_element, optionD_element]
            random.choice(options).click()

        print(f"Question {index} answered!")
        print(f"Question: {word_text}")
        print(f"Answer: {answer}")

        # Stop after 100 questions or when no more questions are available
        if index >= 100:
            print("Test complete!")
            submit_button = wait_and_find_element(
                By.XPATH, "/html/body/div[1]/div/div/div[2]/div/div/div[3]/span"
            )
            submit_button.click()
            break

        time.sleep(1.5)

    except TimeoutException:
        print(f"Skipping question {index + 1} due to timeout...")
        continue

    except Exception as e:
        print(f"Error occurred on question {index + 1}: {e}")
        break

# Optional: quit driver at the end
# driver.quit()
