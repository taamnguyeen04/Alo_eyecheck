import math
import pyautogui
import random

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "K", "L", "M", "N", "P", "R", "T", "U", "V", "W", "X", "Y", "Z"]
LEA_SYMBOLS = [
    {"name": "Nhà", "emoji": "🏠", "id": "nha"},
    {"name": "Táo", "emoji": "🍎", "id": "tao"},
    {"name": "Vòng tròn", "emoji": "⚪", "id": "tron"},
    {"name": "Hình vuông", "emoji": "⬜", "id": "vuong"},
]
SNELLEN_DENOMS = [200, 100, 70, 50, 40, 30, 25, 20]  # từ dễ đến khó

def snellen_letter_size(snellen_denominator=40, distance_m=2.0, diagonal_inch=14.5):
    # Lấy thông tin màn hình
    width, height = pyautogui.size()
    diag_px = math.hypot(width, height)
    ppi = diag_px / diagonal_inch
    mm_per_inch = 25.4

    # 20 ft = 6.096 m, hằng số 0.00145 là góc nhìn 5 phút cung
    height_m = 0.00145 * (snellen_denominator * 0.3048) * (distance_m / 6.096)
    height_mm = height_m * 1000
    height_px = height_mm / mm_per_inch * ppi

    return {
        "height_mm": height_mm,
        "height_px": height_px,
        "ppi": ppi,
        "resolution": (width, height),
    }
def run_eye_test(mode="adult"):
    current_level = 0
    max_level = len(SNELLEN_DENOMS) - 1
    correct_needed = 3
    max_attempts = 5
    distance_m = 2.0
    diagonal_inch = 14.5

    while current_level <= max_level:
        denom = SNELLEN_DENOMS[current_level]
        size_info = snellen_letter_size(snellen_denominator=denom, distance_m=distance_m, diagonal_inch=diagonal_inch)
        print(
            f"\n=== Snellen 20/{denom}, cỡ ký hiệu: {size_info['height_mm']:.1f} mm / {size_info['height_px']:.1f} px ===")
        correct = 0
        attempts = 0

        while attempts < max_attempts:
            if mode == "adult":
                item = random.choice(LETTERS)
                print(f"Ký tự ngẫu nhiên: {item}")
                answer = input("Nhập ký tự bạn nhìn thấy: ").strip().upper()
                is_correct = (answer == item)
                if is_correct:
                    print("✅ Đúng")
                    correct += 1
                else:
                    print("❌ Sai. Đáp án là:", item)
            elif mode == "child":
                item = random.choice(LEA_SYMBOLS)
                # Cho trẻ nhìn emoji + 4 lựa chọn text
                options = random.sample(LEA_SYMBOLS, len(LEA_SYMBOLS))
                text_options = [f"{idx+1}. {o['name']}" for idx, o in enumerate(options)]
                print(f"Biểu tượng: {item['emoji']}")
                print("Chọn đáp án đúng:")
                for opt in text_options:
                    print(opt)
                answer = input("Nhập số thứ tự ký hiệu đúng: ").strip()
                try:
                    idx = int(answer) - 1
                except:
                    idx = -1
                is_correct = (idx >= 0 and options[idx]['id'] == item['id'])
                if is_correct:
                    print("✅ Đúng")
                    correct += 1
                else:
                    print(f"❌ Sai. Đáp án là: {item['name']}")
            else:
                raise ValueError("Chế độ không hợp lệ: 'adult' hoặc 'child'")
            attempts += 1
            if correct >= correct_needed:
                print(f"Đã đúng {correct}/{attempts} lần, tăng cấp kiểm tra lên khó hơn!")
                break

        if correct < correct_needed:
            print("Bạn chưa đạt tiêu chí vượt cấp. Kết thúc test ở mức này.")
            break
        current_level += 1

    print(f"\n==> Thị lực ước tính ở mức: 20/{SNELLEN_DENOMS[max(0, current_level - 1)]}")

if __name__ == "__main__":
    print("Chọn chế độ đo mắt:\n1. Người lớn biết chữ\n2. Trẻ nhỏ (không biết chữ, đo qua icon đơn giản)")
    mode_choice = input("Nhập số (1 hoặc 2): ").strip()
    if mode_choice == "1":
        run_eye_test(mode="adult")
    else:
        run_eye_test(mode="child")
