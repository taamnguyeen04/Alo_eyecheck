from tts import text_to_speech
from stt import recognize_speech
from processing import snellen_letter_size, format_size_display, check_answer_match
from chatbot import (
    get_welcome_message, get_eye_test_instruction, get_level_instruction,
    get_feedback, check_child_answer_with_ai, get_final_consultation
)
import random
import pygame

# Constants - Các hằng số quan trọng
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "K", "L", "M", "N", "P", "R", "T", "U", "V", "W", "X", "Y", "Z"]
LEA_SYMBOLS = [
    {"name": "Nhà", "emoji": "🏠", "id": "nha"},
    {"name": "Táo", "emoji": "🍎", "id": "tao"},
    {"name": "Vòng tròn", "emoji": "⚪", "id": "tron"},
    {"name": "Hình vuông", "emoji": "⬜", "id": "vuong"},
]
SNELLEN_DENOMS = [200, 100, 70, 50, 40, 30, 25, 20]  # Từ dễ → khó

def get_user_input(prompt, is_speech):
    """
    Lấy input từ người dùng (gõ phím hoặc giọng nói)

    Args:
        prompt: Câu hỏi hiển thị
        is_speech: True = dùng STT, False = gõ phím

    Returns:
        str: Câu trả lời của người dùng
    """
    print(f"\n{prompt}")
    if is_speech:
        print("Đang lắng nghe...")
        return recognize_speech()
    else:
        return input(">>> ").strip()

def main():
    """
    Hàm main - Thu thập thông tin và điều khiển flow chương trình

    Flow:
    1. Khởi tạo pygame mixer
    2. In header chào mừng
    3. Thu thập thông tin: distance_m, diagonal_inch, is_adult, is_speech
    4. Lấy lời chào từ Gemini và phát TTS
    5. Test mắt trái → lưu kết quả
    6. Test mắt phải → lưu kết quả
    7. Tạo báo cáo tư vấn từ Gemini
    8. Hiển thị và đọc báo cáo
    """
    pygame.mixer.init()

    print("\n" + "="*60)
    print("CHƯƠNG TRÌNH KIỂM TRA THỊ LỰC SNELLEN")
    print("="*60)

    # Thu thập thông tin
    print("\nVui lòng nhập các thông tin sau:")

    # TODO: Thu thập thông tin với try-except để xử lý lỗi
    distance_m = float(input("Khoảng cách từ mắt đến màn hình (mét) [mặc định: 0.5]: ") or "0.5")

    # TODO: Lấy đường chéo màn hình (diagonal_inch) - mặc định 14.5 ?
    diagonal_inch = 0  # Thay đổi dòng này

    # TODO: Lấy đối tượng kiểm tra (1=Người lớn, 2=Trẻ nhỏ)
    # Gợi ý: Lấy input, so sánh == "1" để có boolean
    is_adult_input = ""  # Thay đổi dòng này
    is_adult = False  # Thay đổi dòng này

    # TODO: Lấy phương thức trả lời (1=Gõ phím, 2=Giọng nói)
    is_speech_input = ""  # Thay đổi dòng này
    is_speech = False  # Thay đổi dòng này

######################################################################################
    # TODO: Lấy lời chào từ Gemini AI
    # Gợi ý: welcome_msg = get_welcome_message(is_adult, distance_m)
    welcome_msg = ""  # Thay đổi dòng này

    # TODO: In lời chào và phát TTS
    # Gợi ý: print(f"\nTrợ lý AI: {welcome_msg}") và text_to_speech(welcome_msg)
    pass  # Thay đổi các dòng này
    pass

    print("\n" + "-"*60)
    input("\nNhấn Enter để bắt đầu...")

    # TODO: Test mắt trái và lưu kết quả
    # Gợi ý: left_result = test_eye("trái",....)
    left_result = ""  # Thay đổi dòng này

    # TODO: In kết quả mắt trái


    # TODO: Đợi người dùng sẵn sàng test mắt phải tương tự mắt trái left_result = test_eye("trái",....)


    # TODO: In kết quả mắt phải


    print("\n" + "="*60)
    print("ĐANG TẠO BÁO CÁO TƯ VẤN...")
    print("="*60)

    # TODO: Lấy báo cáo tư vấn từ Gemini
    # Gợi ý: get_final_consultation(.....)
    consultation = ""  # Thay đổi dòng này

    print(f"\nTƯ VẤN TỪ BÁC SĨ AI:\n")
    print(consultation)
    text_to_speech(consultation)


    print("\n" + "="*60)
    print("HOÀN THÀNH KIỂM TRA!")
    print("="*60)

