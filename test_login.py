"""测试登录页面"""
from playwright.sync_api import sync_playwright
import os

# 登录页面路径
login_page = r"D:\vs_code\Smart Analysis\templates\login_new.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 直接打开本地文件
    page.goto(f'file:///{login_page}')
    page.wait_for_load_state('networkidle')

    # 截图
    page.screenshot(path='/tmp/login_page.png', full_page=True)
    print("截图已保存: /tmp/login_page.png")

    # 获取页面标题
    print(f"页面标题: {page.title()}")

    browser.close()
