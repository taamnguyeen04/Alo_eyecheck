import math
import random
import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
import pyautogui

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "K", "L", "M", "N", "P", "R", "T", "U", "V", "W", "X", "Y", "Z"]
LEA_SYMBOLS = [
    {"name": "Nhà", "emoji": "🏠", "id": "nha"},
    {"name": "Táo", "emoji": "🍎", "id": "tao"},
    {"name": "Vòng tròn", "emoji": "⚪", "id": "tron"},
    {"name": "Hình vuông", "emoji": "⬜", "id": "vuong"},
]
SNELLEN_DENOMS = [200, 100, 70, 50, 40, 30, 25, 20]


class EyeTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Đo Thị Lực")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Biến lưu trữ
        self.diagonal_inch = tk.DoubleVar(value=14.5)
        self.distance_m = tk.DoubleVar(value=2.0)
        self.mode = tk.StringVar(value="adult")
        self.input_method = tk.StringVar(value="keyboard")

        # Biến test
        self.current_level = 0
        self.correct = 0
        self.attempts = 0
        self.current_item = None
        self.current_options = []

        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Màn hình chào mừng và cài đặt"""
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        # Tiêu đề
        title = tk.Label(
            main_frame,
            text="🔍 ỨNG DỤNG ĐO THỊ LỰC",
            font=("Arial", 28, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title.pack(pady=(0, 30))

        # Frame cài đặt
        settings_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ Cài đặt",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#34495e",
            padx=30,
            pady=20
        )
        settings_frame.pack(fill="x", pady=10)

        # Kích thước màn hình
        screen_frame = tk.Frame(settings_frame, bg="white")
        screen_frame.pack(fill="x", pady=10)
        tk.Label(
            screen_frame,
            text="📺 Kích thước màn hình (inch):",
            font=("Arial", 12),
            bg="white"
        ).pack(side="left", padx=(0, 10))
        screen_entry = ttk.Entry(screen_frame, textvariable=self.diagonal_inch, width=10, font=("Arial", 11))
        screen_entry.pack(side="left")

        # Khoảng cách
        distance_frame = tk.Frame(settings_frame, bg="white")
        distance_frame.pack(fill="x", pady=10)
        tk.Label(
            distance_frame,
            text="📏 Khoảng cách đến màn hình (m):",
            font=("Arial", 12),
            bg="white"
        ).pack(side="left", padx=(0, 10))
        distance_entry = ttk.Entry(distance_frame, textvariable=self.distance_m, width=10, font=("Arial", 11))
        distance_entry.pack(side="left")

        # Chế độ kiểm tra
        mode_frame = tk.LabelFrame(
            main_frame,
            text="👤 Chế độ kiểm tra",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#34495e",
            padx=30,
            pady=20
        )
        mode_frame.pack(fill="x", pady=10)

        tk.Radiobutton(
            mode_frame,
            text="👨 Người lớn (biết chữ)",
            variable=self.mode,
            value="adult",
            font=("Arial", 12),
            bg="white",
            activebackground="white",
            selectcolor="#3498db"
        ).pack(anchor="w", pady=5)

        tk.Radiobutton(
            mode_frame,
            text="👶 Trẻ nhỏ (không biết chữ)",
            variable=self.mode,
            value="child",
            font=("Arial", 12),
            bg="white",
            activebackground="white",
            selectcolor="#3498db"
        ).pack(anchor="w", pady=5)

        # Phương thức nhập liệu
        input_frame = tk.LabelFrame(
            main_frame,
            text="⌨️ Phương thức trả lời",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#34495e",
            padx=30,
            pady=20
        )
        input_frame.pack(fill="x", pady=10)

        tk.Radiobutton(
            input_frame,
            text="⌨️ Bàn phím",
            variable=self.input_method,
            value="keyboard",
            font=("Arial", 12),
            bg="white",
            activebackground="white",
            selectcolor="#2ecc71"
        ).pack(anchor="w", pady=5)

        tk.Radiobutton(
            input_frame,
            text="🎤 Giọng nói",
            variable=self.input_method,
            value="voice",
            font=("Arial", 12),
            bg="white",
            activebackground="white",
            selectcolor="#2ecc71"
        ).pack(anchor="w", pady=5)

        # Nút bắt đầu
        start_btn = tk.Button(
            main_frame,
            text="▶️ BẮT ĐẦU KIỂM TRA",
            command=self.start_test,
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            padx=30,
            pady=15,
            cursor="hand2",
            relief="raised",
            borderwidth=3
        )
        start_btn.pack(pady=30)

    def snellen_letter_size(self, snellen_denominator=40):
        """Tính kích thước ký tự theo chuẩn Snellen"""
        width, height = pyautogui.size()
        diag_px = math.hypot(width, height)
        ppi = diag_px / self.diagonal_inch.get()
        mm_per_inch = 25.4

        height_m = 0.00145 * (snellen_denominator * 0.3048) * (self.distance_m.get() / 6.096)
        height_mm = height_m * 1000
        height_px = height_mm / mm_per_inch * ppi

        return int(height_px)

    def start_test(self):
        """Bắt đầu kiểm tra thị lực"""
        try:
            if self.diagonal_inch.get() <= 0 or self.distance_m.get() <= 0:
                messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ!")
                return
        except:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
            return

        self.current_level = 0
        self.correct = 0
        self.attempts = 0
        self.show_test_screen()

    def show_test_screen(self):
        """Hiển thị màn hình kiểm tra"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frame chính
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(expand=True, fill="both")

        # Thanh trạng thái phía trên
        status_frame = tk.Frame(main_frame, bg="#34495e", height=60)
        status_frame.pack(fill="x")
        status_frame.pack_propagate(False)

        denom = SNELLEN_DENOMS[self.current_level]
        self.status_label = tk.Label(
            status_frame,
            text=f"📊 Mức: 20/{denom} | ✅ Đúng: {self.correct}/3 | 📝 Lượt: {self.attempts + 1}/5",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="white"
        )
        self.status_label.pack(pady=15)

        # Frame hiển thị ký tự/biểu tượng
        display_frame = tk.Frame(main_frame, bg="#ecf0f1")
        display_frame.pack(expand=True, fill="both", pady=40)

        # Tạo câu hỏi mới
        if self.mode.get() == "adult":
            self.current_item = random.choice(LETTERS)
            font_size = self.snellen_letter_size(denom)

            self.symbol_label = tk.Label(
                display_frame,
                text=self.current_item,
                font=("Arial", font_size, "bold"),
                bg="#ecf0f1",
                fg="#2c3e50"
            )
            self.symbol_label.pack()
        else:
            self.current_item = random.choice(LEA_SYMBOLS)
            font_size = self.snellen_letter_size(denom) * 2

            self.symbol_label = tk.Label(
                display_frame,
                text=self.current_item["emoji"],
                font=("Arial", font_size),
                bg="#ecf0f1"
            )
            self.symbol_label.pack()

            # Hiển thị các lựa chọn
            self.current_options = random.sample(LEA_SYMBOLS, len(LEA_SYMBOLS))
            options_frame = tk.Frame(display_frame, bg="#ecf0f1")
            options_frame.pack(pady=30)

            for idx, opt in enumerate(self.current_options):
                btn = tk.Button(
                    options_frame,
                    text=f"{idx + 1}. {opt['emoji']} {opt['name']}",
                    font=("Arial", 16),
                    bg="white",
                    fg="#2c3e50",
                    padx=20,
                    pady=10,
                    command=lambda i=idx: self.check_answer_child(i),
                    cursor="hand2",
                    relief="raised",
                    borderwidth=2
                )
                btn.pack(pady=5)

        # Frame nhập liệu (chỉ cho người lớn)
        if self.mode.get() == "adult":
            input_frame = tk.Frame(main_frame, bg="#ecf0f1")
            input_frame.pack(pady=20)

            if self.input_method.get() == "keyboard":
                tk.Label(
                    input_frame,
                    text="Nhập ký tự bạn nhìn thấy:",
                    font=("Arial", 12),
                    bg="#ecf0f1"
                ).pack()

                self.answer_entry = ttk.Entry(input_frame, font=("Arial", 16), width=10, justify="center")
                self.answer_entry.pack(pady=10)
                self.answer_entry.focus()
                self.answer_entry.bind("<Return>", lambda e: self.check_answer_keyboard())

                submit_btn = tk.Button(
                    input_frame,
                    text="✓ Xác nhận",
                    command=self.check_answer_keyboard,
                    font=("Arial", 12, "bold"),
                    bg="#3498db",
                    fg="white",
                    padx=20,
                    pady=10,
                    cursor="hand2"
                )
                submit_btn.pack()
            else:
                voice_btn = tk.Button(
                    input_frame,
                    text="🎤 Nhấn để nói",
                    command=self.check_answer_voice,
                    font=("Arial", 14, "bold"),
                    bg="#e74c3c",
                    fg="white",
                    padx=30,
                    pady=15,
                    cursor="hand2",
                    relief="raised",
                    borderwidth=3
                )
                voice_btn.pack()

        # Nút quay lại
        back_btn = tk.Button(
            main_frame,
            text="← Quay lại",
            command=self.show_welcome_screen,
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        back_btn.pack(pady=10)

    def check_answer_keyboard(self):
        """Kiểm tra câu trả lời từ bàn phím"""
        answer = self.answer_entry.get().strip().upper()
        is_correct = (answer == self.current_item)
        self.process_answer(is_correct)

    def check_answer_voice(self):
        """Kiểm tra câu trả lời từ giọng nói"""
        self.status_label.config(text="🎤 Đang nghe...")
        self.root.update()

        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language="vi-VI").upper()

            # Xử lý text nhận được
            is_correct = (text == self.current_item or self.current_item in text)
            self.process_answer(is_correct)
        except sr.UnknownValueError:
            messagebox.showwarning("Lỗi", "Không nhận diện được giọng nói. Vui lòng thử lại!")
            self.show_test_screen()
        except sr.RequestError:
            messagebox.showerror("Lỗi", "Lỗi kết nối đến dịch vụ nhận diện giọng nói!")
            self.show_test_screen()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")
            self.show_test_screen()

    def check_answer_child(self, idx):
        """Kiểm tra câu trả lời cho trẻ nhỏ"""
        is_correct = (self.current_options[idx]['id'] == self.current_item['id'])
        self.process_answer(is_correct)

    def process_answer(self, is_correct):
        """Xử lý câu trả lời"""
        self.attempts += 1

        if is_correct:
            self.correct += 1
            messagebox.showinfo("Kết quả", "✅ Chính xác!")
        else:
            if self.mode.get() == "adult":
                messagebox.showerror("Kết quả", f"❌ Sai. Đáp án đúng là: {self.current_item}")
            else:
                messagebox.showerror("Kết quả", f"❌ Sai. Đáp án đúng là: {self.current_item['name']}")

        # Kiểm tra điều kiện
        if self.correct >= 3:
            # Qua level
            self.current_level += 1
            if self.current_level >= len(SNELLEN_DENOMS):
                self.show_result()
                return
            self.correct = 0
            self.attempts = 0
            self.show_test_screen()
        elif self.attempts >= 5:
            # Hết lượt
            self.show_result()
        else:
            # Tiếp tục
            self.show_test_screen()

    def show_result(self):
        """Hiển thị kết quả cuối cùng"""
        for widget in self.root.winfo_children():
            widget.destroy()

        result_frame = tk.Frame(self.root, bg="#ecf0f1")
        result_frame.pack(expand=True, fill="both", padx=40, pady=40)

        # Tiêu đề
        tk.Label(
            result_frame,
            text="🎉 KẾT QUẢ KIỂM TRA",
            font=("Arial", 28, "bold"),
            bg="#ecf0f1",
            fg="#27ae60"
        ).pack(pady=30)

        # Kết quả
        final_level = max(0, self.current_level - 1)
        result_text = f"Thị lực ước tính của bạn: 20/{SNELLEN_DENOMS[final_level]}"

        tk.Label(
            result_frame,
            text=result_text,
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#2c3e50",
            padx=30,
            pady=20,
            relief="solid",
            borderwidth=2
        ).pack(pady=20)

        # Lời khuyên
        advice = ""
        if SNELLEN_DENOMS[final_level] >= 40:
            advice = "👍 Thị lực của bạn rất tốt!"
        elif SNELLEN_DENOMS[final_level] >= 25:
            advice = "😊 Thị lực của bạn khá tốt!"
        else:
            advice = "⚠️ Bạn nên đi khám mắt để được tư vấn cụ thể hơn."

        tk.Label(
            result_frame,
            text=advice,
            font=("Arial", 14),
            bg="#ecf0f1",
            fg="#34495e"
        ).pack(pady=20)

        # Các nút
        btn_frame = tk.Frame(result_frame, bg="#ecf0f1")
        btn_frame.pack(pady=30)

        retry_btn = tk.Button(
            btn_frame,
            text="🔄 Kiểm tra lại",
            command=self.show_welcome_screen,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        retry_btn.pack(side="left", padx=10)

        exit_btn = tk.Button(
            btn_frame,
            text="✖️ Thoát",
            command=self.root.quit,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        exit_btn.pack(side="left", padx=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = EyeTestApp(root)
    root.mainloop()