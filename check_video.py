import sys

import cv2  # 导入OpenCV库，用于处理视频和图像


def detect_motion(video_path, threshold=25, duration=5):
    """
    检测视频中是否有画面变动超过指定的时间段。

    参数：
    - video_path: 视频文件路径
    - threshold: 像素值变化阈值，用于判断帧之间的差异
    - duration: 检测到连续画面变动的最短持续时间，单位为秒
    """
    cap = cv2.VideoCapture(video_path)  # 打开视频文件
    if not cap.isOpened():  # 检查视频是否成功打开
        print("无法打开视频文件")
        return

    frame_rate = cap.get(cv2.CAP_PROP_FPS)  # 获取视频帧率（每秒帧数）
    prev_frame = None  # 保存上一帧图像，用于计算帧差
    motion_detected = False  # 变动标志位，初始为无变动

    frame_count = 0  # 帧计数器，记录当前处理到的视频帧数
    consecutive_motion_frames = 0  # 连续发生变动的帧数计数器

    while True:  # 循环读取视频帧
        ret, frame = cap.read()  # 读取一帧图像
        if not ret:  # 如果读取失败，说明到达视频末尾
            break
        frame_count += 1  # 递增帧计数器
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将当前帧转换为灰度图像
        gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)  # 使用高斯模糊减少噪声

        if prev_frame is not None:  # 如果前一帧存在
            frame_diff = cv2.absdiff(prev_frame, gray_frame)  # 计算当前帧与前一帧的绝对差异
            _, thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)
            # 应用阈值处理，生成二值化图像
            motion_pixels = cv2.countNonZero(thresh)  # 计算变动的像素数量
            if motion_pixels > 2000:  # 判断变动是否超过像素数阈值
                motion_detected = True  # 标记变动为True
                consecutive_motion_frames += 1  # 增加连续变动帧计数
            else:
                if motion_detected and consecutive_motion_frames >= frame_rate * duration:
                    # 如果连续变动帧超过设定时长，输出结果
                    print("TRUE")
                    cap.release()  # 释放视频资源
                    return
                motion_detected = False  # 重置变动标志
                consecutive_motion_frames = 0  # 重置连续变动帧计数

        prev_frame = gray_frame  # 更新上一帧为当前帧

    if not motion_detected or consecutive_motion_frames < frame_rate * duration:
        # 如果整个视频中没有检测到足够长的变动，打印提示
        print("FALSE")
    cap.release()  # 释放视频资源


# 示例调用
def showImg(img, num_changes):
    show_frame = cv2.resize(img, None, fx=0.2, fy=0.2)
    cv2.imshow(str(num_changes), show_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


video_file = args = sys.argv[1]
detect_motion(video_file)  # 调用函数检测画面变动
