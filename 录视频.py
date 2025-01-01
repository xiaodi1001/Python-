import cv2
import time

def auto_record_video(output_file, duration=10, frame_rate=20.0):
    """
    自动录制视频并保存到文件中。

    :param output_file: 输出文件名，例如 'output.avi'
    :param duration: 录制时长（秒）
    :param frame_rate: 视频帧率
    """
    # 打开摄像头
    cap = cv2.VideoCapture(0)  # 0 表示默认摄像头
    if not cap.isOpened():
        print("无法打开摄像头！")
        return

    # 获取摄像头分辨率
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 定义视频编码器和输出文件
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用 XVID 编码
    out = cv2.VideoWriter(output_file, fourcc, frame_rate, (frame_width, frame_height))

    print(f"开始录制视频：{output_file}")
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法捕获视频帧！")
            break

        # 写入视频帧
        out.write(frame)

        # 显示视频（可选）
        cv2.imshow('Recording...', frame)

        # 检查录制时长或按键中断
        if time.time() - start_time > duration or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"视频录制完成：{output_file}")

# 调用录制函数，录制10秒视频
auto_record_video("output.avi", duration=10)