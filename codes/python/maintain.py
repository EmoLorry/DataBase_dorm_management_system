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


class MaintainSystem:
    def __init__(self, admin_id):
        # 全视窗
        self.maintain_window = tk.Tk()
        # 二层功能视窗
        self.function_frame = None
        # 三层视窗
        self.function_frame_final = None
        # 学生id
        self.id = admin_id
        window_width = 800
        window_height = 600

        screen_width = self.maintain_window.winfo_screenwidth()
        screen_height = self.maintain_window.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.maintain_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.maintain_window.title("维修界面")
        self.bg_photo = ImageTk.PhotoImage(compress_image("MyHappyCottage.jpg", (1400, 600)))
        self.bg_photo0 = ImageTk.PhotoImage(compress_image("MyHappyCottage0.jpg", (800, 600)))
        self.bg_photo1 = ImageTk.PhotoImage(compress_image("TreeWithLight.jpg", (1200, 600)))
        self.bg_photo2 = ImageTk.PhotoImage(compress_image("LightTower.jpg", (1200, 600)))
        self.create_widgets()

    def create_widgets(self):

        # 分层视图分割化
        canvas = tk.Canvas(self.maintain_window, width=800, height=600)
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo2)

        label0 = tk.Label(self.maintain_window, text="维修人员页")
        label0.place(x=10, y=10)

        # 创建第一层功能选择按钮
        fix_button = tk.Button(self.maintain_window, text="我的维修",
                               command=lambda: self.select_function("我的维修"))
        fix_button.place(x=10, y=200)

        information_button = tk.Button(self.maintain_window, text="个人信息",
                                       command=lambda: self.select_function("个人信息"))
        information_button.place(x=10, y=100)

        # 创建第二层功能显示区域
        self.function_frame = tk.Frame(self.maintain_window)
        self.function_frame.place(x=90, y=0, width=710, height=600)

        # 默认显示个人信息界面
        self.create_information_widgets()
        information_button.config(relief=tk.SUNKEN, bg='gold')

    def create_fix_widgets(self):
        # 清空当前功能显示区域
        for widget in self.function_frame.winfo_children():
            widget.destroy()

        # 创建画布并设置背景图像
        canvas = tk.Canvas(self.function_frame, width=710, height=600)
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo1)

        # 创建第三层功能显示区域
        self.function_frame_final = tk.Frame(self.function_frame)
        self.function_frame_final.place(x=0, y=70, width=710, height=530)

        # 创建报修管理界面
        query_button = tk.Button(self.function_frame, text="我的维修", command=self.fix)
        query_button.place(x=60, y=15)

        self.fix()

    def on_fix_query_select(self, event):
        selected_item = self.listbox.selection()
        if not selected_item:
            return

        item = self.listbox.item(selected_item)
        values = item['values']
        apply_student_id, timestamp, detail, is_approved_str = values
        is_fixed = 1

        try:
            cursor = db.cursor()
            update_query = '''
                    UPDATE fix
                    SET is_fixed = %s
                    WHERE apply_student_id = %s AND timestamp = %s
                '''
            cursor.execute(update_query, (is_fixed, apply_student_id, timestamp))
            db.commit()
            messagebox.showinfo("成功", "已更改状态为已维修！")
            self.fix_query_action()  # 重新查询以刷新列表框

        except Exception as e:
            messagebox.showerror("错误", "维修状态更新失败: " + str(e))

    def fix(self):

        button_font = font.Font(family="宋体", size=12, weight="bold")
        button_font_big_title = font.Font(family="楷体", size=24, weight="bold")

        for widget in self.function_frame_final.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.function_frame_final, width=710, height=600)
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo1)

        # 取消所有按钮的选中状态
        for child in self.function_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.config(relief=tk.RAISED, bg='#ffffff')

        for child in self.function_frame.winfo_children():
            if isinstance(child, tk.Button) and child.cget("text") == "我的维修":
                child.config(relief=tk.SUNKEN, bg='pink')

        label = tk.Label(self.function_frame_final, text="我的维修(已审批)：", font=button_font,
                         bg=self.function_frame_final["bg"])
        label.place(x=365, y=50, anchor="center")

        # 创建学号输入框
        stu_id_label = tk.Label(self.function_frame_final, text="学号：", font=button_font)
        stu_id_label.place(x=172, y=120)
        self.stu_id = tk.Entry(self.function_frame_final)
        self.stu_id.place(x=230, y=120)

        fix_query_button = tk.Button(self.function_frame_final, text="查询（双击设置已维修）",
                                     command=self.fix_query_action,
                                     width=20, height=3,
                                     font=button_font)
        fix_query_button.place(x=400, y=98)

        self.result_frame = tk.Frame(self.function_frame_final, width=400, height=200, bg="white")
        self.result_frame.place(x=170, y=200)
        # 创建竖直滚动条
        scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical")

        # 创建列表框
        self.listbox = ttk.Treeview(self.result_frame, columns=("1", "2", "3", "4"), show="headings",
                                    yscrollcommand=scrollbar.set)

        # 绑定<<TreeviewSelect>>事件,双击进入记录以进一步操作
        self.listbox.bind("<Double-1>", self.on_fix_query_select)
        # 设置每列的标题
        self.listbox.heading("1", text="报修学生")
        self.listbox.heading("2", text="报修时间")
        self.listbox.heading("3", text="报修理由")
        self.listbox.heading("4", text="是否已维修")

        # 设置每列的宽度和对齐方式
        self.listbox.column("1", width=100, anchor="center")
        self.listbox.column("2", width=100, anchor="center")
        self.listbox.column("3", width=100, anchor="center")
        self.listbox.column("4", width=100, anchor="center")

        # 将滚动条与列表框关联
        scrollbar.config(command=self.listbox.yview)

        # 使用pack方法来布局滚动条和列表框
        # 使用grid方法来布局滚动条和列表框
        self.listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        # 创建查看评价按钮
        query_button = tk.Button(self.function_frame, text="查看评价", command=self.evaluate_query)
        query_button.place(x=350, y=500)

    def fix_query_action(self):
        stu_id = self.stu_id.get()
        # 获取所有的item,如果存在item，则删除
        items = self.listbox.get_children()
        if items:
            for item in items:
                self.listbox.delete(item)
        cursor = db.cursor()
        cursor.execute('SELECT count(*) FROM '
                       'fix '
                       'where is_fixed = 0 and '
                       'apply_student_id in (select student_id from '
                       'student natural join dorm natural join dormitory_building '
                       'where maintain_id =%s)', self.id)
        print(f"当前系统中有{cursor.fetchone()[0]}条您负责的宿舍楼未维修的报修记录")
        db.commit()
        cursor = db.cursor()
        if not stu_id:
            cursor.execute('SELECT apply_student_id, timestamp, detail, is_fixed '
                           'FROM '
                           'fix '
                           'where '
                           'is_approved = 1 and '
                           'apply_student_id in (select student_id from '
                           'student natural join dorm natural join dormitory_building '
                           'where maintain_id =%s)', self.id)
            student_info = cursor.fetchall()
            # 转换 is_approved 的值
            converted_info = []
            for record in student_info:
                apply_student_id, timestamp, detail, is_approved = record
                is_approved_str = "是" if is_approved == 1 else "否"
                converted_info.append((apply_student_id, timestamp, detail, is_approved_str))
        else:
            cursor.execute('SELECT apply_student_id, timestamp, detail, is_fixed '
                           'FROM '
                           'fix '
                           'where '
                           'is_approved = 1 and '
                           'apply_student_id in (select student_id from '
                           'student natural join dorm natural join dormitory_building '
                           'where maintain_id =%s) and '
                           'apply_student_id  LIKE %s', (self.id, '%' + stu_id + '%'))
            student_info = cursor.fetchall()
            # 转换 is_approved 的值
            converted_info = []
            for record in student_info:
                apply_student_id, timestamp, detail, is_approved = record
                is_approved_str = "是" if is_approved == 1 else "否"
                converted_info.append((apply_student_id, timestamp, detail, is_approved_str))

        # 按照 is_approved_str 的值进行排序，确保 "否" 的记录排在前面
        converted_info.sort(key=lambda x: x[3], reverse=False)

        # 将学生信息逐行添加到列表框中
        if not converted_info:
            messagebox.showinfo("未找到匹配筛选结果", "未找到匹配筛选结果，请尝试其他搜索条件。")
        else:
            for info in converted_info:
                self.listbox.insert("", "end", values=tuple(str(i) for i in info))

    def evaluate_query(self):
        try:
            cursor = db.cursor()
            # 查询评价记录，按时间戳排序
            query = (
                "SELECT * FROM evaluate "
                "WHERE student_id IN ("
                "SELECT student_id FROM "
                "student NATURAL JOIN dorm "
                "NATURAL JOIN dormitory_building "
                "WHERE maintain_id = %s) "
                "ORDER BY apply_timestamp"
            )
            cursor.execute(query, (self.id,))

            # 获取所有记录
            records = cursor.fetchall()

            if not records:
                messagebox.showinfo("未找到记录", "未找到评价记录。")
                return

            # 创建新窗口
            new_window = tk.Toplevel()
            new_window.title("评价记录")

            # 定义表头
            columns = ("提交学生id", "报修申请时间", "评价时间", "报修申请描述", "评价描述")
            tree = ttk.Treeview(new_window, columns=columns, show='headings')
            tree.pack(fill=tk.BOTH, expand=True)

            # 定义每列的标题和宽度
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            # 插入记录
            for record in records:
                tree.insert("", tk.END, values=record)

        except db.Error as err:
            messagebox.showerror("数据库错误", f"错误: {err}")

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
        cursor.execute('select job_number, sta_age, sta_sex, sta_name, job_content '
                       'from dorm_maintain natural join dormitorystaff '
                       'where job_number = %s', self.id)
        admin_info = cursor.fetchone()
        job_number = admin_info[0]
        sta_age = admin_info[1]
        sta_sex = admin_info[2]
        sta_name = admin_info[3]
        sta_content = admin_info[4]

        Label0 = tk.Label(self.function_frame, text="工号: " + str(job_number), font=button_font_big_title)
        Label0.place(x=370, y=20, anchor="center")
        Label1 = tk.Label(self.function_frame, text="姓名: " + str(sta_name), font=button_font_big_title)
        Label1.place(x=370, y=70, anchor="center")
        Label2 = tk.Label(self.function_frame, text="性别: " + str(sta_sex), font=button_font_big_title)
        Label2.place(x=370, y=120, anchor="center")
        Label3 = tk.Label(self.function_frame, text="年龄: " + str(sta_age), font=button_font_big_title)
        Label3.place(x=370, y=170, anchor="center")
        Label4 = tk.Label(self.function_frame, text="工作内容: " + str(sta_content), font=button_font_big_title)
        Label4.place(x=370, y=220, anchor="center")
        if self.id != '88888888':
            cursor.execute('select building_id '
                           'from dormitory_building  '
                           'where maintain_id = %s', self.id)
            mana_building = cursor.fetchone()[0]
            Label5 = tk.Label(self.function_frame, text="维修宿舍楼: " + str(mana_building), font=button_font_big_title)
            Label5.place(x=370, y=270, anchor="center")
        # 创建重设密码按钮
        reset_password_button = tk.Button(self.function_frame, text="重设密码", command=self.show_reset_password_window)
        reset_password_button.place(x=550, y=270, anchor="center")

        # 创建更改工作内容按钮
        change_job_content_button = tk.Button(self.function_frame, text="更改工作内容",
                                              command=lambda: self.show_change_job_content_window(Label4))
        change_job_content_button.place(x=650, y=270, anchor="center")

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
        cursor.execute('SELECT password FROM dormitorystaff WHERE job_number = %s', self.id)
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
            cursor.execute('UPDATE dormitorystaff SET password = %s WHERE job_number = %s',
                           (new_password_entry, self.id))
            db.commit()
            tk.messagebox.showinfo("成功", "密码已成功重设！")
            reset_password_window.destroy()
        else:
            # 原密码不正确，显示错误提示
            tk.messagebox.showerror("错误", "原密码不正确，请重新输入！")

    def show_change_job_content_window(self, Label4):
        change_job_content_window = tk.Toplevel()
        change_job_content_window.title("更改工作内容")
        change_job_content_window.geometry("300x150")

        job_content_label = tk.Label(change_job_content_window, text="新工作内容：")
        job_content_label.pack()
        job_content_entry = tk.Entry(change_job_content_window)
        job_content_entry.pack()

        confirm_button = tk.Button(change_job_content_window, text="确认",
                                   command=lambda: self.change_job_content(str(job_content_entry.get()), Label4,
                                                                           change_job_content_window))
        confirm_button.pack()

    def change_job_content(self, job_content_entry, Label4, change_job_content_window):
        button_font_big_title = font.Font(family="楷体", size=18, weight="bold")
        cursor = db.cursor()

        # 更新职工的工作内容
        cursor.execute('UPDATE dorm_maintain SET Job_Content = %s WHERE job_number = %s',
                       (job_content_entry, self.id))
        db.commit()
        tk.messagebox.showinfo("成功", "工作内容已成功更新！")
        change_job_content_window.destroy()
        Label4.config(text="工作内容: " + job_content_entry)

    def select_function(self, function_name):
        # 清空当前功能显示区域
        for widget in self.function_frame.winfo_children():
            widget.destroy()

        # 取消所有按钮的选中状态
        for child in self.maintain_window.winfo_children():
            if isinstance(child, tk.Button):
                child.config(relief=tk.RAISED, bg='#ffffff')

        if function_name == "我的维修":
            self.create_fix_widgets()
        elif function_name == "个人信息":
            self.create_information_widgets()

        # 设置当前选中按钮为凹陷状态
        for child in self.maintain_window.winfo_children():
            if isinstance(child, tk.Button) and child.cget("text") == function_name:
                child.config(relief=tk.SUNKEN, bg='gold')


# if __name__ == "__main__":
#     admin = MaintainSystem("20242317")
#     admin.maintain_window.mainloop()
