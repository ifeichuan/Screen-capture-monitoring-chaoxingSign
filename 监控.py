from PIL import Image  # 导入ImageGrab模块，用于截取屏幕图像
import numpy as np  # 导入numpy模块，用于处理图像数据
import os  # 导入os模块，用于文件和文件夹操作
import win32api 
import win32ui 
import win32con 
import win32gui
import requests
import time
import socket
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
# 设置截图保存路径
def capture_screenshot(file_path):
    # 获取桌面窗口句柄
    hdesktop = win32gui.GetDesktopWindow()
    
    # 获取屏幕尺寸
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    print(f"Screen width: {width}, Screen height: {height}")
    print(f"Screen left: {left}, Screen top: {top}")
    
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    # 创建位图对象
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

    # 将屏幕内容复制到内存位图中
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

    # 保存位图到文件
    screenshot.SaveBitmapFile(mem_dc, file_path)

    # 释放资源
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())
    img_dc.DeleteDC()
    win32gui.ReleaseDC(hdesktop, desktop_dc)
    with Image.open("screenhost.png") as img: 
        img = img.resize(
            (int(width*0.75), int(height *0.75)),
    #     #     # Image.ANTIALIAS
        )
    #     # 保存压缩后的图像
        img.save(file_path, format='JPEG', quality=80)  # 用
 
# 定义监控区域的左上角和右下角坐标
url = "http://127.0.0.1:3000/upload"
monitor_region = ()  
name = socket.gethostname()
try:
    while True:  # 进入无限循环，持续监控屏幕变化
        # 获取当前屏幕截图
        # current_screenshot = capture_screenshot("screenhot.jpg")  # 截取指定区域的屏幕图像，并赋值给current_screenshot变量
        #     # 生成截图文件名
        capture_screenshot("screenhost.png")
        #     # 保存截图
        # current_screenshot.save(screenshot_path)  # 将当前截图保存为图片文件
            
        response = requests.post(url, files={'image':open("screenhost.png",'rb')},data={
            "name":name
        })  # 发送POST请求，上传截图文件
        if(response.status_code==200):
            print("上传成功")
            # 输出截图信息
        # print(f"Scree")  # 打印截图保存路径

            
 
        # 每隔一定时间进行一次截图
        time.sleep(2.5)  # 2.5秒钟检查一次屏幕变化，可根据需要调整
except KeyboardInterrupt:  # 捕获键盘中断异常，用于停止监控
    print("Monitoring stopped.")  # 打印停止监控的提示信息


