import cv2
import numpy as np
import sounddevice as sd
import wave
from threading import Thread
from moviepy.editor import VideoFileClip, AudioFileClip

def record_audio(filename, duration=15, samplerate=44100):
    """录制音频"""
    def audio_callback(indata, frames, time, status):
        audio_frames.append(indata.copy())

    print("开始录制音频...")
    audio_frames = []
    with sd.InputStream(samplerate=samplerate, channels=2, callback=audio_callback):
        sd.sleep(duration * 1000)

    print("音频录制完成，保存中...")
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)  # 双声道
        wf.setsampwidth(2)  # 每样本2字节
        wf.setframerate(samplerate)
        wf.writeframes(b''.join(audio_frames))

def record_video(filename, duration=15):
    """录制视频"""
    print("开始录制视频...")
    cap = cv2.VideoCapture(0)  # 打开摄像头
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))

    start_time = cv2.getTickCount()
    while (cv2.getTickCount() - start_time) / cv2.getTickFrequency() < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Recording', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 键中止
                break
        else:
            break

    print("视频录制完成，保存中...")
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def combine_audio_video(video_file, audio_file, output_file):
    """合成音频和视频"""
    print("正在合成音频和视频...")
    video_clip = VideoFileClip(video_file)
    audio_clip = AudioFileClip(audio_file)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
    print("合成完成！")

if __name__ == "__main__":
    video_file = "output_video.mp4"
    audio_file = "output_audio.wav"
    output_file = "final_output.mp4"

    # 使用多线程同时录制视频和音频
    audio_thread = Thread(target=record_audio, args=(audio_file,))
    video_thread = Thread(target=record_video, args=(video_file,))

    audio_thread.start()
    video_thread.start()

    audio_thread.join()
    video_thread.join()

    # 合成音频和视频
    combine_audio_video(video_file, audio_file, output_file)