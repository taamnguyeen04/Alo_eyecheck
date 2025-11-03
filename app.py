import tkinter as tk
from tkinter import ttk, messagebox
import threading
import pygame
from tts import text_to_speech
from stt import recognize_speech
from processing import snellen_letter_size, format_size_display, check_answer_match
from chatbot import (
    get_welcome_message, get_eye_test_instruction, get_level_instruction,
    get_feedback, check_child_answer_with_ai, get_final_consultation
)
import random

# Constants
LETTERS = ["A", "B", "C", "D", "E", "G", "H", "K", "L", "M", "N", "R", "T", "U", "V", "X", "Y", "Z"]
LEA_SYMBOLS = [
    {"name": "Nhà", "emoji": "🏠", "id": "nha"},
    {"name": "Táo", "emoji": "🍎", "id": "tao"},
    {"name": "Vòng tròn", "emoji": "⚪", "id": "tron"},
    {"name": "Hình vuông", "emoji": "⬜", "id": "vuong"},
]
SNELLEN_DENOMS = [200, 100, 70, 50, 40, 30, 25, 20]

# Colors
COLOR_PRIMARY = "#2c3e50"
COLOR_SECONDARY = "#3498db"
COLOR_SUCCESS = "#27ae60"
COLOR_DANGER = "#e74c3c"
COLOR_LIGHT = "#ecf0f1"
COLOR_WHITE = "#ffffff"
COLOR_TEXT = "#2c3e50"

class EyeTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kiểm Tra Thị Lực Snellen")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLOR_LIGHT)

        # Initialize pygame mixer
        pygame.mixer.init()

        # State variables
        self.distance_m = tk.DoubleVar(value=0.5)
        self.diagonal_inch = tk.DoubleVar(value=14.5)
        self.is_adult = tk.BooleanVar(value=True)
        self.is_speech = tk.BooleanVar(value=False)

        self.current_eye = None  # "trái" or "phải"
        self.left_result = None
        self.right_result = None
        self.current_level = 0
        self.correct_count = 0
        self.attempt_count = 0
        self.current_item = None
        self.is_listening = False

        # Show welcome screen
        self.show_welcome_screen()

    def clear_screen(self):
        """Xóa tất cả widgets trên màn hình"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        """Màn hình chào mừng"""
        self.clear_screen()

        frame = tk.Frame(self.root, bg=COLOR_LIGHT)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title = tk.Label(
            frame,
            text="👁️ KIỂM TRA THỊ LỰC",
            font=("Arial", 48, "bold"),
            bg=COLOR_LIGHT,
            fg=COLOR_PRIMARY
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            frame,
            text="Chuẩn Snellen với hỗ trợ AI",
            font=("Arial", 20),
            bg=COLOR_LIGHT,
            fg=COLOR_SECONDARY
        )
        subtitle.pack(pady=10)

        # Start button
        start_btn = tk.Button(
            frame,
            text="BẮT ĐẦU",
            font=("Arial", 20, "bold"),
            bg=COLOR_SUCCESS,
            fg=COLOR_WHITE,
            padx=50,
            pady=20,
            border=0,
            cursor="hand2",
            command=self.show_setup_screen
        )
        start_btn.pack(pady=40)

        # Credits
        # credits = tk.Label(
        #     frame,
        #     text="Powered by Gemini AI",
        #     font=("Arial", 12),
        #     bg=COLOR_LIGHT,
        #     fg=COLOR_TEXT
        # )
        # credits.pack(pady=10)

    def show_setup_screen(self):
        """Màn hình cài đặt thông tin"""
        self.clear_screen()

        # Main container
        container = tk.Frame(self.root, bg=COLOR_LIGHT)
        container.pack(expand=True, fill="both", padx=50, pady=50)

        # Title
        title = tk.Label(
            container,
            text="⚙️ THIẾT LẬP",
            font=("Arial", 36, "bold"),
            bg=COLOR_LIGHT,
            fg=COLOR_PRIMARY
        )
        title.pack(pady=20)

        # Form frame
        form_frame = tk.Frame(container, bg=COLOR_WHITE, padx=40, pady=40)
        form_frame.pack(pady=20)

        # Distance
        tk.Label(
            form_frame,
            text="Khoảng cách đến màn hình (mét):",
            font=("Arial", 14),
            bg=COLOR_WHITE,
            fg=COLOR_TEXT
        ).grid(row=0, column=0, sticky="w", pady=10)

        distance_entry = tk.Entry(
            form_frame,
            textvariable=self.distance_m,
            font=("Arial", 14),
            width=20
        )
        distance_entry.grid(row=0, column=1, padx=20, pady=10)

        # Diagonal
        tk.Label(
            form_frame,
            text="Đường chéo màn hình (inch):",
            font=("Arial", 14),
            bg=COLOR_WHITE,
            fg=COLOR_TEXT
        ).grid(row=1, column=0, sticky="w", pady=10)

        diagonal_entry = tk.Entry(
            form_frame,
            textvariable=self.diagonal_inch,
            font=("Arial", 14),
            width=20
        )
        diagonal_entry.grid(row=1, column=1, padx=20, pady=10)

        # Age group
        tk.Label(
            form_frame,
            text="Đối tượng kiểm tra:",
            font=("Arial", 14),
            bg=COLOR_WHITE,
            fg=COLOR_TEXT
        ).grid(row=2, column=0, sticky="w", pady=10)

        age_frame = tk.Frame(form_frame, bg=COLOR_WHITE)
        age_frame.grid(row=2, column=1, sticky="w", padx=20, pady=10)

        tk.Radiobutton(
            age_frame,
            text="Người lớn",
            variable=self.is_adult,
            value=True,
            font=("Arial", 12),
            bg=COLOR_WHITE
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            age_frame,
            text="Trẻ nhỏ",
            variable=self.is_adult,
            value=False,
            font=("Arial", 12),
            bg=COLOR_WHITE
        ).pack(side="left", padx=10)

        # Input method
        tk.Label(
            form_frame,
            text="Phương thức trả lời:",
            font=("Arial", 14),
            bg=COLOR_WHITE,
            fg=COLOR_TEXT
        ).grid(row=3, column=0, sticky="w", pady=10)

        method_frame = tk.Frame(form_frame, bg=COLOR_WHITE)
        method_frame.grid(row=3, column=1, sticky="w", padx=20, pady=10)

        tk.Radiobutton(
            method_frame,
            text="Gõ phím",
            variable=self.is_speech,
            value=False,
            font=("Arial", 12),
            bg=COLOR_WHITE
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            method_frame,
            text="Giọng nói",
            variable=self.is_speech,
            value=True,
            font=("Arial", 12),
            bg=COLOR_WHITE
        ).pack(side="left", padx=10)

        # Start button
        start_btn = tk.Button(
            container,
            text="BẮT ĐẦU KIỂM TRA",
            font=("Arial", 18, "bold"),
            bg=COLOR_SUCCESS,
            fg=COLOR_WHITE,
            padx=40,
            pady=15,
            border=0,
            cursor="hand2",
            command=self.start_test
        )
        start_btn.pack(pady=30)

    def start_test(self):
        """Bắt đầu test - hiển thị lời chào từ AI"""
        self.clear_screen()

        # Loading frame
        frame = tk.Frame(self.root, bg=COLOR_LIGHT)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        loading = tk.Label(
            frame,
            text="🤖 Đang tải trợ lý AI...",
            font=("Arial", 24),
            bg=COLOR_LIGHT,
            fg=COLOR_PRIMARY
        )
        loading.pack()

        # Get welcome message in background
        def load_welcome():
            try:
                msg = get_welcome_message(self.is_adult.get(), self.distance_m.get())
                self.root.after(0, lambda: self.show_instruction_screen(msg, "left"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Không thể kết nối AI: {e}"))
                self.root.after(0, self.show_setup_screen)

        threading.Thread(target=load_welcome, daemon=True).start()

    def show_instruction_screen(self, message, eye):
        """Hiển thị hướng dẫn từ AI"""
        self.clear_screen()
        self.current_eye = "trái" if eye == "left" else "phải"

        frame = tk.Frame(self.root, bg=COLOR_LIGHT)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # AI Icon
        icon = tk.Label(
            frame,
            text="🤖",
            font=("Arial", 80),
            bg=COLOR_LIGHT
        )
        icon.pack(pady=20)

        # Message
        msg_label = tk.Label(
            frame,
            text=message,
            font=("Arial", 18),
            bg=COLOR_LIGHT,
            fg=COLOR_TEXT,
            wraplength=800,
            justify="center"
        )
        msg_label.pack(pady=20)

        # Continue button
        continue_btn = tk.Button(
            frame,
            text="TIẾP TỤC",
            font=("Arial", 16, "bold"),
            bg=COLOR_SECONDARY,
            fg=COLOR_WHITE,
            padx=40,
            pady=15,
            border=0,
            cursor="hand2",
            command=lambda: self.start_eye_test(eye)
        )
        continue_btn.pack(pady=30)

        # Play TTS
        threading.Thread(target=lambda: text_to_speech(message), daemon=True).start()

    def start_eye_test(self, eye):
        """Bắt đầu test một mắt"""
        self.current_eye = "trái" if eye == "left" else "phải"
        self.current_level = 0
        self.correct_count = 0
        self.attempt_count = 0

        # Get instruction
        def load_instruction():
            try:
                instruction = get_eye_test_instruction(self.current_eye, self.is_adult.get())
                self.root.after(0, lambda: self.show_eye_instruction(instruction))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi AI: {e}"))

        threading.Thread(target=load_instruction, daemon=True).start()

    def show_eye_instruction(self, instruction):
        """Hiển thị hướng dẫn trước khi test mắt"""
        self.clear_screen()

        frame = tk.Frame(self.root, bg=COLOR_LIGHT)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Eye icon
        eye_icon = "👁️" if self.current_eye == "trái" else "👁️"
        icon = tk.Label(
            frame,
            text=eye_icon,
            font=("Arial", 100),
            bg=COLOR_LIGHT
        )
        icon.pack(pady=20)

        # Title
        title = tk.Label(
            frame,
            text=f"KIỂM TRA MẮT {self.current_eye.upper()}",
            font=("Arial", 32, "bold"),
            bg=COLOR_LIGHT,
            fg=COLOR_PRIMARY
        )
        title.pack(pady=10)

        # Instruction
        inst_label = tk.Label(
            frame,
            text=instruction,
            font=("Arial", 16),
            bg=COLOR_LIGHT,
            fg=COLOR_TEXT,
            wraplength=800,
            justify="center"
        )
        inst_label.pack(pady=20)

        # Ready button
        ready_btn = tk.Button(
            frame,
            text="SẴN SÀNG",
            font=("Arial", 18, "bold"),
            bg=COLOR_SUCCESS,
            fg=COLOR_WHITE,
            padx=50,
            pady=20,
            border=0,
            cursor="hand2",
            command=self.show_test_screen
        )
        ready_btn.pack(pady=30)

        # Play TTS
        threading.Thread(target=lambda: text_to_speech(instruction), daemon=True).start()

    def show_test_screen(self):
        """Màn hình test - hiển thị ký tự/biểu tượng"""
        if self.current_level >= len(SNELLEN_DENOMS):
            # Hoàn thành test mắt này
            result = f"20/{SNELLEN_DENOMS[-1]}"
            if self.current_eye == "trái":
                self.left_result = result
                # Chuyển sang mắt phải
                def load_next():
                    try:
                        msg = f"Hoàn thành mắt trái! Kết quả: {result}. Chuẩn bị kiểm tra mắt phải."
                        text_to_speech(msg)
                        self.root.after(2000, lambda: self.show_instruction_screen(msg, "right"))
                    except:
                        pass
                threading.Thread(target=load_next, daemon=True).start()
            else:
                self.right_result = result
                self.show_result_screen()
            return

        # Check if level failed
        if self.attempt_count >= 5 and self.correct_count < 3:
            result_denom = SNELLEN_DENOMS[max(0, self.current_level - 1)] if self.current_level > 0 else 200
            result = f"20/{result_denom}"

            if self.current_eye == "trái":
                self.left_result = result
                # Chuyển sang mắt phải
                def load_next():
                    try:
                        msg = f"Hoàn thành mắt trái! Kết quả: {result}. Chuẩn bị kiểm tra mắt phải."
                        text_to_speech(msg)
                        self.root.after(2000, lambda: self.show_instruction_screen(msg, "right"))
                    except:
                        pass
                threading.Thread(target=load_next, daemon=True).start()
            else:
                self.right_result = result
                self.show_result_screen()
            return

        # Check if passed level
        if self.correct_count >= 3:
            self.current_level += 1
            self.correct_count = 0
            self.attempt_count = 0

            if self.current_level >= len(SNELLEN_DENOMS):
                result = f"20/{SNELLEN_DENOMS[-1]}"
                if self.current_eye == "trái":
                    self.left_result = result
                    def load_next():
                        try:
                            msg = f"Hoàn thành mắt trái! Kết quả: {result}. Chuẩn bị kiểm tra mắt phải."
                            text_to_speech(msg)
                            self.root.after(2000, lambda: self.show_instruction_screen(msg, "right"))
                        except:
                            pass
                    threading.Thread(target=load_next, daemon=True).start()
                else:
                    self.right_result = result
                    self.show_result_screen()
                return

        self.clear_screen()

        # Get current level info
        denom = SNELLEN_DENOMS[self.current_level]
        size_info = snellen_letter_size(denom, self.distance_m.get(), self.diagonal_inch.get())

        # Header
        header = tk.Frame(self.root, bg=COLOR_PRIMARY)
        header.pack(fill="x")

        header_text = tk.Label(
            header,
            text=f"Mắt {self.current_eye} | Snellen 20/{denom} | Câu {self.attempt_count + 1}/5 | Đúng: {self.correct_count}/3",
            font=("Arial", 16, "bold"),
            bg=COLOR_PRIMARY,
            fg=COLOR_WHITE,
            pady=15
        )
        header_text.pack()

        # Main display frame
        display_frame = tk.Frame(self.root, bg=COLOR_WHITE)
        display_frame.pack(expand=True, fill="both")

        # Generate item
        if self.is_adult.get():
            self.current_item = random.choice(LETTERS)
            item_text = self.current_item
        else:
            self.current_item = random.choice(LEA_SYMBOLS)
            item_text = self.current_item['emoji']

        # Display item with calculated size
        item_label = tk.Label(
            display_frame,
            text=item_text,
            font=("Arial", int(size_info['height_px'])),
            bg=COLOR_WHITE,
            fg=COLOR_TEXT
        )
        item_label.pack(expand=True)

        # Size info
        size_label = tk.Label(
            display_frame,
            text=format_size_display(size_info),
            font=("Arial", 12),
            bg=COLOR_WHITE,
            fg=COLOR_TEXT
        )
        size_label.pack(pady=10)

        # Input frame
        input_frame = tk.Frame(self.root, bg=COLOR_LIGHT, pady=20)
        input_frame.pack(fill="x")

        if not self.is_adult.get():
            # Show options for children
            options_frame = tk.Frame(input_frame, bg=COLOR_LIGHT)
            options_frame.pack(pady=10)

            for i, symbol in enumerate(LEA_SYMBOLS, 1):
                btn = tk.Button(
                    options_frame,
                    text=f"{i}. {symbol['name']} {symbol['emoji']}",
                    font=("Arial", 14),
                    bg=COLOR_WHITE,
                    fg=COLOR_TEXT,
                    padx=20,
                    pady=10,
                    cursor="hand2",
                    command=lambda s=symbol: self.submit_answer(s['id'] if self.is_adult.get() else str(LEA_SYMBOLS.index(s) + 1))
                )
                btn.pack(side="left", padx=10)

        # Input entry
        if self.is_speech.get():
            listen_btn = tk.Button(
                input_frame,
                text="🎤 NHẤN ĐỂ NÓI",
                font=("Arial", 16, "bold"),
                bg=COLOR_DANGER,
                fg=COLOR_WHITE,
                padx=30,
                pady=15,
                border=0,
                cursor="hand2",
                command=self.start_listening
            )
            listen_btn.pack()
        else:
            entry_container = tk.Frame(input_frame, bg=COLOR_LIGHT)
            entry_container.pack()

            answer_entry = tk.Entry(
                entry_container,
                font=("Arial", 16),
                width=20
            )
            answer_entry.pack(side="left", padx=10)
            answer_entry.focus()

            submit_btn = tk.Button(
                entry_container,
                text="GỬI",
                font=("Arial", 14, "bold"),
                bg=COLOR_SUCCESS,
                fg=COLOR_WHITE,
                padx=30,
                pady=10,
                border=0,
                cursor="hand2",
                command=lambda: self.submit_answer(answer_entry.get())
            )
            submit_btn.pack(side="left")

            answer_entry.bind("<Return>", lambda e: self.submit_answer(answer_entry.get()))

    def start_listening(self):
        """Bắt đầu lắng nghe giọng nói"""
        if self.is_listening:
            return

        self.is_listening = True

        def listen():
            try:
                answer = recognize_speech()
                self.root.after(0, lambda: self.submit_answer(answer))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Không nhận diện được: {e}"))
            finally:
                self.is_listening = False

        threading.Thread(target=listen, daemon=True).start()

    def submit_answer(self, user_answer):
        """Xử lý câu trả lời"""
        if not user_answer:
            return

        self.attempt_count += 1

        # Check answer
        if self.is_adult.get():
            is_correct = check_answer_match(user_answer, self.current_item, is_symbol=False)
        else:
            if self.is_speech.get():
                # Use AI for children speech
                is_correct = check_child_answer_with_ai(user_answer, self.current_item['name'])
            else:
                # Check number input
                try:
                    idx = int(user_answer) - 1
                    is_correct = (0 <= idx < len(LEA_SYMBOLS) and LEA_SYMBOLS[idx]['id'] == self.current_item['id'])
                except:
                    is_correct = False

        if is_correct:
            self.correct_count += 1

        # Get feedback
        def get_and_show_feedback():
            try:
                feedback = get_feedback(is_correct, self.correct_count, self.attempt_count)
                self.root.after(0, lambda: self.show_feedback(feedback, is_correct))
            except:
                self.root.after(0, lambda: self.show_feedback(
                    "Tốt lắm!" if is_correct else "Tiếp tục cố gắng!",
                    is_correct
                ))

        threading.Thread(target=get_and_show_feedback, daemon=True).start()

    def show_feedback(self, message, is_correct):
        """Hiển thị feedback"""
        # Show popup
        color = COLOR_SUCCESS if is_correct else COLOR_DANGER
        icon = "✅" if is_correct else "❌"

        # Create overlay
        overlay = tk.Toplevel(self.root)
        overlay.title("")
        overlay.geometry("400x200")
        overlay.configure(bg=color)
        overlay.transient(self.root)
        overlay.grab_set()

        # Center the window
        overlay.update_idletasks()
        x = (overlay.winfo_screenwidth() // 2) - (overlay.winfo_width() // 2)
        y = (overlay.winfo_screenheight() // 2) - (overlay.winfo_height() // 2)
        overlay.geometry(f"+{x}+{y}")

        icon_label = tk.Label(
            overlay,
            text=icon,
            font=("Arial", 60),
            bg=color,
            fg=COLOR_WHITE
        )
        icon_label.pack(pady=20)

        msg_label = tk.Label(
            overlay,
            text=message,
            font=("Arial", 14),
            bg=color,
            fg=COLOR_WHITE,
            wraplength=350
        )
        msg_label.pack(pady=10)

        # Play TTS
        threading.Thread(target=lambda: text_to_speech(message), daemon=True).start()

        # Auto close after 2 seconds
        self.root.after(2000, lambda: self.close_feedback_and_continue(overlay))

    def close_feedback_and_continue(self, overlay):
        """Đóng feedback và tiếp tục"""
        overlay.destroy()
        self.show_test_screen()

    def show_result_screen(self):
        """Màn hình kết quả cuối cùng"""
        self.clear_screen()

        # Loading
        frame = tk.Frame(self.root, bg=COLOR_LIGHT)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        loading = tk.Label(
            frame,
            text="🤖 Đang tạo báo cáo tư vấn...",
            font=("Arial", 24),
            bg=COLOR_LIGHT,
            fg=COLOR_PRIMARY
        )
        loading.pack()

        # Get consultation
        def get_consultation():
            try:
                consultation = get_final_consultation(self.left_result, self.right_result)
                self.root.after(0, lambda: self.display_result(consultation))
            except Exception as e:
                self.root.after(0, lambda: self.display_result(f"Không thể tạo báo cáo: {e}"))

        threading.Thread(target=get_consultation, daemon=True).start()

    def display_result(self, consultation):
        """Hiển thị kết quả"""
        self.clear_screen()

        # Container
        container = tk.Frame(self.root, bg=COLOR_LIGHT)
        container.pack(expand=True, fill="both", padx=50, pady=30)

        # Title
        title = tk.Label(
            container,
            text="📊 KẾT QUẢ KIỂM TRA",
            font=("Arial", 36, "bold"),
            bg=COLOR_LIGHT,
            fg=COLOR_PRIMARY
        )
        title.pack(pady=20)

        # Results frame
        results_frame = tk.Frame(container, bg=COLOR_WHITE, padx=30, pady=20)
        results_frame.pack(fill="x", pady=10)

        result_text = f"👁️ Mắt trái: {self.left_result}     👁️ Mắt phải: {self.right_result}"
        result_label = tk.Label(
            results_frame,
            text=result_text,
            font=("Arial", 20, "bold"),
            bg=COLOR_WHITE,
            fg=COLOR_PRIMARY
        )
        result_label.pack()

        # Consultation frame
        consult_frame = tk.Frame(container, bg=COLOR_WHITE, padx=30, pady=30)
        consult_frame.pack(fill="both", expand=True, pady=10)

        consult_title = tk.Label(
            consult_frame,
            text="🤖 TƯ VẤN TỪ BÁC SĨ AI",
            font=("Arial", 18, "bold"),
            bg=COLOR_WHITE,
            fg=COLOR_SECONDARY
        )
        consult_title.pack(pady=10)

        # Scrollable text
        text_frame = tk.Frame(consult_frame, bg=COLOR_WHITE)
        text_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        consult_text = tk.Text(
            text_frame,
            font=("Arial", 14),
            bg=COLOR_WHITE,
            fg=COLOR_TEXT,
            wrap="word",
            yscrollcommand=scrollbar.set,
            padx=20,
            pady=20
        )
        consult_text.pack(fill="both", expand=True)
        consult_text.insert("1.0", consultation)
        consult_text.config(state="disabled")
        scrollbar.config(command=consult_text.yview)

        # Buttons
        btn_frame = tk.Frame(container, bg=COLOR_LIGHT)
        btn_frame.pack(pady=20)

        restart_btn = tk.Button(
            btn_frame,
            text="🔄 KIỂM TRA LẠI",
            font=("Arial", 14, "bold"),
            bg=COLOR_SECONDARY,
            fg=COLOR_WHITE,
            padx=30,
            pady=15,
            border=0,
            cursor="hand2",
            command=self.show_welcome_screen
        )
        restart_btn.pack(side="left", padx=10)

        exit_btn = tk.Button(
            btn_frame,
            text="❌ THOÁT",
            font=("Arial", 14, "bold"),
            bg=COLOR_DANGER,
            fg=COLOR_WHITE,
            padx=30,
            pady=15,
            border=0,
            cursor="hand2",
            command=self.root.quit
        )
        exit_btn.pack(side="left", padx=10)

        # Play TTS
        threading.Thread(target=lambda: text_to_speech(consultation), daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = EyeTestApp(root)
    root.mainloop()
