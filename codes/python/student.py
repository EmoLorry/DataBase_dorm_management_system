# -*- coding: utf-8 -*-
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import messagebox, Listbox, END, Toplevel, Text, Button, Label
from PIL import Image, ImageTk
from tkinter import font
import pymysql
from admin_set_student import *
from datetime import datetime

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


def compress_image(input_path, max_size):
    """
    压缩图像到指定大小
    :param input_path: 输入图像路径
    :param max_size: 最大尺寸（以像素为单位），如 (800, 600)
    """
    image = Image.open(input_path)
    image.thumbnail(max_size)
    return image


def show_evaluation_page(record):
    eval_window = tk.Toplevel()
    eval_window.title("评价报修")
    eval_window.geometry("400x300")

    student_id, timestamp, detail, is_approved, is_fixed = record
    date_part = timestamp.date()  # 获取日期部分
    time_part = timestamp.time()  # 获取时间部分
    formatted_time = datetime.combine(date_part, time_part).strftime("%Y-%m-%d %H:%M:%S")  # 创建 datetime 对象并格式化时间

    Label(eval_window, text=f"申请提交时间: {formatted_time}").pack(pady=5)
    Label(eval_window, text=f"描述: {detail}").pack(pady=5)
    approval = "已审批" if is_approved else "未审批"
    fixation = "已修复" if is_fixed else "未修复"
    Label(eval_window, text=f"报修情况: {approval} {fixation}").pack(pady=5)
    Label(eval_window, text="评价内容：").pack(pady=5)
    eval_text = Text(eval_window, wrap=tk.WORD, width=40, height=6)
    eval_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def submit_evaluation():
        evaluation_content = eval_text.get("1.0", END).strip()
        if evaluation_content:
            try:
                current_timestamp = datetime.now()
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO evaluate (Student_id, apply_timestamp, evaluate_timestamp, apply_description, "
                    "evaluate_description) VALUES (%s, %s, %s, %s, %s)",
                    (student_id, timestamp, current_timestamp, detail, evaluation_content))
                db.commit()
                messagebox.showinfo("成功", "评价提交成功")
                eval_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", "评价提交失败: " + str(e))
        else:
            messagebox.showwarning("警告", "评价内容不能为空")

    submit_button = Button(eval_window, text="提交", command=submit_evaluation)
    submit_button.pack(pady=10)


