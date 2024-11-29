import cv2
import numpy as np

def detect_motion(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("无法打开视频文件")
        return

    # 读取第一帧，作为初始背景
    ret, prev_frame = cap.read()
    if not ret:
        print("无法读取视频帧")
        cap.release()
        return

    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    consecutive_changes = 0  # 用于记录连续变化的秒数
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # 获取帧率
    sec = 1

    while True:
        # 跳过每秒的其他帧
        for _ in range(fps - 1):
            cap.grab()
        
        # 读取当前秒的第一帧
        ret, frame = cap.read()
        if not ret:
            break  # 结束条件：视频读取结束

        # 转为灰度图
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 计算帧间差分
        frame_diff = cv2.absdiff(prev_frame_gray, frame_gray)

        # 计算变化区域面积
        _, diff_thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
        motion_area = cv2.countNonZero(diff_thresh)

        # 使用直方图计算相似度，排除摄像头转动影响
        hist_prev = cv2.calcHist([prev_frame_gray], [0], None, [256], [0, 256])
        hist_curr = cv2.calcHist([frame_gray], [0], None, [256], [0, 256])
        similarity = cv2.compareHist(hist_prev, hist_curr, cv2.HISTCMP_CORREL)

        # 如果变化区域大且直方图相似性低，判断为有物体移动
        if motion_area > 500 and similarity < 0.9:
            consecutive_changes += 1
        else:
            consecutive_changes = 0

        # 如果连续变化超过3秒，打印True并结束程序
        if consecutive_changes >= 3:
            print("True")
            cap.release()
            return

        # 更新上一帧
        prev_frame_gray = frame_gray
        sec += 1

    # 如果遍历完整个视频没有检测到连续变化
    print("False")
    cap.release()

# 使用方法：传入视频路径
detect_motion("path_to_video.mp4")
