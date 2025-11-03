# import sounddevice as sd
# import numpy as np
# import pyaudio

# device_index = 1  # mic bạn muốn test
# duration = 3  # thu 3 giây
# sample_rate = 16000

# print(f"Đang thu thử từ thiết bị {device_index} trong {duration} giây...")

# sd.default.device = (device_index, None)  # (input_device, output_device)
# audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
# sd.wait()

# max_amp = np.abs(audio).max()
# print(f"Max âm lượng thu được: {max_amp}")

# if max_amp == 0:
#     print("⚠️ Mic này không thu được âm thanh — có thể đang tắt, không được chọn hoặc Windows không cấp quyền.")
# elif max_amp < 100:
#     print("🔈 Mic hoạt động nhưng tín hiệu yếu — có thể do khoảng cách hoặc độ nhạy thấp.")
# else:
#     print("✅ Mic hoạt động tốt!")

# # p = pyaudio.PyAudio()
# # for i in range(p.get_device_count()):
# #     info = p.get_device_info_by_index(i)
# #     print(i, info["name"])