class StudentSystem:
    def __init__(self, admin_id):
        # 全视窗
        self.student_window = tk.Tk()
        # 二层功能视窗
        self.function_frame = None
        # 学生id
        self.id = admin_id
        window_width = 800
        window_height = 600

        screen_width = self.student_window.winfo_screenwidth()
        screen_height = self.student_window.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.student_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.student_window.title("学生界面")
        self.bg_photo = ImageTk.PhotoImage(compress_image("MyHappyCottage.jpg", (1400, 600)))
        self.bg_photo0 = ImageTk.PhotoImage(compress_image("MyHappyCottage0.jpg", (800, 600)))
        self.bg_photo1 = ImageTk.PhotoImage(compress_image("TreeWithLight.jpg", (1200, 600)))
        self.bg_photo2 = ImageTk.PhotoImage(compress_image("LightTower.jpg", (1200, 600)))
        self.create_widgets()

    def create_widgets(self):

        # 分层视图分割化
        canvas = tk.Canvas(self.student_window, width=800, height=600)
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo2)

        label0 = tk.Label(self.student_window, text="学生页")
        label0.place(x=20, y=10)

        # 创建第一层功能选择按钮
        fix_button = tk.Button(self.student_window, text="维修申请",
                               command=lambda: self.select_function("维修申请"))
        fix_button.place(x=10, y=200)

        information_button = tk.Button(self.student_window, text="个人信息",
                                       command=lambda: self.select_function("个人信息"))
        information_button.place(x=10, y=100)

        # 创建第二层功能显示区域
        self.function_frame = tk.Frame(self.student_window)
        self.function_frame.place(x=90, y=0, width=710, height=600)

        # 默认显示个人信息界面
        self.create_information_widgets()
        #
        information_button.config(relief=tk.SUNKEN, bg='gold')

    # 学生管理界面
    def create_student_fix_widgets(self):
        # 清空当前功能显示区域
        for widget in self.function_frame.winfo_children():
            widget.destroy()

        button_font = font.Font(family="宋体", size=12, weight="bold")
        button_font_big_title = font.Font(family="楷体", size=24, weight="bold")

        # 创建画布并设置背景图像
        canvas = tk.Canvas(self.function_frame, width=710, height=600)
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo1)

        fix_label = tk.Label(self.function_frame, text="维修申请细节描述：", font=button_font)
        fix_label.place(x=285, y=70)
        fix_entry = tk.Text(self.function_frame, width=50, height=10)
        fix_entry.place(x=185, y=135)

        query_button = tk.Button(self.function_frame, text="提交维修申请",
                                 command=lambda: self.fix_action(fix_entry.get("1.0", "end").strip()))
        query_button.place(x=320, y=300)
        query_button = tk.Button(self.function_frame, text="我的报修",
                                 command=lambda: self.fix_query())
        query_button.place(x=332, y=350)

        cursor = db.cursor()
        cursor.execute('select sta_name, phone '
                       'from dormitorystaff natural join dorm_maintain '
                       'where job_number = (select maintain_id from dormitory_building '
                       'where building_id = (select building_id from dorm '
                       'where dormitory_id= (select dormitory_id from student '
                       'where student_id=%s)))', self.id)
        maintain_info = cursor.fetchone()
        Label8 = tk.Label(self.function_frame, text="宿舍楼维修员姓名: " + str(maintain_info[0]),
                          font=button_font)
        Label8.place(x=370, y=530, anchor="center")
        Label9 = tk.Label(self.function_frame, text="宿舍楼维修员联系方式: " + str(maintain_info[1]),
                          font=button_font)
        Label9.place(x=370, y=570, anchor="center")

    def fix_query(self):
        root = tk.Tk()
        root.title("维修记录查询")
        root.geometry("500x300")
        listbox = tk.Listbox(root, width=60, height=15)
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        try:
            # 创建游标对象
            cursor = db.cursor()

            # 执行查询操作，按时间排序
            cursor.execute("SELECT * FROM fix WHERE apply_student_id = %s ORDER BY timestamp DESC", (self.id,))
            records = cursor.fetchall()
            # 格式化显示维修记录
            for record in records:
                student_id, timestamp, detail, is_approved, is_fixed = record

                date_part = timestamp.date()  # 获取日期部分
                time_part = timestamp.time()  # 获取时间部分
                formatted_time = datetime.combine(date_part, time_part).strftime(
                    "%Y-%m-%d %H:%M:%S")  # 创建 datetime 对象并格式化时间
                approved_text = "已审批" if is_approved else "未审批"
                fixed_text = "已修复" if is_fixed else "未修复"
                listbox.insert(tk.END, f"时间: {formatted_time}  详情: {detail}  {approved_text}  {fixed_text}")

            def on_double_click(event):
                widget = event.widget
                selection = widget.curselection()
                if selection:
                    index = selection[0]
                    select_record = records[index]
                    show_evaluation_page(select_record)

            listbox.bind('<Double-Button-1>', on_double_click)

        except Exception as e:
            messagebox.showerror("错误", "报修记录查询失败: " + str(e))

        root.mainloop()

    def fix_action(self, detail):
        try:
            print(detail)
            # 检查申请内容是否为空
            if not detail:
                messagebox.showwarning("警告", "报修内容不能为空！")
                return

            # 创建游标对象
            cursor = db.cursor()

            # 执行插入操作
            cursor.execute("INSERT INTO fix (apply_student_id, detail) VALUES (%s, %s)", (self.id, detail))

            # 提交事务
            db.commit()
            messagebox.showinfo("成功", "维修记录提交成功！请耐心等待审核结果，可在本界面中点击“我的报修”查询！: ")

        except Exception as e:
            messagebox.showerror("错误", "维修记录提交失败: " + str(e))

    # 个人信息界面,逻辑比较简单，不再详细注释
    def create_information_widgets(self):
        # 清空当前功能显示区域
        for widget in self.function_frame.winfo_children():
            widget.destroy()

        button_font = font.Font(family="宋体", size=12, weight="bold")
        button_font_big_title = font.Font(family="楷体", size=18, weight="bold")

        canvas = tk.Canvas(self.function_frame, width=710, height=600)
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo1)

        cursor = db.cursor()
        cursor.execute('select dormitory_id, stu_name, stu_sex, stu_seat,stu_college '
                       'from student '
                       'where student_id = %s', self.id)
        student_info = cursor.fetchone()
        stu_id = self.id
        dorm_id = student_info[0]
        stu_seat = student_info[3]
        stu_sex = student_info[2]
        stu_name = student_info[1]
        stu_college = student_info[4]

        Label0 = tk.Label(self.function_frame, text="学号: " + str(stu_id), font=button_font_big_title)
        Label0.place(x=370, y=20, anchor="center")
        Label1 = tk.Label(self.function_frame, text="姓名: " + str(stu_name), font=button_font_big_title)
        Label1.place(x=370, y=70, anchor="center")
        Label2 = tk.Label(self.function_frame, text="学院: " + str(stu_college), font=button_font_big_title)
        Label2.place(x=370, y=120, anchor="center")
        Label3 = tk.Label(self.function_frame, text="性别: " + str(stu_sex), font=button_font_big_title)
        Label3.place(x=370, y=170, anchor="center")

        # 创建重设密码按钮
        reset_password_button = tk.Button(self.function_frame, text="重设密码", command=self.show_reset_password_window)
        reset_password_button.place(x=526, y=20, anchor="center")

        # 创建更改个人信息按钮
        change_job_content_button = tk.Button(self.function_frame, text="更改信息",
                                              command=lambda: self.show_change_student_info_window(Label1,
                                                                                                   Label2, ))
        change_job_content_button.place(x=590, y=20, anchor="center")
        print(dorm_id)
        if dorm_id is not None:
            cursor.execute('select stu_count, electricity_balance '
                           'from dorm '
                           'where dormitory_id = %s', dorm_id)
            dorm_info = cursor.fetchone()
            cursor.execute('select sta_name, phone '
                           'from dormitorystaff natural join dorm_supervisor '
                           'where job_number = (select manager_id from dormitory_building '
                           'where building_id = (select building_id from dorm '
                           'where dormitory_id= %s))', dorm_id)
            manager_info = cursor.fetchone()
            Label4 = tk.Label(self.function_frame, text="宿舍号: " + str(dorm_id), font=button_font_big_title)
            Label4.place(x=370, y=320, anchor="center")
            Label5 = tk.Label(self.function_frame, text="宿舍人数: " + str(dorm_info[0]), font=button_font_big_title)
            Label5.place(x=370, y=370, anchor="center")
            Label6 = tk.Label(self.function_frame, text="我的床位: " + str(stu_seat), font=button_font_big_title)
            Label6.place(x=370, y=420, anchor="center")
            Label7 = tk.Label(self.function_frame, text="宿舍电费余额: " + str(dorm_info[1]),
                              font=button_font_big_title)
            Label7.place(x=370, y=470, anchor="center")
            Label8 = tk.Label(self.function_frame, text="宿舍楼管理员姓名: " + str(manager_info[0]),
                              font=button_font_big_title)
            Label8.place(x=370, y=520, anchor="center")
            Label9 = tk.Label(self.function_frame, text="宿舍楼管理员联系方式: " + str(manager_info[1]),
                              font=button_font_big_title)
            Label9.place(x=370, y=570, anchor="center")
            query_dorm_mate_button = tk.Button(self.function_frame, text="查看舍友信息",
                                               command=self.show_query_dorm_mate_window)
            query_dorm_mate_button.place(x=665, y=20, anchor="center")
        else:
            Label9 = tk.Label(self.function_frame, text="未分配宿舍 ", font=button_font_big_title)
            Label9.place(x=370, y=420, anchor="center")

    def show_query_dorm_mate_window(self):
        cursor = db.cursor()
        cursor.execute('SELECT dormitory_id from student where student_id = %s', self.id)
        dorm_id = cursor.fetchone()[0]
        cursor.execute('SELECT stu_count,building_id,building_location from dorm natural join dormitory_building'
                       ' where dormitory_id = %s', dorm_id)
        item_values = cursor.fetchone()
        stu_count = item_values[0]
        building = item_values[0]
        area = item_values[0]

        # 创建新窗口
        new_window = tk.Toplevel()
        new_window.title("宿舍信息卡")
        # 设置新窗口的大小
        window_width = 410
        window_height = 600
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建分割线
        canvas = tk.Canvas(new_window, width=410, height=600)
        canvas.place(x=0, y=0)
        # 使用 place() 方法来放置画布，设置 x 和 y 坐标
        line1 = canvas.create_line(0, 170, 410, 170)
        line2 = canvas.create_line(0, 460, 410, 460)
        line3 = canvas.create_line(0, 325, 410, 325)
        line4 = canvas.create_line(205, 210, 205, 450)
        canvas.itemconfig(line1, fill="green")
        canvas.itemconfig(line2, fill="green")
        canvas.itemconfig(line3, fill="red")
        canvas.itemconfig(line4, fill="red")
        cursor = db.cursor()
        cursor.execute('SELECT electricity_balance, dormitory_resident from dorm '
                       'where dormitory_id = %s', dorm_id)
        dorm_info = cursor.fetchone()
        dorm_balance = dorm_info[0]
        dorm_resident = dorm_info[1]

        # 显示宿舍信息
        tk.Label(new_window, text="宿舍号: " + str(dorm_id)).pack()
        tk.Label(new_window, text="宿舍人数: " + str(stu_count)).pack()
        tk.Label(new_window, text="宿舍电费余额: " + str(dorm_balance)).pack()
        tk.Label(new_window, text="宿舍规格: " + str(dorm_resident) + "人寝").pack()
        tk.Label(new_window, text="所在宿舍楼: " + str(building)).pack()
        tk.Label(new_window, text="所在建筑集群: " + str(area)).pack()

        cursor.execute(
            'SELECT Student_id, stu_name, stu_college '
            'FROM student '
            'WHERE dormitory_id = %s', dorm_id
        )
        student_info = cursor.fetchall()

        # 显示选定的学生信息
        # 创建四个 Frame 分割界面
        frame1 = tk.Frame(new_window, width=200, height=100)
        frame1.place(x=0, y=220)
        frame2 = tk.Frame(new_window, width=200, height=100)
        frame2.place(x=210, y=220)
        frame3 = tk.Frame(new_window, width=200, height=100)
        frame3.place(x=0, y=330)
        frame4 = tk.Frame(new_window, width=200, height=100)
        frame4.place(x=210, y=330)
        tk.Label(new_window, text=f"宿舍学生信息：").place(x=170, y=180)
        # 显示学生信息
        for i, (student_id, student_name, student_college) in enumerate(student_info, start=0):
            frame_index = i  # 确定当前学生信息应该显示在哪个 Frame 中
            current_frame = [frame1, frame2, frame3, frame4][frame_index]

            # 在当前 Frame 中显示学生信息
            tk.Label(current_frame, text=f"学生{i + 1}:").place(x=90, y=0)
            tk.Label(current_frame, text=f"学号: {student_id}").place(x=20, y=20)
            tk.Label(current_frame, text=f"姓名: {student_name}").place(x=120, y=20)
            tk.Label(current_frame, text=f"学院: {student_college}").place(x=20, y=50)

    def show_reset_password_window(self):
        reset_password_window = tk.Toplevel()
        reset_password_window.title("重设密码")
        reset_password_window.geometry("300x200")

        original_password_label = tk.Label(reset_password_window, text="原密码：")
        original_password_label.pack()
        original_password_entry = tk.Entry(reset_password_window, show="*")
        original_password_entry.pack()

        new_password_label = tk.Label(reset_password_window, text="新密码：")
        new_password_label.pack()
        new_password_entry = tk.Entry(reset_password_window, show="*")
        new_password_entry.pack()

        confirm_button = tk.Button(reset_password_window, text="确认",
                                   command=lambda: self.reset_password(str(original_password_entry.get()),
                                                                       str(new_password_entry.get()),
                                                                       reset_password_window))
        confirm_button.pack()

    def reset_password(self, old_password_entry, new_password_entry, reset_password_window):
        # 检查原密码是否正确
        cursor = db.cursor()
        cursor.execute('SELECT login_password FROM student WHERE student_id = %s', self.id)
        fetched_password = cursor.fetchone()[0]
        # print(fetched_password)
        print(old_password_entry)
        if old_password_entry == fetched_password:
            if new_password_entry == "":
                tk.messagebox.showerror("错误", "新密码不能为空！")
                return
            if new_password_entry == fetched_password:
                tk.messagebox.showerror("错误", "新密码不能与原密码相同！")
                return
            # 原密码正确，执行密码更新操作
            cursor.execute('UPDATE student SET login_password = %s WHERE student_id = %s',
                           (new_password_entry, self.id))
            db.commit()
            tk.messagebox.showinfo("成功", "密码已成功重设！")
            reset_password_window.destroy()
        else:
            # 原密码不正确，显示错误提示
            tk.messagebox.showerror("错误", "原密码不正确，请重新输入！")

    def show_change_student_info_window(self, Label1, Label2):
        show_change_student_info_window = tk.Toplevel()
        show_change_student_info_window.title("更改个人信息")
        show_change_student_info_window.geometry("300x150")

        name_label = tk.Label(show_change_student_info_window, text="姓名：")
        name_label.pack()
        name_entry = tk.Entry(show_change_student_info_window)
        name_entry.pack()
        college_label = tk.Label(show_change_student_info_window, text="学院：")
        college_label.pack()
        college_entry = tk.Entry(show_change_student_info_window)
        college_entry.pack()

        confirm_button = tk.Button(show_change_student_info_window, text="确认",
                                   command=lambda: self.change_info_content(str(name_entry.get()),
                                                                            str(college_entry.get()),
                                                                            Label1,
                                                                            Label2,
                                                                            show_change_student_info_window
                                                                            ))
        confirm_button.pack()

    def change_info_content(self, name, college, Label1, Label2, show_change_student_info_window):
        button_font_big_title = font.Font(family="楷体", size=18, weight="bold")
        cursor = db.cursor()
        # 更新姓名
        cursor.execute('UPDATE student SET stu_name = %s WHERE student_id = %s',
                       (name, self.id))
        # 更新学院
        cursor.execute('UPDATE student SET stu_college = %s WHERE student_id = %s',
                       (college, self.id))
        db.commit()
        tk.messagebox.showinfo("修改成功", "你的信息已成功更新！")
        show_change_student_info_window.destroy()
        name = str(name)
        college = str(college)
        Label1.config(text="姓名: " + name)
        Label2.config(text="学院: " + college)

    def select_function(self, function_name):
        # 清空当前功能显示区域
        for widget in self.function_frame.winfo_children():
            widget.destroy()

        # 取消所有按钮的选中状态
        for child in self.student_window.winfo_children():
            if isinstance(child, tk.Button):
                child.config(relief=tk.RAISED, bg='#ffffff')

        if function_name == "维修申请":
            self.create_student_fix_widgets()
        elif function_name == "个人信息":
            self.create_information_widgets()

        # 设置当前选中按钮为凹陷状态
        for child in self.student_window.winfo_children():
            if isinstance(child, tk.Button) and child.cget("text") == function_name:
                child.config(relief=tk.SUNKEN, bg='gold')


# if __name__ == "__main__":
#     #admin = StudentSystem("2510011")
#     admin = StudentSystem("2510003")
#
#     admin.student_window.mainloop()
