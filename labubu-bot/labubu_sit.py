from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, date
from zoneinfo import ZoneInfo
import time

from datetime import timedelta
TARGET_TIME_EST = datetime.now(tz=ZoneInfo("US/Eastern"))
today = date.today()
# TARGET_TIME_EST = datetime(today.year, today.month, today.day, 10, 0, 0, tzinfo=ZoneInfo("US/Eastern"))

# 🧠 使用你复制出来的 Chrome 登录配置
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=/Users/tongtongzhao/popmart-profile")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# 🚀 启动浏览器
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 🎯 直接进入购物车页面
cart_url = "https://www.popmart.com/us/largeShoppingCart"
driver.get(cart_url)

# ⏳ 等待时间
print(f"等待抢购时间（美东）：{TARGET_TIME_EST}")
while True:
    now = datetime.now(tz=ZoneInfo("US/Eastern"))
    if now >= TARGET_TIME_EST:
        break
    print(f"当前美东时间：{now.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(0.1)

# 🛒 只负责全选并结账
try:
    while True:
        driver.refresh()
        wait = WebDriverWait(driver, 10)

        # 先勾选“Select all”复选框（用JS点击，避免被遮挡）
        select_all_checkbox = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                '//div[contains(@class, "index_selectText") and contains(text(), "Select all")]/preceding-sibling::div[contains(@class, "index_checkbox__")]'
            ))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_all_checkbox)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", select_all_checkbox)
        print("✅ 已勾选全选框")

        # 再点击结账按钮
        checkout_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.index_checkout__V9YPC'))
        )
        checkout_button.click()
        print("🚀 跳转结账页")

        # 只点击一次“PROCEED TO PAY”，避免被风控
        try:
            proceed_to_pay_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.index_placeOrderBtn__wgYr6'))
            )
            time.sleep(0.5)  # 模拟用户反应
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proceed_to_pay_button)
            driver.execute_script("arguments[0].click();", proceed_to_pay_button)
            print("💳 已点击 PROCEED TO PAY")
        except Exception as e:
            print("⚠️ PROCEED TO PAY按钮不可用，请手动检查页面或刷新后再试！")

        input("请手动完成支付，完成后按回车退出...")
        break

except Exception as e:
    print("⚠️ 出错：", e)