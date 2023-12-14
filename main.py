import time
import cv2
from paddleocr import PaddleOCR
import pyautogui
import logging
import numpy as np

logging.disable(logging.DEBUG)
logging.disable(logging.WARNING)
pyautogui.FAILSAFE = False

def get_screen_size():
    width, height = pyautogui.size()
    return width, height

# 使用示例
screen_width, screen_height = get_screen_size()

# 配置PaddleOCR的中文语言包路径
ocr = PaddleOCR(use_angle_cls=False, lang="ch", show_log=False)

# 获取字符串在屏幕上的位置
def get_string_location_on_screen(text, region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save('./log/screenshot.png')
    image = cv2.imread('./log/screenshot.png')
    time.sleep(1)
    result = ocr.ocr(image, cls=True)
    if text in str(result):
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                if text in str(line):
                    print(int(region[0]+(line[0][0][0]+line[0][2][0])//2), int(region[1]+(line[0][0][1]+line[0][2][1])//2))
                    return int(region[0]+(line[0][0][0]+line[0][2][0])//2), int(region[1]+(line[0][0][1]+line[0][2][1])//2)
    return None, None


# 功能一：检测屏幕特定区域，检测是否有某个字符串出现
def detect_string(text, region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save('./log/screenshot.png')
    image = cv2.imread('./log/screenshot.png')
    time.sleep(1)
    result = ocr.ocr(image, cls=True)
    if text in str(result):
        return True
    else:
        print("未找到", text)
        return False

# 功能二：检测屏幕特定区域，检测是否有某个字符串出现，有则点击字符串所在处
def detect_and_click_string(text, region, trytime):
    wait_time = 0
    while not detect_string(text, region) and wait_time < 3:
        print('等待出现', text)
        time.sleep(1)
        wait_time = wait_time + 1
    x, y = get_string_location_on_screen(text, region)
    tryTime = trytime or 0
    if x and y:
        time.sleep(1)
        pyautogui.click(x, y)
        print(text, "click", x, y, region)
    else:
        print("try", text)
        time.sleep(1)
        if tryTime < 1:
            detect_and_click_string(text, region, tryTime+1)

# 功能三：检测屏幕特定区域，检测是否有某个特定图像出现
def detect_image(img_path, region):
    sample_image = cv2.imread(img_path, 0)
    target_image = pyautogui.screenshot(region=region)
    target_image.save('./log/screenshot.png')
    target_image = cv2.cvtColor(np.array(target_image), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(target_image, sample_image, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.80  # 设置匹配的阈值
    if max_val >= threshold:
        return True
    else:
        return False

# 功能四：检测屏幕特定区域，检测是否有某个特定图像出现，有则点击图像中心点
def detect_and_click_image(img_path, region):
    wait_time = 0
    while not detect_image(img_path, region) and wait_time < 3:
        print("等待图片", img_path)
        time.sleep(1)
        wait_time = wait_time + 1

    sample_image = cv2.imread(img_path, 0)
    target_image = pyautogui.screenshot(region=region)
    target_image = cv2.cvtColor(np.array(target_image), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(target_image, sample_image, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.80  # 设置匹配的阈值
    if max_val >= threshold:
        top_left = max_loc
        img_center = (int(top_left[0] + sample_image.shape[1] // 2), int(top_left[1] + sample_image.shape[0] // 2))
        pyautogui.click(img_center[0] + region[0], img_center[1] + region[1])
        print("click", img_center[0] + region[0], img_center[1] + region[1], region)
    else:
        print("无法找到以下图片，请尝试自行替换为自己截取的图片：", img_path)

# 功能五：文本化
def get_text(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save('./log/screenshot.png')
    image = cv2.imread('./log/screenshot.png')
    time.sleep(1)
    result = ocr.ocr(image, cls=True)
    text = ""
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text += line[1][0]
    return text

# 使用示例
region_1 = (0, 0, int(0.5*screen_width), int(0.5*screen_height))  # 示例区域1
region_2 = (int(0.5*screen_width), 0, int(0.5*screen_width), int(0.5*screen_height))  # 示例区域2
region_3 = (0, int(0.75*screen_height), int(0.5*screen_width), int(0.25*screen_height))  # 示例区域2
region_4 = (int(0.5*screen_width), int(0.75*screen_height), int(0.5*screen_width), int(0.25*screen_height))  # 示例区域2
region_13 = (0, 0, int(0.5*screen_width), int(screen_height))  # 示例区域2
region_24 = (int(0.5*screen_width), 0, int(0.5*screen_width), int(screen_height))  # 示例区域2
region_12 = (0, 0, int(screen_width), int(0.5*screen_height))  # 示例区域2
region_34 = (0, int(0.5*screen_height), int(screen_width), int(0.5*screen_height))  # 示例区域2
region_full = (0, 0, int(screen_width), int(screen_height))
region_center = (int(0.25*screen_width), int(0.5*screen_height), int(0.5*screen_width), int(0.25*screen_height))
#  1 | 2
# -------
#  3 | 4

print(get_text(region_full))
"""
if detect_string('精通等级 3', region_13):
    print('字符串存在')
else:
    print('未检测到')


detect_and_click_string('艺术创新', region_12, 0)

if detect_image('./img/test.png', region_1):
    print('图像存在')
else:
    print('未检测到')

detect_and_click_image('./img/test.png', region_1)
"""

character_point = 1

# 主界面
def main_page():
    print('main page')
    if detect_image('./img/start.png', region_4):
        detect_and_click_image('./img/start.png', region_4)
        time.sleep(1)
    elif detect_string('终止', region_4):
        detect_and_click_string('终止', region_4, 0)
        time.sleep(1)
        detect_and_click_string('确认', region_center, 0)
        time.sleep(1)
        pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
        time.sleep(1)
        pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
        time.sleep(1)
        while not detect_image('./img/start.png', region_4) and not detect_image('./img/nextstep.png', region_4):
            if detect_string('下一页', region_4):
                while not detect_string('完成', region_4):
                    detect_and_click_string('下一页', region_4, 0)
                    time.sleep(1)
                detect_and_click_string('完成', region_4, 0)
                time.sleep(1)
                pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
                time.sleep(1)
                pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
                time.sleep(1)
                pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
                time.sleep(1)
            pyautogui.click(int(0.5 * screen_width), int(0.5 * screen_height))
            main_page()
    else:
        main_page()

# 难度
def chose_difficulty():
    print('difficulty')
    if detect_image('./img/nextstep.png', region_4):
        pyautogui.click(int(0.5*screen_width), int(0.5*screen_height))
        time.sleep(1)
        detect_and_click_image('./img/nextstep.png', region_4)
    else:
        chose_difficulty()

# 编队
def formation():
    print('编队')
    time.sleep(2)
    while not detect_image('./img/checkin.png', region_4):
        pyautogui.click(screen_width*0.2, screen_height*0.5)
        time.sleep(2)
    while not detect_image('./img/checkinEnd.png', region_4):
        detect_and_click_image('./img/checkin.png', region_4)
        time.sleep(2)
    detect_and_click_image('./img/checkinEnd.png', region_4)

# 领奖
def get_equip():
    print("get equip")
    page_text = get_text(region_full)
    retry_time = 0
    while '请选择装备' not in page_text and retry_time < 10:
        print("等待装备选择")
        time.sleep(1)
        page_text = get_text(region_full)
        retry_time = retry_time + 1
    retry_time = 0
    while '确定' not in page_text and retry_time < 10:
        if '可激活' in page_text:
            detect_and_click_string('可激活', region_full, 0)
            time.sleep(2)
        elif '已装备' in page_text:
            detect_and_click_string('已装备', region_full, 0)
            time.sleep(2)
        elif '自动恢复' in page_text:
            detect_and_click_string('自动恢复', region_full, 0)
            time.sleep(2)
        elif '生命' in page_text and '消耗生命' not in page_text:
            detect_and_click_string('生命', region_full, 0)
            time.sleep(2)
        elif '推荐驻场角色' in page_text:
            detect_and_click_string('推荐驻场角色', region_full, 0)
            time.sleep(2)
        else:
            pyautogui.click(int(0.5 * screen_width), int(0.5 * screen_height))
            time.sleep(2)
        page_text = get_text(region_full)
    retry_time = 0
    while '离开' not in page_text and '藏品' not in page_text and '结束购物' not in page_text and retry_time < 10:
        detect_and_click_string('确定', region_4, 0)
        time.sleep(1)
        pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))  # 防止激活提示卡死
        time.sleep(1)
        pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))  # 防止激活提示卡死
        page_text = get_text(region_full)

def get_buff():
    print("get buff")
    page_text = get_text(region_full)
    retry_time = 0
    while not ('领取奖励' in page_text and '离开' not in page_text and retry_time > 10):
        print("等待buff选择")
        time.sleep(1)
        page_text = get_text(region_full)
        retry_time = retry_time + 1
    page_text = get_text((0, int(0.25*screen_height), screen_width, int(0.75*screen_height)))
    print(page_text)
    retry_time = 0
    while '领取' not in page_text and retry_time < 10:
        print("选择buff")
        if '核心修复' in page_text:
            detect_and_click_string('核心修复', region_full, 0)
            pyautogui.click()
        elif '燃血' in page_text:
            detect_and_click_string('燃血', region_full, 0)
            pyautogui.click()
        elif '预加载' in page_text:
            detect_and_click_string('预加载', region_full, 0)
            pyautogui.click()
        elif '过载效应' in page_text:
            detect_and_click_string('过载效应', region_full, 0)
            pyautogui.click()
        elif '递延病毒' in page_text:
            detect_and_click_string('递延病毒', region_full, 0)
            pyautogui.click()
        elif '生命值' in page_text:
            detect_and_click_string('生命值', region_full, 0)
            pyautogui.click()
        elif '核心调优' in page_text:
            detect_and_click_string('核心调优', region_full, 0)
            pyautogui.click()
        elif '性能组件' in page_text:
            detect_and_click_string('性能组件', region_full, 0)
            pyautogui.click()
        elif '向量组件' in page_text:
            detect_and_click_string('向量组件', region_full, 0)
            pyautogui.click()
        else:
            pyautogui.click(int(0.5 * screen_width), int(0.6 * screen_height))
            pyautogui.click()
        time.sleep(1)
        page_text = get_text((0, int(0.25 * screen_height), screen_width, int(0.75 * screen_height)))
    page_text = get_text(region_4)
    retry_time = 0
    while '离开' not in page_text and '藏品' not in page_text and '结束购物' not in page_text and retry_time < 10:
        detect_and_click_string('领取', region_34, 0)
        time.sleep(1)
        pyautogui.click(int(0.5 * screen_width), int(0.9 * screen_height))
        page_text = get_text(region_4)


def get_reward():
    while True:
        time.sleep(1)
        if not detect_string('领取', region_34):
            print('离开')
            break
        else:
            print('领奖')
            detect_and_click_string('领取', region_34, 0)
            time.sleep(2)
            page_text = get_text(region_full)
            while ('领取奖励' in page_text and '离开' not in page_text) or '请选择装备' in page_text or '获得奖励' in page_text:
                if '请选择装备' in page_text:  # 装备类
                    get_equip()
                elif '获得奖励' in page_text:  # 一般奖励
                    print('一般奖励')
                    time.sleep(1)
                    pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))
                    time.sleep(0.5)
                    pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))
                elif '领取奖励' in page_text and '离开' not in page_text:  # buff类
                    get_buff()
                time.sleep(1)
                page_text = get_text(region_full)
    while not detect_string('藏品', region_4):
        detect_and_click_string('离开', region_4, 0)
        time.sleep(1)

# 出发
def tiexin_dadang():
    while not detect_string('出发', region_4):
        detect_and_click_string('大包裹', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('出发', region_4, 0)
    time.sleep(1)
    pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))

def bulv_panshan():
    while not detect_string('决定', region_4):
        detect_and_click_string('跟上他', region_4, 0)
        time.sleep(1)
    while not detect_string('查看信封', region_4):
        detect_and_click_string('看看保险柜', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('查看信封', region_4, 0)
    time.sleep(1)
    detect_and_click_string('打开暗格', region_4, 0)
    time.sleep(1)
    detect_and_click_string('取走补给', region_4, 0)
    get_equip()

def wugui_xinzhu():
    global character_point
    while not detect_string('出发', region_4):
        detect_and_click_string('物归原主', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('出发', region_4, 0)
    time.sleep(1)
    pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))
    character_point = character_point + 2

def yinmi_gongfang():
    global character_point
    while not detect_string('决定', region_4):
        detect_and_click_string('收取', region_4, 0)
        time.sleep(1)
        pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))
        time.sleep(1)
    while not detect_string('出发', region_4):
        detect_and_click_string('直接出发', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('出发', region_4, 0)
    character_point = character_point + 2

def huozai_xianchang():
    while not detect_string('决定', region_4):
        detect_and_click_string('推测', region_4, 0)
        time.sleep(1)
    while not detect_string('检查尸体', region_4):
        detect_and_click_string('愚蠢的失误', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('检查尸体', region_4, 0)
    time.sleep(1)
    detect_and_click_string('离开', region_4, 0)
    time.sleep(1)
    pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))

def touhao_wanjia():
    while not detect_string('决定', region_4):
        detect_and_click_string('继续', region_4, 0)
        time.sleep(1)
    while not detect_string('离开', region_4):
        detect_and_click_string('月光', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)
    time.sleep(1)
    pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))

