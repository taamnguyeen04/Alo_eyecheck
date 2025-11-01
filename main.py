from tts import text_to_speech
from stt import recognize_speech
from processing import snellen_letter_size, format_size_display, check_answer_match
from chatbot import (
    get_welcome_message, get_eye_test_instruction, get_level_instruction,
    get_feedback, check_child_answer_with_ai, get_final_consultation
)
import random
import pygame

# Constants
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "K", "L", "M", "N", "P", "R", "T", "U", "V", "W", "X", "Y", "Z"]
LEA_SYMBOLS = [
    {"name": "Nhà", "emoji": "🏠", "id": "nha"},
    {"name": "Táo", "emoji": "🍎", "id": "tao"},
    {"name": "Vòng tròn", "emoji": "⚪", "id": "tron"},
    {"name": "Hình vuông", "emoji": "⬜", "id": "vuong"},
]
SNELLEN_DENOMS = [200, 100, 70, 50, 40, 30, 25, 20]

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
    """Thu thập thông tin và khởi động chương trình"""
    pygame.mixer.init()

    print("\n" + "="*60)
    print("CHƯƠNG TRÌNH KIỂM TRA THỊ LỰC SNELLEN")
    print("="*60)

    # Thu thập thông tin
    print("\nVui lòng nhập các thông tin sau:")

    try:
        distance_m = float(input("Khoảng cách từ mắt đến màn hình (mét) [mặc định: 0.5]: ") or "0.5")
        diagonal_inch = float(input("Đường chéo màn hình (inch) [mặc định: 14.5]: ") or "14.5")

        is_adult_input = input("Đối tượng kiểm tra (1=Người lớn, 2=Trẻ nhỏ) [mặc định: 1]: ") or "1"
        is_adult = is_adult_input == "1"

        is_speech_input = input("Phương thức trả lời (1=Gõ phím, 2=Giọng nói) [mặc định: 1]: ") or "1"
        is_speech = is_speech_input == "2"

    except ValueError:
        print("Giá trị không hợp lệ, sử dụng mặc định.")
        distance_m = 0.5
        diagonal_inch = 14.5
        is_adult = True
        is_speech = False

    # Lời chào từ Gemini
    print("\n" + "-"*60)
    welcome_msg = get_welcome_message(is_adult, distance_m)
    print(f"\nTrợ lý AI: {welcome_msg}")
    text_to_speech(welcome_msg)

    print("\n" + "-"*60)
    input("\nNhấn Enter để bắt đầu...")

    # Test từng mắt
    left_result = test_eye("trái", is_adult, is_speech, distance_m, diagonal_inch)
    print(f"\nKết quả mắt trái: {left_result}")

    print("\n" + "="*60)
    input("Nhấn Enter để kiểm tra mắt phải...")

    right_result = test_eye("phải", is_adult, is_speech, distance_m, diagonal_inch)
    print(f"\nKết quả mắt phải: {right_result}")

    # Tư vấn cuối cùng
    print("\n" + "="*60)
    print("ĐANG TẠO BÁO CÁO TƯ VẤN...")
    print("="*60)

    consultation = get_final_consultation(left_result, right_result)
    print(f"\nTƯ VẤN TỪ BÁC SĨ AI:\n")
    print(consultation)
    text_to_speech(consultation)

    print("\n" + "="*60)
    print("HOÀN THÀNH KIỂM TRA!")
    print("="*60)

def test_eye(eye_name, is_adult, is_speech, distance_m, diagonal_inch):
    """
    Test một mắt theo chuẩn Snellen

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

    # Hướng dẫn từ Gemini
    instruction = get_eye_test_instruction(eye_name, is_adult)
    print(f"\nTrợ lý AI: {instruction}")
    text_to_speech(instruction)

    input("\nNhấn Enter khi đã sẵn sàng...")

    current_level = 0
    max_level = len(SNELLEN_DENOMS) - 1
    correct_needed = 3
    max_attempts = 5

    while current_level <= max_level:
        denom = SNELLEN_DENOMS[current_level]
        size_info = snellen_letter_size(denom, distance_m, diagonal_inch)

        # Hướng dẫn level mới
        print(f"\n{'─'*60}")
        level_msg = get_level_instruction(denom, is_adult)
        print(f"Trợ lý AI: {level_msg}")
        text_to_speech(level_msg)

        correct = 0
        attempts = 0

        while attempts < max_attempts:
            attempts += 1
            print(f"\n[Câu {attempts}/{max_attempts}]")

            if is_adult:
                # Test người lớn - chữ cái
                letter = random.choice(LETTERS)
                size_str = format_size_display(size_info)
                print(f"\n>>> {letter} {size_str}")

                user_answer = get_user_input("Bạn nhìn thấy chữ gì?", is_speech)
                is_correct = check_answer_match(user_answer, letter, is_symbol=False)

            else:
                # Test trẻ nhỏ - biểu tượng
                symbol = random.choice(LEA_SYMBOLS)
                size_str = format_size_display(size_info)
                print(f"\n>>> {symbol['emoji']} {size_str}")

                # Hiển thị lựa chọn
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

            # Cập nhật điểm
            if is_correct:
                correct += 1

            # Feedback từ Gemini
            # feedback = get_feedback(is_correct, correct, attempts)
            # print(feedback)
            # text_to_speech(feedback)

            # Kiểm tra đủ điểm qua level
            if correct >= correct_needed:
                print(f"\nĐạt {correct}/{attempts} - Chuyển sang mức khó hơn!")
                break

        # Kiểm tra có qua level không
        if correct < correct_needed:
            print(f"\nChỉ đúng {correct}/{attempts} - Dừng tại mức này.")
            final_denom = SNELLEN_DENOMS[max(0, current_level - 1)] if current_level > 0 else 200
            return f"20/{final_denom}"

        current_level += 1

    # Đạt level cao nhất
    return f"20/{SNELLEN_DENOMS[-1]}"

if __name__ == '__main__':
    main()
