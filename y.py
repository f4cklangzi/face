import cv2
import numpy as np

# 初始化视频捕捉
cap = cv2.VideoCapture('your_video_file.mp4')

# 检查视频是否打开
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# 设置视频读取的帧率，默认是每秒读取一帧
fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(fps)  # 每秒读取的帧数

# 初始化背景减除器
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)

# 用于存储上次帧与当前帧的差异
frame_diff_count = 0
motion_detected = False

# 上一帧的时间戳
last_timestamp = -1

while True:
    ret = cap.grab()  # 只读取下一帧，不解码
    if not ret:
        break

    timestamp = cap.get(cv2.CAP_PROP_POS_FRAMES)  # 获取当前帧数
    if timestamp % frame_interval != 0:
        continue  # 只处理每秒钟的第一帧

    ret, frame = cap.read()
    if not ret:
        break

    # 转换为灰度图，减少计算量
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 使用背景减除法计算前景
    fg_mask = fgbg.apply(gray)

    # 计算前景掩码的变化，阈值设定用于避免噪声影响
    _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

    # 计算前景图像中的白色像素（即运动区域）
    motion_area = np.sum(fg_mask) / 255  # 计算有多少白色像素

    # 如果运动区域大于一定的阈值，认为有物体移动
    if motion_area > 5000:  # 可以调整该值来控制灵敏度
        frame_diff_count += 1
    else:
        frame_diff_count = 0

    # 如果有超过3秒的连续变化
    if frame_diff_count > 3 * fps:  # 3秒连续变化
        print("True")
        break

    # 更新上一帧时间戳
    last_timestamp = timestamp

# 如果整个视频都没有检测到足够的变化
if frame_diff_count == 0:
    print("False")

cap.release()
cv2.destroyAllWindows()
