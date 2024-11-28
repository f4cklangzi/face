import cv2
import numpy as np
import time

def is_motion_detected(video_path):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps)  # 每秒读取一帧
    prev_frame = None
    change_detected_time = 0  # 记录画面变化时间
    motion_threshold = 3  # 持续变化阈值（秒）

    while cap.isOpened():
        # 跳过到下一个关键帧（模拟每秒读取一帧）
        for _ in range(interval - 1):
            cap.grab()

        ret, frame = cap.read()
        if not ret:
            break

        # 将帧转换为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is not None:
            # 使用ORB检测特征点并匹配
            orb = cv2.ORB_create()
            kp1, des1 = orb.detectAndCompute(prev_frame, None)
            kp2, des2 = orb.detectAndCompute(gray, None)

            if des1 is not None and des2 is not None:
                # 特征点匹配
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(des1, des2)

                # 计算匹配点的变动量
                if len(matches) > 0:
                    distances = [m.distance for m in matches]
                    avg_distance = np.mean(distances)

                    # 全局变化检测（摄像头转动） - 忽略全局特征变化
                    if avg_distance < 30:  # 距离小于阈值，视为整体移动，忽略
                        change_detected_time = max(0, change_detected_time - 1)
                        continue

            # 检测局部变化（帧差法）
            diff = cv2.absdiff(prev_frame, gray)
            non_zero_count = np.count_nonzero(diff > 50)  # 变化较大的像素点数量
            non_zero_ratio = non_zero_count / gray.size

            if non_zero_ratio > 0.01:  # 局部变化超过1%
                change_detected_time += 1
            else:
                change_detected_time = max(0, change_detected_time - 1)

        # 更新前一帧
        prev_frame = gray

        # 判断是否持续变化超过阈值
        if change_detected_time >= motion_threshold:
            print("TRUE")
        else:
            print("FALSE")

        # 显示帧以调试（可以注释掉）
        # cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# 使用示例
video_path = "your_video.mp4"  # 或者用摄像头：video_path = 0
is_motion_detected(video_path)