def jushou_zhilao():
    while not detect_string('离开', region_4):
        detect_and_click_string('去花园', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)
    time.sleep(1)
    get_buff()

def yanpin_gongjiang():
    while not detect_string('离开', region_4):
        detect_and_click_string('游戏机的芯片', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)
    time.sleep(1)
    pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))

def Jsgame():
    while not detect_string('答应', region_4):
        detect_and_click_string('追上她', region_4, 0)
        time.sleep(1)
    while not detect_string('决定', region_4):
        detect_and_click_string('答应', region_4, 0)
        time.sleep(1)
    while not detect_string('摸索', region_4):
        detect_and_click_string('熊布偶', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('摸索', region_4, 0)
    time.sleep(1)
    detect_and_click_string('回头', region_4, 0)
    time.sleep(1)
    get_buff()
    time.sleep(1)
    detect_and_click_string('一起离开', region_4, 0)

def pinkun_shoucangjia():
    while not detect_string('离开', region_4):
        detect_and_click_string('拒绝', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)

def dongwu_fenchang():
    while not detect_string('决定', region_24):
        detect_and_click_string('查看周围', region_4, 0)
        time.sleep(1)
    while not detect_string('搜索', region_4):
        detect_and_click_string('挖掘', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('搜索', region_4, 0)
    time.sleep(1)
    while not detect_string('离开', region_4):
        detect_and_click_string('水井', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)
    time.sleep(1)
    get_equip()

def tiantai_niudanji():
    while not detect_string('离开', region_4):
        detect_and_click_string('还是算了', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)
    time.sleep(1)

def niudanji():
    while not detect_string('离开', region_4):
        detect_and_click_string('还是算了', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)

def xuxu_rusheng():
    while not detect_string('继续', region_24):
        detect_and_click_string('看向油画', region_24, 0)
        time.sleep(1)
    while not detect_string('决定', region_24):
        detect_and_click_string('继续', region_24, 0)
        time.sleep(1)
    while not detect_string('转身去追女人', region_24):
        detect_and_click_string('绝境的希望', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    while not detect_string('离开', region_4):
        detect_and_click_string('取下纸条', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)
    time.sleep(1)
    pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))

def xiaci_zaowu():
    while not detect_string('决定', region_4):
        detect_and_click_string('观赏大卫', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    while not detect_string('决定', region_4):
        detect_and_click_string('取走胶囊', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)
    time.sleep(1)
    pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))