def test_eye(eye_name, is_adult, is_speech, distance_m, diagonal_inch):
    """
    Test một mắt theo chuẩn Snellen

    Logic:
    - Chạy từng level (SNELLEN_DENOMS) từ dễ → khó
    - Mỗi level: Hỏi tối đa 5 câu
    - Nếu đúng >= 3/5: Qua level tiếp theo
    - Nếu đúng < 3/5: Dừng lại, trả về kết quả level trước

    Args:
        eye_name: "trái" hoặc "phải"
        is_adult: True = người lớn, False = trẻ nhỏ
        is_speech: True = dùng STT, False = gõ phím
        distance_m: Khoảng cách đến màn hình
        diagonal_inch: Đường chéo màn hình

    Returns:
        str: Kết quả Snellen (ví dụ: "20/40")
    """
    print(f"\n{'='*60}")
    print(f"KIỂM TRA MẮT {eye_name.upper()}")
    print("="*60)

    # TODO: Lấy hướng dẫn từ Gemini cho mắt này
    # Gợi ý: instruction = get_eye_test_instruction()
    instruction = ""  # Thay đổi dòng này

    # TODO: In hướng dẫn và phát TTS
    pass  # Thay đổi các dòng này
    pass

    # TODO: Đợi người dùng sẵn sàng
    pass  # Thay đổi dòng này

    # TODO: Khởi tạo các biến tracking
    current_level = 0
    max_level = len(SNELLEN_DENOMS) - 1
    correct_needed = 3
    max_attempts = 5

    # TODO: Vòng lặp qua từng level
    while False:  # Thay đổi điều kiện mức hiện tại nhỏ hơn mức cao nhất
        # TODO: Lấy mẫu số Snellen hiện tại
        denom = 0  # Thay đổi dòng này (gợi ý: list[index])

        # TODO: Tính kích thước ký tự cho level này
        size_info = 0 # (gợi ý: snellen_letter_size(...))

        # TODO: Lấy hướng dẫn level từ Gemini
        level_msg = ""  # get_level_instruction

        # TODO: In hướng dẫn và phát TTS
        pass  # Thay đổi các dòng này


        # TODO: Reset điểm cho level mới
        correct = 0 # số câu trả lời đúng
        attempts = 0 # số câu đã trả lời

        # TODO: Vòng lặp hỏi 5 câu
        while False:  # số câu đã trả lời < ....
            attempts += 1

            print(f"\n[Câu {attempts}/{max_attempts}]")

            # TODO: Kiểm tra là người lớn hay trẻ nhỏ
            if False:  # Thay đổi điều kiện (gợi ý: is_adult)
                # ===== TEST NGƯỜI LỚN - CHỮ CÁI =====
                # TODO: Random 1 chữ cái từ LETTERS
                letter = ""  # Thay đổi dòng này

                size_str = format_size_display(size_info)

                # TODO: In chữ cái với kích thước
                pass  # Thay đổi dòng này

                user_answer = get_user_input("Bạn nhìn thấy chữ gì?", is_speech)

                # TODO: Kiểm tra đúng/sai
                is_correct = False  # check_answer_match()

            else:
                # ===== TEST TRẺ NHỎ - BIỂU TƯỢNG =====
                symbol = random.choice(LEA_SYMBOLS)

                size_str = format_size_display(size_info)

                print(f"\n>>> {symbol['emoji']} {size_str}")

                print("\nLựa chọn:")
                for i, s in enumerate(LEA_SYMBOLS, 1):
                    print(f"{i}. {s['name']} {s['emoji']}")

                user_answer = get_user_input("Chọn số hoặc nói tên biểu tượng:", is_speech)


                # Xử lý câu trả lời
                if is_speech:
                    # Dùng AI kiểm tra câu trả lời giọng nói
                    is_correct = check_child_answer_with_ai(user_answer, symbol['name'])
                else:
                    # Kiểm tra số nhập vào
                    try:
                        idx = int(user_answer) - 1
                        if 0 <= idx < len(LEA_SYMBOLS):
                            is_correct = LEA_SYMBOLS[idx]['id'] == symbol['id']
                        else:
                            is_correct = False
                    except ValueError:
                        is_correct = False

            # TODO: Cập nhật điểm nếu đúng
            if False:  # Thay đổi điều kiện (gợi ý: is_correct)
                pass  # điểm + 1


            # TODO: Kiểm tra đủ điểm qua level chưa
            if False:  # Thay đổi điều kiện (gợi ý: correct >= correct_needed)
                print(f"\nĐạt {correct}/{attempts} - Chuyển sang mức khó hơn!")
                break

        # TODO: Kiểm tra có pass level không
        if False:  # Thay đổi điều kiện (gợi ý: correct < correct_needed)
            print(f"\nChỉ đúng {correct}/{attempts} - Dừng tại mức này.")

            # TODO: Tính toán kết quả cuối (level trước đó)
            # Gợi ý: Nếu current_level > 0 thì lấy level trước, nếu không thì 200
            final_denom = 200  # SNELLEN_DENOMS[....]
            return ""  # Thay đổi dòng này (gợi ý: f"20/{final_denom}")

        current_level += 1

    # Đạt level cao nhất
    return f"20/{SNELLEN_DENOMS[-1]}"

if __name__ == '__main__':
    main()
