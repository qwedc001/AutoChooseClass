import time
import os
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 初始化,可以进行相关的配置
def init(url):
    print("[debug]执行初始化")
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9887")
    print("[debug]已设置debugger参数")
    driver = webdriver.Chrome(options=chrome_options)
    print("[debug]已获取当前chrome程序")
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def choose(driver:webdriver.Chrome, wait:WebDriverWait):
    print("任务开始")
    start_time = time.time()
    # 点击查询
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[1]/div/ul/li[2]/a'))).click() # 这里对应“自主选课”按钮在我的应用的位置
    all_handles = driver.window_handles
    new_window_handle = all_handles[1]
    driver.switch_to.window(new_window_handle)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[1]/div/div/div/div/span/button[1]'))).click()
    # 定位体育课列表
    PE = True
    if PE:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@class="panel panel-info"]/ul/li/a[@id="tab_kklx_06"]'))).click()
    # 定位所有选课列表
    classNames = [
        '大学体育（1）(2023-2024-2)-B151118-5', # 户外运动
        '大学体育（1）(2023-2024-2)-B151107-7'  # 排球
    ]
    time.sleep(3)
    succ = 0
    fail = 0
    total = len(classNames)
    for className in classNames:
        try:
            curClass = driver.find_element(By.XPATH, '//*[@class="body_tr"]/td[@class="jxbmc" and text()="'+className+'"]')
            print("找到课程"+className)
            curClass.find_element(By.XPATH, './/*[@class="an"]').click()
            succ += 1
            break # 体育课只允许选择一门，选择成功后就退出
        except Exception as e:
            print(f'[Error]无法定位课程{className}/该课程的按钮元素')
            fail += 1
    end_time = time.time()
    print(f'已全部完成,总的选课数{total},成功选课数{succ},失败选课数{fail},用时{round(end_time-start_time,2)}秒')
    exit()


if __name__ == '__main__':
    url = 'https://jw.qlu.edu.cn'
    driver, wait = init(url)
    # auto_login(driver, wait)
    schedule.every().day.at("12:00").do(choose, driver, wait)
    print("已完成任务初始化")
    while True:
        schedule.run_pending()
        time.sleep(1)