def zhiming_shiwu():
    while not detect_string('取走东西', region_4):
        detect_and_click_string('日志阅读', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('取走东西', region_4, 0)
    time.sleep(1)
    detect_and_click_string('赶紧离开', region_4, 0)
    time.sleep(1)
    get_equip()

def eyun_liansuo():
    while not detect_string('冲上前', region_4):
        detect_and_click_string('上前', region_4, 0)
        time.sleep(1)
    while not detect_string('挣脱', region_4):
        detect_and_click_string('躲开', region_24, 0)
        detect_and_click_string('冲上前', region_4, 0)
        time.sleep(1)
    while not detect_string('直面', region_4):
        detect_and_click_string('挣脱', region_4, 0)
        time.sleep(1)
    detect_and_click_string('直面', region_4, 0)
    time.sleep(1)
    battle()

def buxiang_laoyin():
    global character_point
    while not detect_string('决定', region_4):
        detect_and_click_string('前进', region_4, 0)
        time.sleep(1)
    while not detect_string('环顾四周', region_4):
        detect_and_click_string('询问', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    while not detect_string('取走', region_4):
        detect_and_click_string('环顾四周', region_4, 0)
        time.sleep(1)
    while not detect_string('决定', region_4):
        detect_and_click_string('取走', region_4, 0)
        time.sleep(1)
        pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
        time.sleep(1)
    while not detect_string('调整了下状态', region_4):
        detect_and_click_string('直接出发', region_24, 0)
        detect_and_click_string('决定', region_2, 0)
        time.sleep(1)
    detect_and_click_string('出发', region_24, 0)
    character_point = character_point + 2

def taochu_shengtian():
    while not detect_string('决定', region_4):
        detect_and_click_string('环顾四周', region_4, 0)
        time.sleep(1)
    while not detect_string('大声惨叫', region_2):
        detect_and_click_string('让她试试', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    while not detect_string('安抚', region_4):
        detect_and_click_string('拉回绳子', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    while not detect_string('离开', region_4):
        detect_and_click_string('安抚', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)
    time.sleep(1)
    get_buff()

def shuxia_nvwu():
    while not detect_string('决定', region_4):
        detect_and_click_string('上前', region_4, 0)
        time.sleep(1)
    while not detect_string('离开', region_4):
        detect_and_click_string('接受少女的好意', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    while not detect_string('继续前行', region_4):
        detect_and_click_string('离开', region_4, 0)
        time.sleep(1)
    detect_and_click_string('继续前行', region_4, 0)
    time.sleep(1)
    pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))

def Jsstory():
    while not detect_string('决定', region_4):
        detect_and_click_string('继续', region_4, 0)
        time.sleep(1)
    while not detect_string('继续', region_4):
        detect_and_click_string('旅行者的故事', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    while not detect_string('zz', region_4):
        detect_and_click_string('继续', region_4, 0)
        time.sleep(1)
    detect_and_click_string('zz', region_4, 0)
    time.sleep(1)
    get_equip()

def xiuqi_zhidi():
    global character_point
    detect_and_click_string('前往', region_4, 0)
    time.sleep(1)
    pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
    character_point = character_point + 2

def caineng_jiaxiang():
    while not detect_string('决定', region_4):
        detect_and_click_string('继续', region_4, 0)
        time.sleep(1)
    while not detect_string('离开', region_4):
        detect_and_click_string('赚钱', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)
    time.sleep(1)
    pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))

def yingxiong_jiaxiang():
    while not detect_string('决定', region_4):
        detect_and_click_string('跟随他', region_4, 0)
        time.sleep(1)
    while not detect_string('离开', region_4):
        detect_and_click_string('答应他', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('离开', region_4, 0)
    time.sleep(1)
    pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))

def zidonghua_gongfang():
    while not detect_string('决定', region_4):
        detect_and_click_string('继续', region_4, 0)
        time.sleep(1)
    while not detect_string('进入', region_4):
        detect_and_click_string('进入工坊', region_24, 0)
        detect_and_click_string('决定', region_4, 0)
        time.sleep(1)
    detect_and_click_string('进入', region_4, 0)
    time.sleep(1)
    pyautogui.press('esc')
    time.sleep(1)
    detect_and_click_string('确定', region_34, 0)
    time.sleep(1)
    pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))

