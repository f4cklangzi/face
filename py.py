import cv2

def detect_motion(video_path, threshold=25, duration=5):
    """
    检测视频中画面变动的起止时间，直到连续5秒无变化后结束记录。
    
    参数：
    - video_path: 视频文件路径
    - threshold: 像素值变化的阈值
    - duration: 画面无变化的最短持续时间，单位为秒
    """
    cap = cv2.VideoCapture(video_path)  # 打开视频文件
    if not cap.isOpened():  # 检查视频是否成功打开
        print("无法打开视频文件")
        return

    frame_rate = cap.get(cv2.CAP_PROP_FPS)  # 获取视频帧率（每秒帧数）
    frame_duration = 1 / frame_rate  # 每帧持续的时间（秒）
    prev_frame = None  # 保存上一帧图像，用于计算帧差
    motion_start = None  # 记录变动开始的帧索引
    motion_detected = False  # 变动标志位
    no_motion_frames = 0  # 连续无变化帧数计数器

    frame_count = 0  # 帧计数器

    while True:
        ret, frame = cap.read()  # 读取视频帧
        if not ret:  # 如果读取失败，说明到达视频末尾
            break

        frame_count += 1  # 增加帧计数
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
        gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)  # 高斯模糊降噪

        if prev_frame is not None:  # 如果上一帧存在
            frame_diff = cv2.absdiff(prev_frame, gray_frame)  # 计算帧差
            _, thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)
            # 二值化处理，突出变动区域
            motion_pixels = cv2.countNonZero(thresh)  # 统计变动的像素点数量

            if motion_pixels > 500:  # 如果像素变化超过阈值，认为有变动
                if not motion_detected:  # 如果变动刚开始
                    motion_start = frame_count  # 记录变动起始帧
                motion_detected = True  # 标记变动为True
                no_motion_frames = 0  # 重置无变化计数器
            else:  # 如果当前帧无明显变化
                if motion_detected:  # 变动已发生
                    no_motion_frames += 1  # 增加无变化帧计数
                    if no_motion_frames >= frame_rate * duration:  # 如果连续无变化帧达到时长
                        start_time = motion_start * frame_duration  # 计算变动起始时间
                        end_time = (frame_count - no_motion_frames) * frame_duration  # 计算变动结束时间
                        print(f"画面变动检测到，起始时间: {start_time:.2f}s, 结束时间: {end_time:.2f}s")
                        cap.release()  # 释放视频资源
                        return
                else:
                    no_motion_frames = 0  # 无变动时重置计数器

        prev_frame = gray_frame  # 更新当前帧为上一帧

    if not motion_detected:
        print("无画面变动超过指定时长")
    cap.release()  # 释放视频资源

# 示例调用
video_path = "your_video_file.mp4"  # 替换为视频文件路径
detect_motion(video_path)  # 调用函数
