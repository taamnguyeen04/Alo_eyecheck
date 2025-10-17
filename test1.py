# physical_screen_size.py
import math
import pyautogui

def physical_size_from_pixels(px_w: int, px_h: int, diag_inch: float):
    """
    Trả về (width_inch, height_inch, ppi)
    """
    diag_px = math.hypot(px_w, px_h)         # đường chéo theo pixel
    if diag_inch <= 0:
        raise ValueError("diag_inch phải > 0")
    ppi = diag_px / diag_inch                # pixels per inch
    width_in = px_w / ppi
    height_in = px_h / ppi
    return width_in, height_in, ppi

if __name__ == "__main__":
    # Lấy độ phân giải màn hình hiện tại (pixel)
    width_px, height_px = pyautogui.size()
    # Nếu bạn muốn dùng độ phân giải thủ công, thay  width_px/height_px bằng số bạn muốn

    # Đổi ở đây nếu bạn muốn dùng đường chéo khác
    diagonal_inch = 14.5

    w_in, h_in, ppi = physical_size_from_pixels(width_px, height_px, diagonal_inch)
    mm_per_inch = 25.4
    w_mm = w_in * mm_per_inch
    h_mm = h_in * mm_per_inch
    pixel_pitch_mm = mm_per_inch / ppi  # kích thước 1 pixel theo mm

    print(f"Pixel resolution: {width_px} x {height_px}")
    print(f"Diagonal (reported): {diagonal_inch:.2f} in")
    print()
    print(f"Physical width : {w_in:.3f} in  / {w_mm:.1f} mm")
    print(f"Physical height: {h_in:.3f} in  / {h_mm:.1f} mm")
    print(f"PPI (pixels per inch): {ppi:.2f}")
    print(f"Pixel pitch (size of one pixel): {pixel_pitch_mm:.3f} mm")