def shenyuan_yuyin():
    while not detect_string('点头', region_4):
        detect_and_click_string('转身', region_4, 0)
        time.sleep(1)
    while not detect_string('前', region_4):
        detect_and_click_string('握紧', region_24, 0)
        detect_and_click_string('点头', region_4, 0)
        time.sleep(1)
    detect_and_click_string('前', region_4, 0)
    time.sleep(1)
    battle()



# 鲨士多
def store():
    if detect_string('改进型手提电视', region_24):
        detect_and_click_string('改进型手提电视', region_24, 0)
        time.sleep(1)
        detect_and_click_string('购买', region_4, 0)
        time.sleep(0.2)
        if detect_image('./img/store-no-coin.png', region_full):
            pass
        else:
            time.sleep(1)
            get_equip()
            time.sleep(1)
            pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))
    if detect_string('速递包裹', region_24):
        detect_and_click_string('速递包裹', region_24, 0)
        time.sleep(1)
        detect_and_click_string('购买', region_4, 0)
        time.sleep(0.2)
        if detect_image('./img/store-no-coin.png', region_full):
            pass
        else:
            time.sleep(1)
            get_buff()
            time.sleep(1)
            pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))
    if detect_string('向量组件', region_24):
        detect_and_click_string('向量组件', region_24, 0)
        time.sleep(1)
        detect_and_click_string('购买', region_4, 0)
        time.sleep(0.2)
        if detect_image('./img/store-no-coin.png', region_full):
            pass
        else:
            time.sleep(1)
            pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))
    if detect_string('演算增效', region_24):
        detect_and_click_string('演算增效', region_24, 0)
        time.sleep(1)
        detect_and_click_string('购买', region_4, 0)
        time.sleep(0.2)
        if detect_image('./img/store-no-coin.png', region_full):
            pass
        else:
            time.sleep(1)
            pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))
    else:
        pass
    time.sleep(1)
    detect_and_click_string('结束购物', region_4, 0)
    time.sleep(1)
    detect_and_click_string('确认', region_center, 0)
    time.sleep(1)
    detect_and_click_string('结束购物', region_4, 0)
    time.sleep(1)
    while not detect_string("藏品", region_4):
        if detect_string("请选择装备", region_12):
            get_equip()
        time.sleep(1)


