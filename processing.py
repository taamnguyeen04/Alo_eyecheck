import math
import pyautogui

def snellen_letter_size(snellen_denominator=40, distance_m=2.0, diagonal_inch=14.5):
    """
    Tính kích thước ký tự theo công thức Snellen
    Args:
        snellen_denominator: Mẫu số Snellen (20, 25, 30, ...)
        distance_m: Khoảng cách từ mắt đến màn hình (mét)
        diagonal_inch: Đường chéo màn hình (inch)

    Returns:
        dict: {"height_mm": float, "height_px": float, "ppi": float}
    """
    # TODO: Lấy kích thước màn hình
    # Sử dụng pyautogui.size() để lấy width, height
    width, height = 0, 0  

    # TODO: Tính đường chéo màn hình theo pixel
    diag_px = 0  

    # TODO: Tính PPI (pixels per inch)
    ppi = 0  

    mm_per_inch = 25.4

    # TODO: Áp dụng công thức Snellen để tính chiều cao ký tự (đơn vị: mét)
    height_m = 0

    # TODO: Chuyển đổi sang milimét
    height_mm = 0

    # TODO: Chuyển đổi sang pixel
    height_px = 0

    return {
        "height_mm": round(height_mm, 1),
        "height_px": round(height_px, 1),
        "ppi": round(ppi, 1),
    }

def format_size_display(size_info):
    """
    Format hiển thị kích thước cho terminal
    Ví dụ: "(45.2px, 5.3mm)"

    Args:
        size_info: dict chứa height_px và height_mm

    Returns:
        str: Chuỗi format đẹp
    """
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
        # TODO: Với symbol, so sánh ID trực tiếp
        return False
    else:
        # TODO: Với chữ cái, so sánh không phân biệt hoa thường
        # Chuyển cả 2 về .upper() rồi so sánh
        return False
