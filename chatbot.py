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
    """Lời chào và hướng dẫn ban đầu"""
    mode = "người lớn" if is_adult else "trẻ nhỏ"
    messages = [
        ("system", "Bạn là trợ lý y tế thân thiện, hỗ trợ kiểm tra thị lực. Hãy nói ngắn gọn, rõ ràng và thân thiện."),
        ("human", f"Hãy chào và hướng dẫn {mode} ngồi cách màn hình {distance_m} chuẩn bị kiểm tra thị lực theo chuẩn Snellen. Hướng dẫn ngắn gọn trong 2-3 câu.")
    ]
    response = llm.invoke(messages)
    return str(response.content).replace("**","")

def get_eye_test_instruction(eye_name, is_adult):
    """Hướng dẫn trước khi test từng mắt"""
    mode = "chữ cái" if is_adult else "biểu tượng"
    messages = [
        ("system", "Bạn là trợ lý y tế thân thiện. Hãy nói ngắn gọn."),
        ("human", f"Hướng dẫn người dùng che mắt {'phải' if eye_name == 'trái' else 'trái'} để kiểm tra mắt {eye_name}. Sẽ hiển thị {mode} trên màn hình. Nói trong 1-2 câu.")
    ]
    response = llm.invoke(messages)
    return str(response.content).replace("**","")

def get_level_instruction(snellen_denom, is_adult):
    """Hướng dẫn cho mỗi level mới"""
    messages = [
        ("system", "Bạn là trợ lý y tế thân thiện. Hãy nói ngắn gọn."),
        ("human", f"Thông báo người dùng bắt đầu kiểm tra mức Snellen 20/{snellen_denom}. Khuyến khích họ. Nói trong 1 câu ngắn.")
    ]
    response = llm.invoke(messages)
    return str(response.content).replace("**","")

def get_feedback(is_correct, correct_count, total_count):
    """Phản hồi sau mỗi câu trả lời"""
    result = "đúng" if is_correct else "sai"
    messages = [
        ("system", "Bạn là trợ lý y tế thân thiện. Hãy khuyến khích người dùng bằng 1 câu ngắn."),
        ("human", f"Người dùng vừa trả lời {result}. Hiện tại đúng {correct_count}/{total_count} câu. Hãy phản hồi động viên ngắn gọn.")
    ]
    response = llm.invoke(messages)
    return str(response.content).replace("**","")

def check_child_answer_with_ai(user_answer, correct_symbol_name):
    """
    Dùng AI kiểm tra câu trả lời của trẻ nhỏ (có thể nói khác nhưng đúng ý nghĩa)

    Args:
        user_answer: Câu trả lời của trẻ (text từ STT)
        correct_symbol_name: Tên đúng của biểu tượng (ví dụ: "Nhà", "Táo")

    Returns:
        bool: True nếu đúng, False nếu sai
    """
    messages = [
        ("system", "Bạn là hệ thống đánh giá câu trả lời. Chỉ trả lời 'ĐÚNG' hoặc 'SAI'."),
        ("human", f"Đáp án đúng là: '{correct_symbol_name}'. Người dùng trả lời: '{user_answer}'. "
                  f"Nếu ý nghĩa giống nhau (ví dụ: 'căn nhà' ~ 'nhà', 'quả táo' ~ 'táo') thì trả lời ĐÚNG. "
                  f"Chỉ trả lời 1 từ: ĐÚNG hoặc SAI.")
    ]
    response = llm.invoke(messages)
    return "ĐÚNG" in str(response.content).replace("**","").upper()

def get_final_consultation(left_eye_result, right_eye_result):
    """
    Tư vấn cuối cùng dựa trên kết quả 2 mắt

    Args:
        left_eye_result: Kết quả mắt trái (ví dụ: "20/40")
        right_eye_result: Kết quả mắt phải (ví dụ: "20/30")

    Returns:
        str: Tư vấn chi tiết từ Gemini
    """
    messages = [
        ("system", "Bạn là bác sĩ nhãn khoa chuyên nghiệp. Hãy tư vấn chi tiết, dễ hiểu."),
        ("human", f"Kết quả kiểm tra thị lực Snellen:\n"
                  f"- Mắt trái: {left_eye_result}\n"
                  f"- Mắt phải: {right_eye_result}\n\n"
                  f"Hãy: đánh giá thị lực và đưa ra lời khuyên giúp tôi")
    ]
    response = llm.invoke(messages)
    return str(response.content).replace("**","")
