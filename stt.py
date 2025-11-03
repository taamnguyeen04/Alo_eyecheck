import speech_recognition as sr
# from vosk import Model, KaldiRecognizer
# import pyaudio
# import json

def recognize_speech():
    """
    Nhận diện giọng nói và chuyển đổi thành văn bản.
    """
    r = sr.Recognizer()
    with sr.Microphone(device_index=18) as source:
        # r.energy_threshold = 100  # mặc định khoảng 300, giảm để bắt âm nhỏ
        # r.pause_threshold = 0.3   # giảm thời gian chờ im lặng
        # r.non_speaking_duration = 0.3  # phải nhỏ hơn pause_threshold
        print("Nói gì đó: ")
        audio = r.listen(source, phrase_time_limit=2)
        print(1)
    try:
        print(2)
        text = r.recognize_google(audio, language="vi-VI")
        print(text)
        return text
    except sr.UnknownValueError:
        return "Không nhận diện được giọng nói."
    except sr.RequestError:
        return "Lỗi kết nối đến dịch vụ nhận diện giọng nói."

# https://alphacephei.com/vosk/models
# def recognize_speech_vosk(model_path="vosk-model-vn-0.4"):
#     """
#     Nhận diện giọng nói bằng Vosk (offline, hỗ trợ tiếng Việt).
#     Trả về chuỗi văn bản đã nhận dạng.
#     """

#     # Tải model Vosk
#     model = Model(model_path)
#     recognizer = KaldiRecognizer(model, 16000)

#     # Khởi tạo microphone
#     mic = pyaudio.PyAudio()
#     stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000,
#                       input=True, frames_per_buffer=8000)
#     stream.start_stream()

#     print("Nói gì đó: ")

#     # Thu âm trong một khoảng ngắn (ví dụ 3 giây)
#     frames = []
#     for _ in range(int(16000 / 4000 * 3)):  # khoảng 3 giây
#         data = stream.read(4000, exception_on_overflow=False)
#         frames.append(data)
#         if recognizer.AcceptWaveform(data):
#             break

#     # Dừng stream
#     stream.stop_stream()
#     stream.close()
#     mic.terminate()

#     # Xử lý kết quả
#     text_result = recognizer.FinalResult()
#     text_json = json.loads(text_result)
#     text = text_json.get("text", "").strip()

#     if text:
#         print("Bạn nói:", text)
#         return text
#     else:
#         return "Không nhận diện được giọng nói."

if __name__ == '__main__':
    # recognize_speech_vosk()
    recognize_speech()
