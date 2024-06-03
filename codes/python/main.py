import pymysql
import tkinter as tk
from admin import AdminSystem
from student import StudentSystem
from maintain import MaintainSystem
from tkinter import font
from PIL import Image, ImageTk

DBHOST = 'localhost'
DBUSER = 'root'
DBPAWO = '-----------'
DBNAME = 'mydormitory'

# connection
try:
    db = pymysql.Connect(host=DBHOST, user=DBUSER, password=DBPAWO, database=DBNAME)
    print("Connecting to database mydormitory Successfully!")
except pymysql.Error as e:
    print("Error connecting to database mydormitory")


class LoginSystem:
    def __init__(self):
        self.login_window = tk.Tk()
        window_width = 800
        window_height = 600

        screen_width = self.login_window.winfo_screenwidth()
        screen_height = self.login_window.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.login_window.title("学生宿舍管理系统登录")
        # self.login_window.configure(bg="white")
        self.create_widgets()

    def create_widgets(self):
        # 创建字体对象
        button_font = font.Font(family="宋体", size=12, weight="bold")
        button_font_big_title = font.Font(family="楷体", size=24, weight="bold")

        # 创建直线
        self.canvas = tk.Canvas(self.login_window, width=800, height=600)
        self.canvas.place(x=0, y=0)
        # 使用 place() 方法来放置画布，设置 x 和 y 坐标
        line = self.canvas.create_line(100, 80, 700, 80, 700, 450, 100, 450, 100, 80)
        self.canvas.itemconfig(line, fill="green")

        U_label = tk.Label(self.login_window, text="学生宿舍管理系统", font=button_font_big_title)
        U_label.place(x=270, y=20)

        # 创建用户名和密码输入框
        username_label = tk.Label(self.login_window, text="账号：", font=button_font)
        username_label.place(x=300, y=100)
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.place(x=350, y=100)

        password_label = tk.Label(self.login_window, text="密码：", font=button_font)
        password_label.place(x=300, y=130)
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.place(x=350, y=130)
        # 创建密码可视性切换按钮
        self.show_password_var = tk.BooleanVar()
        show_password_checkbox = tk.Checkbutton(self.login_window, text="显示密码", variable=self.show_password_var,
                                                command=self.toggle_password_visibility)
        show_password_checkbox.place(x=520, y=130)

        # 创建登录选项
        self.user_type = tk.StringVar()
        self.user_type.set("admin")  # 默认选项为管理员登录
        login_options_frame = tk.Frame(self.login_window)
        login_options_frame.place(x=253, y=170)
        tk.Radiobutton(login_options_frame, text="我是管理员", variable=self.user_type, value="admin").pack(
            side=tk.LEFT, padx=5)
        tk.Radiobutton(login_options_frame, text="我是学生", variable=self.user_type, value="student").pack(
            side=tk.LEFT, padx=5)
        tk.Radiobutton(login_options_frame, text="我是维修人员", variable=self.user_type, value="maintenance").pack(
            side=tk.LEFT, padx=5)
        # 创建登录按钮，调整大小并居中设置

        login_button = tk.Button(self.login_window, text="登录", command=self.login, width=20, height=3,
                                 font=button_font)
        login_button.place(x=305, y=270)

        # 创建用于显示错误消息的标签
        self.error_label = tk.Label(self.login_window, fg="red", font=button_font)
        self.error_label.place(x=331, y=350)

        U1_label = tk.Label(self.login_window, text="作者：罗瑞", font=button_font)
        U1_label.place(x=655, y=510)
        U1_label = tk.Label(self.login_window, text="时间：2024年5月", font=button_font)
        U1_label.place(x=655, y=540)
        U1_label = tk.Label(self.login_window, text="version 1.0 based on mySQL8.2 & py3.9", font=button_font)
        U1_label.place(x=450, y=570)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            # 显示密码
            self.password_entry.config(show="")
        else:
            # 隐藏密码
            self.password_entry.config(show="*")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type.get()

        # 这里可以添加验证用户名和密码的逻辑，这里简化为直接比较
        if user_type == "admin":
            cursor = db.cursor()

            # 执行查询以检查用户名和密码是否匹配
            cursor.execute('SELECT COUNT(*) '
                           'FROM dorm_supervisor natural join dormitorystaff '
                           'WHERE job_number = %s AND password = %s',
                           (username, password))
            result = cursor.fetchone()

            if result[0] == 1:  # 如果查询返回一个匹配的结果
                # 管理员登录成功，销毁登录窗口，显示管理界面
                self.login_window.destroy()
                # 跳转到username对应的管理类中
                admin = AdminSystem(username)
                admin.admin_window.mainloop()

            else:
                self.error_label.config(text="用户名或密码错误")

        elif user_type == "student":
            cursor = db.cursor()

            # 执行查询以检查用户名和密码是否匹配
            cursor.execute('SELECT COUNT(*) '
                           'FROM student '
                           'WHERE student_id = %s AND login_password = %s',
                           (username, password))
            result = cursor.fetchone()
            if result[0] == 1:  # 如果查询返回一个匹配的结果
                # 学生登录成功，销毁登录窗口，显示学生界面
                self.login_window.destroy()
                # self.show_student_window(user_type)
                student = StudentSystem(username)
                student.student_window.mainloop()

            else:
                self.error_label.config(text="用户名或密码错误")
        elif user_type == "maintenance":
            cursor = db.cursor()

            # 执行查询以检查用户名和密码是否匹配
            cursor.execute('SELECT COUNT(*) '
                           'FROM dorm_maintain natural join dormitorystaff '
                           'WHERE job_number = %s AND password = %s',
                           (username, password))
            result = cursor.fetchone()

            if result[0] == 1:  # 如果查询返回一个匹配的结果
                # 学生登录成功，销毁登录窗口，显示学生界面
                self.login_window.destroy()
                # self.show_student_window(user_type)
                student = MaintainSystem(username)
                student.maintain_window.mainloop()

            else:
                self.error_label.config(text="用户名或密码错误")


if __name__ == "__main__":
    login_system = LoginSystem()
    login_system.login_window.mainloop()
# 20241315
# jin5

# 学生
# 2552522
# 123456


