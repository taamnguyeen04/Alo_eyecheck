import math
import pyautogui

def snellen_letter_size(snellen_denominator=40, distance_m=2.0, diagonal_inch=14.5):
    """
    Tính kích thước kí tự theo công thức Snellen

    Args:
        snellen_denominator: Mẫu số Snellen (20, 25, 30, ...)
        distance_m: Khoảng cách từ mắt đến màn hình (mét)
        diagonal_inch: đường chéo màn hình (inch)

    Returns:
        dict: Chứa height_mm, height_px, ppi
    """
    width, height = pyautogui.size()
    diag_px = math.hypot(width, height)
    ppi = diag_px / diagonal_inch
    mm_per_inch = 25.4

    # Công thức Snellen
    height_m = 0.00145 * (snellen_denominator * 0.3048) * (distance_m / 6.096)
    height_mm = height_m * 1000
    height_px = height_mm / mm_per_inch * ppi

    return {
        "height_mm": round(height_mm, 1),
        "height_px": round(height_px, 1),
        "ppi": round(ppi, 1),
    }

def format_size_display(size_info):
    """Format hiển thị kích thước cho terminal"""
    return f"({size_info['height_px']}px, {size_info['height_mm']}mm)"

def check_answer_match(user_answer, correct_answer, is_symbol=False):
    """
    Kiểm tra câu trả lời có khớp không

    Args:
        user_answer: Câu trả lời người dùng
        correct_answer: Đáp án đúng
        is_symbol: True nếu là symbol (trẻ nhỏ), False nếu là chữ cái

    Returns:
        bool: True nếu đúng, False nếu sai
    """
    if is_symbol:
        # Với symbol, so sánh ID
        return user_answer == correct_answer
    else:
        # Với chữ cái, so sánh không phân biệt hoa thường
        return user_answer.upper() == correct_answer.upper()