# 艺术创新/竭诚欢迎/大难临头/迫不及待/疯狂侵攻/守株待兔/本能反应
def battle():
    time.sleep(1)
    detect_and_click_string('出击', region_4, 0)
    time.sleep(3)
    while True:
        pyautogui.press('j')
        time.sleep(0.2)
        pyautogui.press('j')
        time.sleep(0.2)
        pyautogui.press('j')
        time.sleep(0.2)
        pyautogui.press('k')
        time.sleep(0.2)
        pyautogui.press('j')
        time.sleep(0.2)
        pyautogui.press('j')
        time.sleep(0.2)
        pyautogui.press('j')
        time.sleep(0.2)
        pyautogui.press('2')
        time.sleep(0.1)
        pyautogui.press('q')
        pyautogui.press('g')
        time.sleep(0.2)
        pyautogui.press('j')
        time.sleep(0.2)
        pyautogui.press('j')
        time.sleep(0.2)
        pyautogui.press('j')
        time.sleep(0.2)
        pyautogui.press('r')
        # 战斗逻辑
        # ...
        if detect_image('./img/relive.png', (int(0.5*screen_width), int(0.5*screen_height), int(0.5*screen_width), int(0.5*screen_height))):
            detect_and_click_image('./img/relive.png', (int(0.5*screen_width), int(0.5*screen_height), int(0.5*screen_width), int(0.5*screen_height)))
            time.sleep(0.5)
            if detect_image('./img/no-coin.png', region_full):
                detect_and_click_string('放弃', (0, int(0.5*screen_height), int(0.5*screen_width), int(0.5*screen_height)), 0)
                break
        elif detect_image('./img/getreward.png', region_12):
            get_reward()
            break
    print('战斗结束')
    time.sleep(5)


