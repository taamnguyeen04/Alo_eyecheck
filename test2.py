import math
import pyautogui

def snellen_letter_size(snellen_denominator=40, distance_m=2.0, diagonal_inch=14.5):
    # Lấy độ phân giải màn hình hiện tại
    width, height = pyautogui.size()
    diag_px = math.hypot(width, height)
    ppi = diag_px / diagonal_inch
    mm_per_inch = 25.4

    # Công thức Snellen: chiều cao chữ = D * 0.00145 (D tính bằng mét)
    denominator_m = snellen_denominator * 0.3048
    letter_height_m = denominator_m * 0.00145
    letter_height_mm = letter_height_m * 1000

    # Tỉ lệ khoảng cách
    scale = distance_m / denominator_m
    height_mm = letter_height_mm * scale

    # Quy đổi sang pixel
    height_px = height_mm / mm_per_inch * ppi

    return {
        "height_mm": height_mm,
        "height_px": height_px,
        "ppi": ppi,
        "resolution": (width, height),
    }

if __name__ == "__main__":
    result = snellen_letter_size(snellen_denominator=40, distance_m=2.0, diagonal_inch=14.5)
    print(f"Độ phân giải màn hình: {result['resolution'][0]}x{result['resolution'][1]}")
    print(f"PPI: {result['ppi']:.2f}")
    print(f"Chiều cao chữ 20/40 ở 2m: {result['height_mm']:.1f} mm ≈ {result['height_px']:.1f} px")
