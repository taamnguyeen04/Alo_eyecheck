from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Khởi tạo model Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def get_welcome_message(is_adult, distance_m):
    """
    Tạo lời chào và hướng dẫn ban đầu từ AI

    Hướng dẫn:
    - Tạo biến mode để xác định đối tượng: "người lớn" hoặc "trẻ nhỏ"
    - Tạo messages list với 2 phần tử tuple:
      + ("system", "prompt hệ thống - vai trò AI")
      + ("human", "câu hỏi cụ thể - nhớ dùng f-string để chèn mode và distance_m")
    - Gọi llm.invoke(messages) để lấy response
    - Return nội dung đã loại bỏ ký tự "**"

    Args:
        is_adult: True nếu người lớn, False nếu trẻ nhỏ
        distance_m: Khoảng cách ngồi (mét)

    Returns:
        str: Lời chào từ AI
    """
    # TODO: Xác định mode dựa vào is_adult
    # Gợi ý: Dùng toán tử if-else
    mode = ""  # Thay đổi dòng này

    # TODO: Tạo messages list
    # Gợi ý: [("system", "..."), ("human", "...")]
    messages = []  # Thay đổi dòng này

    # TODO: Gọi AI và lấy response
    # Gợi ý: llm.invoke(messages)
    response = None  # Thay đổi dòng này

    # TODO: Trả về nội dung đã xử lý
    # Gợi ý: str(response.content).replace("**","")
    return ""  # Thay đổi dòng này

def get_eye_test_instruction(eye_name, is_adult):
    """
    Tạo hướng dẫn trước khi test từng mắt

    Hướng dẫn tương tự get_welcome_message

    Args:
        eye_name: "trái" hoặc "phải"
        is_adult: True nếu người lớn, False nếu trẻ nhỏ

    Returns:
        str: Hướng dẫn từ AI
    """
    # TODO: Xác định mode (chữ cái hay biểu tượng)
    mode = ""  # Thay đổi dòng này

    # TODO: Tạo messages - hướng dẫn che mắt đối diện
    # Gợi ý: Nếu test mắt trái thì che mắt phải và ngược lại
    messages = []  # Thay đổi dòng này

    # TODO: Gọi AI và return kết quả
    return ""  # Thay đổi dòng này

def get_level_instruction(snellen_denom, is_adult):
    """
    Tạo hướng dẫn cho mỗi level mới

    Args:
        snellen_denom: Mẫu số Snellen (200, 100, 70, ...)
        is_adult: True nếu người lớn, False nếu trẻ nhỏ

    Returns:
        str: Hướng dẫn level từ AI
    """
    # TODO: Tạo messages thông báo level mới
    # Gợi ý: f"Thông báo người dùng bắt đầu kiểm tra mức Snellen 20/{snellen_denom}. Khuyến khích họ."
    messages = []  # Thay đổi dòng này

    # TODO: Gọi AI và return
    return ""  # Thay đổi dòng này

def get_feedback(is_correct, correct_count, total_count):
    """
    Tạo phản hồi động viên sau mỗi câu trả lời

    Args:
        is_correct: True nếu đúng, False nếu sai
        correct_count: Số câu đúng hiện tại
        total_count: Tổng số câu đã trả lời

    Returns:
        str: Feedback từ AI
    """
    # TODO: Xác định kết quả ("đúng" hay "sai")
    result = ""  # Thay đổi dòng này

    # TODO: Tạo messages yêu cầu AI phản hồi động viên
    messages = []  # Thay đổi dòng này

    # TODO: Gọi AI và return
    return ""  # Thay đổi dòng này

def check_child_answer_with_ai(user_answer, correct_symbol_name):
    """
    Dùng AI kiểm tra câu trả lời của trẻ nhỏ (chấp nhận nhiều cách nói)

    Ví dụ: "căn nhà" = "nhà", "quả táo" = "táo"

    Args:
        user_answer: Câu trả lời của trẻ (text từ STT)
        correct_symbol_name: Tên đúng của biểu tượng (ví dụ: "Nhà", "Táo")

    Returns:
        bool: True nếu đúng, False nếu sai
    """
    # TODO: Tạo messages yêu cầu AI đánh giá
    # Gợi ý: System prompt: "Chỉ trả lời 'ĐÚNG' hoặc 'SAI'"
    #        Human prompt: So sánh user_answer với correct_symbol_name
    messages = []  # Thay đổi dòng này

    # TODO: Gọi AI
    response = None  # Thay đổi dòng này

    # TODO: Kiểm tra xem response có chứa "ĐÚNG" không
    # Gợi ý: "ĐÚNG" in str(response.content).upper()
    return False  # Thay đổi dòng này

def get_final_consultation(left_eye_result, right_eye_result):
    """
    Tạo báo cáo tư vấn cuối cùng từ AI

    Yêu cầu AI:
    1. Đánh giá tình trạng thị lực
    2. So sánh với tiêu chuẩn 20/20
    3. Khuyến nghị có cần khám bác sĩ không
    4. Lời khuyên chăm sóc mắt

    Args:
        left_eye_result: Kết quả mắt trái (ví dụ: "20/40")
        right_eye_result: Kết quả mắt phải (ví dụ: "20/30")

    Returns:
        str: Tư vấn chi tiết từ AI
    """
    # TODO: Tạo messages với system prompt là "bác sĩ nhãn khoa chuyên nghiệp"
    # Human prompt cần bao gồm:
    # - Kết quả 2 mắt
    # - 4 yêu cầu ở trên
    messages = []  # Thay đổi dòng này

    # TODO: Gọi AI và return kết quả
    return ""  # Thay đổi dòng này