def game():
    global character_point
    retry = 0
    battle_keywords = ["艺术创新", "竭诚欢迎", "大难临头", "迫不及待", "疯狂侵攻", "守株待兔", "本能反应", "随心所欲", "点到为止", "排山倒海", "正当防卫", "范围清理"]
    while True:
        page_text = get_text((int(0.2*screen_width), 0, int(0.8*screen_width), screen_height))
        print(page_text)
        matched_keyword = next((keyword for keyword in battle_keywords if keyword in page_text), None)
        if 'ch.' not in page_text and 'Ch.' not in page_text and 'Chapter' not in page_text:
            continue
        if character_point >= 4:
            pyautogui.click(int(0.5*screen_width), int(0.8*screen_height))
            time.sleep(1)
            while not detect_string('编队', region_12):
                detect_and_click_string('编队', region_4, 0)
                time.sleep(1)
            while not detect_image('./img/4cp.png', region_34):
                pyautogui.click(int(0.5*screen_width), int(0.5*screen_height))
                time.sleep(1)
            while not detect_string('确定', region_4):
                detect_and_click_image('./img/4cp.png', region_13)
                time.sleep(1)
                detect_and_click_string('编入', region_4, 0)
                time.sleep(1)
            detect_and_click_string('确定', region_4, 0)
            character_point = character_point - 4
        if '贴心搭档' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('贴心搭档', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            tiexin_dadang()
        elif '物归新主' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('物归新主', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            wugui_xinzhu()
        elif '举手之劳' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('举手之劳', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            jushou_zhilao()
        elif '步履' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('步履', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            bulv_panshan()
        elif '瑕疵造物' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('瑕疵造物', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            xiaci_zaowu()
        elif '栩栩如生' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('栩栩如生', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            xuxu_rusheng()
        elif '洁塔薇的游戏' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('洁塔薇的游戏', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            Jsgame()
        elif '赝品工匠' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('赝品工匠', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            yanpin_gongjiang()
        elif '贫困收藏家' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('贫困收藏家', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            pinkun_shoucangjia()
        elif '致命失误' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('致命失误', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            zhiming_shiwu()
        elif '隐秘工坊' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('隐秘工坊', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            yinmi_gongfang()
        elif '火灾现场' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('火灾现场', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            huozai_xianchang()
        elif '头号玩家' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('头号玩家', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            touhao_wanjia()
        elif '动物坟场' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('动物坟场', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            dongwu_fenchang()
        elif '逃出生天' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('逃出生天', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            taochu_shengtian()
        elif '厄运连锁' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('厄运连锁', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            eyun_liansuo()
        elif '不详烙印' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('不详烙印', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            buxiang_laoyin()
        elif '天台扭蛋机' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('天台扭蛋机', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            tiantai_niudanji()
        elif '树下女巫' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('树下女巫', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            shuxia_nvwu()
        elif '讲故事' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('讲故事', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            Jsstory()
        elif '休憩之地' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('休憩之地', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            xiuqi_zhidi()
        elif '才能假象' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('才能假象', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            caineng_jiaxiang()
        elif '英雄假象' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('英雄假象', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            yingxiong_jiaxiang()
        elif '自动化工坊' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('自动化工坊', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            zidonghua_gongfang()
        elif '深渊余音' in page_text:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('深渊余音', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            shenyuan_yuyin()
        elif '鲨士多' in page_text:
            retry = 0
            """
            pyautogui.press('esc')
            time.sleep(1)
            detect_and_click_string('确定', region_4, 0)
            break
            """
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string('鲨士多', (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            store()
        elif matched_keyword:
            retry = 0
            while not detect_image('./img/chose.png', region_34):
                detect_and_click_string(matched_keyword, (int(0.2*screen_width), int(0.1*screen_height), int(0.8*screen_width), int(0.4*screen_height)), 0)
                time.sleep(1)
            detect_and_click_image('./img/chose.png', region_34)
            time.sleep(1)
            battle()
        elif '模拟演算完成' in page_text or '链路崩溃' in page_text:
            pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
            time.sleep(1)
            detect_and_click_string('下一页', region_4, 0)
            time.sleep(1)
            detect_and_click_string('下一页', region_4, 0)
            time.sleep(1)
            detect_and_click_string('完成', region_4, 0)
            time.sleep(1)
            pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
            time.sleep(1)
            pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
            time.sleep(1)
            pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
            break
        elif retry > 8:
            pyautogui.press('esc')
            time.sleep(5)
            if detect_string('确定', region_center):
                detect_and_click_string('确定', region_center, 0)
            time.sleep(1)
            pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
            time.sleep(1)
            pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
            time.sleep(1)
            pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
            break
        else:
            pyautogui.click(int(0.5 * screen_width), int(0.8 * screen_height))
            retry = retry + 1

        time.sleep(1)

while True:
    main_page()
    chose_difficulty()
    formation()
    game()
