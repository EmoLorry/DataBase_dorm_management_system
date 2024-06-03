# -*- coding: utf-8 -*-
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
from tkinter import font
import pymysql
from admin_set_student import *

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


class HorizontalScrollText(tk.Frame):
    def __init__(self, parent, width, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.width = width
        # 创建文本框
        self.text = tk.Text(self, wrap="none", height=1)
        self.text.pack(side="top", fill="both", expand=True)
        self.append_text("点击查询后此滚动条显示各个宿舍总人数信息")
        # 创建水平滚动条
        scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.text.xview)
        scrollbar.pack(side="bottom", fill="x")

        # 设置文本框与滚动条的关联
        self.text.config(xscrollcommand=scrollbar.set)

    def append_text(self, text):
        # 在文本框中插入新文本
        self.text.insert("end", text)

    def get_text(self):
        # 获取文本框中的文本内容
        return self.text.get("1.0", "end")

    def clear(self):
        # 清空文本框
        self.text.delete("1.0", "end")


def compress_image(input_path, max_size):
    """
    压缩图像到指定大小
    :param input_path: 输入图像路径
    :param max_size: 最大尺寸（以像素为单位），如 (800, 600)
    """
    image = Image.open(input_path)
    image.thumbnail(max_size)
    return image


class AdminSystem:
    def __init__(self, admin_id):
        # 全视窗

        self.admin_window = tk.Tk()
        # 二层功能视窗
        self.function_frame = None
        # 三层功能视窗
        self.function_frame_final = None
        # 结果视窗
        self.result_frame = None
        self.listbox = None

        # 管理员id
        self.id = admin_id
        window_width = 800
        window_height = 600

        screen_width = self.admin_window.winfo_screenwidth()
        screen_height = self.admin_window.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.admin_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.admin_window.title("宿舍管理员")
        self.bg_photo = ImageTk.PhotoImage(compress_image("MyHappyCottage.jpg", (1400, 600)))
        self.bg_photo0 = ImageTk.PhotoImage(compress_image("MyHappyCottage0.jpg", (800, 600)))
        self.bg_photo1 = ImageTk.PhotoImage(compress_image("TreeWithLight.jpg", (1200, 600)))
        self.bg_photo2 = ImageTk.PhotoImage(compress_image("LightTower.jpg", (1200, 600)))
        self.create_widgets()

    def create_widgets(self):

        # 分层视图分割化
        canvas = tk.Canvas(self.admin_window, width=800, height=600)
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo2)
        # canvas.create_line(88, 0, 88, 600, fill="green", width=3)

        label0 = tk.Label(self.admin_window, text="管理员页")
        label0.place(x=12, y=10)

        # 创建第一层功能选择按钮
        student_management_button = tk.Button(self.admin_window, text="学生管理",
                                              command=lambda: self.select_function("学生管理"))
        student_management_button.place(x=10, y=100)

        dormitory_management_button = tk.Button(self.admin_window, text="宿舍管理",
                                                command=lambda: self.select_function("宿舍管理"))
        dormitory_management_button.place(x=10, y=200)

        my_info_button = tk.Button(self.admin_window, text="我的信息", command=lambda: self.select_function("我的信息"))
        my_info_button.place(x=10, y=300)

        # 创建第二层功能显示区域
        self.function_frame = tk.Frame(self.admin_window)
        self.function_frame.place(x=90, y=0, width=710, height=600)

        # 默认显示学生管理界面
        self.create_student_management_widgets()
        # 设定学生管理按钮为当前选中状态
        student_management_button.config(relief=tk.SUNKEN, bg='gold')

    # 学生管理界面
    def create_student_management_widgets(self):
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

        # 创建学生管理界面
        query_button = tk.Button(self.function_frame, text="设置学生", command=self.query_set_student)
        query_button.place(x=60, y=15)
        # 创建报修管理界面
        query_button = tk.Button(self.function_frame, text="报修审批", command=self.fix_approve)
        query_button.place(x=180, y=15)

        # 默认显示查询设置界面
        self.query_set_student()

    def on_fix_query_select(self, event):
        selected_item = self.listbox.selection()
        if not selected_item:
            return

        item = self.listbox.item(selected_item)
        values = item['values']
        apply_student_id, timestamp, detail, is_approved_str = values
        is_approved = 1

        try:
            cursor = db.cursor()
            update_query = '''
                    UPDATE fix
                    SET is_approved = %s
                    WHERE apply_student_id = %s AND timestamp = %s
                '''
            cursor.execute(update_query, (is_approved, apply_student_id, timestamp))
            db.commit()
            messagebox.showinfo("成功", "审批状态更新成功")
            self.fix_query_action()  # 重新查询以刷新列表框

        except Exception as e:
            messagebox.showerror("错误", "审批状态更新失败: " + str(e))

    def fix_approve(self):

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
            if isinstance(child, tk.Button) and child.cget("text") == "报修审批":
                child.config(relief=tk.SUNKEN, bg='pink')

        label = tk.Label(self.function_frame_final, text="报修审批：", font=button_font,
                         bg=self.function_frame_final["bg"])
        label.place(x=365, y=50, anchor="center")

        # 创建学号输入框
        stu_id_label = tk.Label(self.function_frame_final, text="学号：", font=button_font)
        stu_id_label.place(x=172, y=120)
        self.stu_id = tk.Entry(self.function_frame_final)
        self.stu_id.place(x=230, y=120)

        fix_query_button = tk.Button(self.function_frame_final, text="查询（双击记录审批）",
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
        self.listbox.heading("4", text="是否已审批")

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
                       'where is_approved = 0 and '
                       'apply_student_id in (select student_id from '
                       'student natural join dorm natural join dormitory_building '
                       'where manager_id =%s)', self.id)
        print(f"当前系统中有{cursor.fetchone()[0]}条您管理的宿舍楼未审批的报修记录")
        db.commit()
        cursor = db.cursor()
        if not stu_id:
            cursor.execute('SELECT apply_student_id, timestamp, detail, is_approved '
                           'FROM '
                           'fix '
                           'where '
                           'apply_student_id in (select student_id from '
                           'student natural join dorm natural join dormitory_building '
                           'where manager_id =%s)', self.id)
            student_info = cursor.fetchall()
            # 转换 is_approved 的值
            converted_info = []
            for record in student_info:
                apply_student_id, timestamp, detail, is_approved = record
                is_approved_str = "是" if is_approved == 1 else "否"
                converted_info.append((apply_student_id, timestamp, detail, is_approved_str))
        else:
            cursor.execute('SELECT apply_student_id, timestamp, detail, is_approved '
                           'FROM '
                           'fix '
                           'where '
                           'apply_student_id in (select student_id from '
                           'student natural join dorm natural join dormitory_building '
                           'where manager_id =%s) and '
                           'apply_student_id  LIKE %s', (self.id,'%' + stu_id + '%'))
            student_info = cursor.fetchall()
            # 转换 is_approved 的值
            converted_info = []
            for record in student_info:
                apply_student_id, timestamp, detail, is_approved = record
                is_approved_str = "是" if is_approved == 1 else "否"
                converted_info.append((apply_student_id, timestamp, detail, is_approved_str))
        # 将学生信息逐行添加到列表框中
        if not converted_info:
            messagebox.showinfo("未找到匹配筛选结果", "未找到匹配筛选结果，请尝试其他搜索条件。")
        else:
            for info in converted_info:
                self.listbox.insert("", "end", values=tuple(str(i) for i in info))

    # ----------------------------------------------------------------
    # 学生信息卡，双击模糊查询结果即可进入信息卡，隶属于设置学生模块，
    # 拥有重设密码、更新信息、删除学生三个功能
    # ----------------------------------------------------------------
    def on_student_query_select(self, event):
        # 获取被选中的item
        selected_item = self.listbox.selection()[0]
        # 获取item的值
        item_values = self.listbox.item(selected_item, "values")
        stu_id = item_values[0]
        stu_name = item_values[1]
        stu_dorm = item_values[2]
        stu_sex = item_values[3]

        # ----------------------------------------------------------------
        # 查询的操作依据为视图，为student/dorm/dormitory_building三个表
        # 自然连接的视图，根据stu_id为依据寻找即可
        # 查询所有下文中需要的信息
        # view调用视图
        # student_all_info
        # student_id,Stu_seat, stu_college, dormitory_id, building_id, Electricity_balance, Building_location
        # ----------------------------------------------------------------

        # 创建新窗口
        new_window = tk.Toplevel()
        new_window.title("学生信息卡")
        # 设置新窗口的大小
        window_width = 400
        window_height = 300
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        cursor = db.cursor()
        # if stu_dorm == pymysql.NULL:
        #     print("YES")
        # else:
        #     print("NO")
        # print(stu_dorm)
        if stu_dorm == "None":
            cursor.execute('select stu_college '
                           'from student '
                           'where student_id = %s', stu_id)
            student_info = cursor.fetchone()
            stu_college = student_info[0]
            tk.Label(new_window, text="学号: " + str(stu_id)).pack()
            tk.Label(new_window, text="姓名: " + str(stu_name)).pack()
            tk.Label(new_window, text="性别: " + str(stu_sex)).pack()
            tk.Label(new_window, text="学院: " + str(stu_college)).pack()
            tk.Label(new_window, text="宿舍未分配").pack()
        else:
            cursor.execute(
                'SELECT Stu_seat, stu_college, building_id, Electricity_balance, Building_location '
                'FROM student_info_with_dorm '
                'WHERE Student_id = %s', stu_id
            )
            student_info = cursor.fetchone()
            stu_seat = student_info[0]
            stu_college = student_info[1]
            stu_building = student_info[2]
            stu_balance = student_info[3]
            stu_location = student_info[4]
            # 显示选定的学生信息
            tk.Label(new_window, text="学号: " + str(stu_id)).pack()
            tk.Label(new_window, text="姓名: " + str(stu_name)).pack()
            tk.Label(new_window, text="性别: " + str(stu_sex)).pack()
            tk.Label(new_window, text="学院: " + str(stu_college)).pack()
            tk.Label(new_window, text="宿舍号: " + str(stu_dorm)).pack()
            tk.Label(new_window, text="宿舍床号: " + str(stu_seat)).pack()
            tk.Label(new_window, text="宿舍电费余额: " + str(stu_balance)).pack()
            tk.Label(new_window, text="所在宿舍楼: " + str(stu_building)).pack()
            tk.Label(new_window, text="所在建筑集群: " + str(stu_location)).pack()

        # 创建按钮
        button_modify = tk.Button(new_window, text="重置密码", command=lambda: modify_password(self.id, stu_id))
        button_modify.pack()

        button_update = tk.Button(new_window, text="更新信息", command=lambda: update_student(self.id, stu_id))
        button_update.pack()

    # ----------------------------------------------------------------
    # 模糊查询功能界面，隶属于设置学生模块，
    # ----------------------------------------------------------------
    def query_set_student(self):

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
            if isinstance(child, tk.Button) and child.cget("text") == "设置学生":
                child.config(relief=tk.SUNKEN, bg='pink')

        label = tk.Label(self.function_frame_final, text="学生筛选：", font=button_font,
                         bg=self.function_frame_final["bg"])
        label.place(x=365, y=50, anchor="center")

        # 创建学号输入框
        stu_id_label = tk.Label(self.function_frame_final, text="学号：", font=button_font)
        stu_id_label.place(x=172, y=90)
        self.stu_id = tk.Entry(self.function_frame_final)
        self.stu_id.place(x=230, y=90)

        # 创建姓名输入框
        name_label = tk.Label(self.function_frame_final, text="姓名：", font=button_font)
        name_label.place(x=172, y=120)
        self.stu_name = tk.Entry(self.function_frame_final)
        self.stu_name.place(x=230, y=120)

        # 创建姓名输入框
        dorm_label = tk.Label(self.function_frame_final, text="宿舍：", font=button_font)
        dorm_label.place(x=172, y=150)
        self.dorm = tk.Entry(self.function_frame_final)
        self.dorm.place(x=230, y=150)

        query_button = tk.Button(self.function_frame_final, text="查询（双击记录设置）", command=self.query_action,
                                 width=20, height=3,
                                 font=button_font)
        query_button.place(x=400, y=98)

        self.result_frame = tk.Frame(self.function_frame_final, width=400, height=200, bg="white")
        self.result_frame.place(x=170, y=200)
        # 创建竖直滚动条
        scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical")

        # 创建列表框
        self.listbox = ttk.Treeview(self.result_frame, columns=("1", "2", "3", "4"), show="headings",
                                    yscrollcommand=scrollbar.set)

        # 绑定<<TreeviewSelect>>事件,双击进入记录以进一步操作
        self.listbox.bind("<Double-1>", self.on_student_query_select)

        # 设置每列的标题
        self.listbox.heading("1", text="学号")
        self.listbox.heading("2", text="姓名")
        self.listbox.heading("3", text="宿舍")
        self.listbox.heading("4", text="性别")

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

    # ----------------------------------------------------------------
    # 模糊查询动作，隶属于设置学生模块，
    # ----------------------------------------------------------------
    def query_action(self):
        stu_id = self.stu_id.get()
        stu_name = self.stu_name.get()
        stu_dorm = self.dorm.get()
        # 获取所有的item,如果存在item，则删除
        items = self.listbox.get_children()
        if items:
            for item in items:
                self.listbox.delete(item)

        cursor = db.cursor()
        cursor.execute('SELECT count(*) FROM '
                       'student '
                       'WHERE dormitory_id is NULL ')
        print(f"当前系统中有{cursor.fetchone()[0]}个学生未分配宿舍")
        db.commit()
        cursor = db.cursor()
        if stu_dorm == "":
            cursor.execute(
                'SELECT student_id, stu_name, dormitory_id, stu_sex '
                'FROM Student '
                'WHERE Student_id LIKE %s AND stu_name LIKE %s ',
                ('%' + stu_id + '%', '%' + stu_name + '%')
            )
            student_info = cursor.fetchall()
        else:
            cursor.execute(
                'SELECT student_id, stu_name, dormitory_id, stu_sex '
                'FROM Student '
                'WHERE Student_id LIKE %s AND stu_name LIKE %s AND dormitory_id LIKE %s',
                ('%' + stu_id + '%', '%' + stu_name + '%', '%' + stu_dorm + '%')
            )
            student_info = cursor.fetchall()

        # 将学生信息逐行添加到列表框中
        if not student_info:
            messagebox.showinfo("未找到匹配筛选结果", "未找到匹配筛选结果，请尝试其他搜索条件。")
        else:
            for info in student_info:
                self.listbox.insert("", "end", values=tuple(str(i) for i in info))

    # 宿舍管理界面
    def create_dormitory_management_widgets(self):
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

        # 创建宿舍管理界面
        query_button = tk.Button(self.function_frame, text="设置宿舍", command=self.query_set_dormitory)
        query_button.place(x=60, y=15)

        add_button = tk.Button(self.function_frame, text="添加宿舍", command=self.add_dormitory)
        add_button.place(x=180, y=15)

        # 默认显示查询界面
        self.query_set_dormitory()

    def on_dorm_query_select(self, event):
        # 获取被选中的item
        selected_item = self.listbox.selection()[0]
        # 获取item的值
        item_values = self.listbox.item(selected_item, "values")
        dorm_id = str(item_values[0])
        stu_count = item_values[1]
        building = item_values[2]
        area = item_values[3]

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
            'SELECT Student_id, stu_name, stu_college, stu_seat '
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
        for i, (student_id, student_name, student_college, stu_seat) in enumerate(student_info, start=0):
            frame_index = i  # 确定当前学生信息应该显示在哪个 Frame 中
            current_frame = [frame1, frame2, frame3, frame4][frame_index]

            # 在当前 Frame 中显示学生信息
            tk.Label(current_frame, text=f"学生{i + 1}").place(x=20, y=0)
            tk.Label(current_frame, text=f"床位号:{stu_seat}").place(x=120, y=0)
            tk.Label(current_frame, text=f"学号: {student_id}").place(x=20, y=20)
            tk.Label(current_frame, text=f"姓名: {student_name}").place(x=120, y=20)
            tk.Label(current_frame, text=f"学院: {student_college}").place(x=20, y=50)
            # 创建删除学生按钮，并为每个按钮传递唯一的学生标识符
            button_delete = tk.Button(current_frame, text="移出宿舍",
                                      command=lambda sid=student_id: delete_student(self.id, sid))
            button_delete.place(x=80, y=70)

        if int(stu_count) < int(dorm_resident):
            button_delete = tk.Button(new_window, text="添加学生",
                                      command=lambda: add_student(self.id, dorm_id))
            button_delete.place(x=175, y=475)
        button_delete = tk.Button(new_window, text="删除宿舍",
                                  command=lambda: delete_dorm(self.id, dorm_id, window=new_window))
        button_delete.place(x=175, y=510)

    def query_set_dormitory(self):
        for widget in self.function_frame_final.winfo_children():
            widget.destroy()

        button_font = font.Font(family="宋体", size=12, weight="bold")
        button_font_big_title = font.Font(family="楷体", size=24, weight="bold")

        canvas = tk.Canvas(self.function_frame_final, width=710, height=600)
        canvas.place(x=0, y=0)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo1)

        # 取消所有按钮的选中状态
        for child in self.function_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.config(relief=tk.RAISED, bg='#ffffff')

        for child in self.function_frame.winfo_children():
            if isinstance(child, tk.Button) and child.cget("text") == "设置宿舍":
                child.config(relief=tk.SUNKEN, bg='pink')

        label0 = tk.Label(self.function_frame_final, text="宿舍筛选：", font=button_font)
        label0.place(x=365, y=50, anchor="center")
        # 创建宿舍号输入框
        dorm_id_label = tk.Label(self.function_frame_final, text="宿舍号：", font=button_font)
        dorm_id_label.place(x=160, y=90)
        self.dorm_id_entry = tk.Entry(self.function_frame_final)
        self.dorm_id_entry.place(x=235, y=90)

        # 创建宿舍楼输入框
        building_label = tk.Label(self.function_frame_final, text="宿舍楼：", font=button_font)
        building_label.place(x=160, y=120)
        self.building_query = tk.Entry(self.function_frame_final)
        self.building_query.place(x=235, y=120)

        # 创建建筑群输入框
        building_area = tk.Label(self.function_frame_final, text="建筑群：", font=button_font)
        building_area.place(x=160, y=150)
        self.area_query = tk.Entry(self.function_frame_final)
        self.area_query.place(x=235, y=150)

        query_button = tk.Button(self.function_frame_final, text="查询（双击记录设置）",
                                 command=self.query_set_dormitory_action,
                                 width=20, height=3,
                                 font=button_font)
        query_button.place(x=400, y=98)

        self.result_frame = tk.Frame(self.function_frame_final, width=400, height=200, bg="white")
        self.result_frame.place(x=170, y=200)
        # 创建竖直滚动条
        scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical")

        # 创建列表框
        self.listbox = ttk.Treeview(self.result_frame, columns=("1", "2", "3", "4"), show="headings",
                                    yscrollcommand=scrollbar.set)

        # 绑定<<TreeviewSelect>>事件,双击进入记录以进一步操作
        self.listbox.bind("<Double-1>", self.on_dorm_query_select)

        # 设置每列的标题
        self.listbox.heading("1", text="宿舍号")
        self.listbox.heading("2", text="人数")
        self.listbox.heading("3", text="宿舍楼")
        self.listbox.heading("4", text="建筑群")

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

        self.scrollable_text = HorizontalScrollText(self.function_frame_final, width=80)
        self.scrollable_text.place(x=100, y=470)

    def query_set_dormitory_action(self):
        dormitory_id = str(self.dorm_id_entry.get())
        building_id = str(self.building_query.get())
        area = str(self.area_query.get())
        print("query_set_dormitory")
        # 获取所有的item,如果存在item，则删除
        items = self.listbox.get_children()
        if items:
            for item in items:
                self.listbox.delete(item)

        cursor = db.cursor()
        self.scrollable_text.clear()

        # 执行数据库查询
        cursor.execute('SELECT building_id, SUM(stu_count) '
                       'FROM dorm natural join dormitory_building '
                       'GROUP BY building_id')
        dormitory_counts = cursor.fetchall()
        db.commit()
        cursor.close()
        cursor = db.cursor()
        cursor.execute(
            'SELECT dormitory_id, stu_count, building_id, building_location '
            'FROM dorm natural join dormitory_building '
            'WHERE dormitory_id LIKE %s AND building_id LIKE %s AND building_location LIKE %s',
            ('%' + dormitory_id + '%', '%' + building_id + '%', '%' + area + '%')
        )
        dorm_info = cursor.fetchall()
        # 将学生信息逐行添加到列表框中
        if not dorm_info:
            messagebox.showinfo("未找到匹配筛选结果", "未找到匹配筛选结果，请尝试其他搜索条件。")
        else:
            for info in dorm_info:
                self.listbox.insert("", "end", values=tuple(str(i) for i in info))
                # 更新文本框内容
            for j, (building_id, count) in enumerate(dormitory_counts):
                self.scrollable_text.append_text(f"宿舍楼 {building_id} 共有 {count} 个学生         ")
            print(dormitory_counts)

    def add_dormitory(self):
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
            if isinstance(child, tk.Button) and child.cget("text") == "添加宿舍":
                child.config(relief=tk.SUNKEN, bg='pink')

        button_font = font.Font(family="宋体", size=12, weight="bold")
        button_font_big_title = font.Font(family="楷体", size=24, weight="bold")

        label = tk.Label(self.function_frame_final, text="添加宿舍：", font=button_font)
        label.place(x=365, y=50, anchor="center")

        dorm_id_label = tk.Label(self.function_frame_final, text="宿舍号：", font=button_font)
        dorm_id_label.place(x=260, y=100)
        self.dorm_id = tk.Entry(self.function_frame_final)
        self.dorm_id.place(x=335, y=100)
        cursor = db.cursor()
        # 从数据库中获取宿舍楼列表
        cursor.execute('SELECT building_id FROM dormitory_building')
        building_options = [building_id[0] for building_id in cursor.fetchall()]
        # 创建宿舍楼下拉框
        building_label = tk.Label(self.function_frame_final, text="宿舍楼：", font=button_font)
        building_label.place(x=260, y=135)
        self.stu_sex_combobox = ttk.Combobox(self.function_frame_final, values=building_options, state="readonly")
        self.stu_sex_combobox.place(x=335, y=135)
        # 创建宿舍参数输入框
        building_label = tk.Label(self.function_frame_final, text="宿舍最大容量：", font=button_font)
        building_label.place(x=218, y=170)
        self.capacity = tk.Entry(self.function_frame_final)
        self.capacity.place(x=345, y=170)

        add_dorm_button = tk.Button(self.function_frame_final, text="添加", command=self.add_dorm_action,
                                    width=20, height=3,
                                    font=button_font)
        add_dorm_button.place(x=270, y=400)

    def add_dorm_action(self):
        # 获取输入的宿舍信息
        dorm_id = self.dorm_id.get()
        building = self.stu_sex_combobox.get()
        capacity = self.capacity.get()

        # 检查输入的容量是否为正整数
        try:
            capacity = int(capacity)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "宿舍容量必须为正整数")
            return

        try:
            cursor = db.cursor()
            # 检查宿舍号是否与已有的宿舍号冲突
            cursor.execute('SELECT * FROM dorm WHERE dormitory_id = %s', (dorm_id,))
            existing_dorm = cursor.fetchone()
            if existing_dorm:
                messagebox.showerror("错误", "宿舍号已存在")
                return

            # 检查宿舍楼是否存在
            cursor.execute('SELECT * FROM dormitory_building WHERE building_id = %s', (building,))
            existing_building = cursor.fetchone()
            if not existing_building:
                messagebox.showerror("错误", "宿舍楼不存在")
                return

            # 添加宿舍
            cursor.execute('INSERT INTO dorm (dormitory_id, building_id, '
                           'dormitory_resident, electricity_balance, stu_count) '
                           'VALUES (%s, %s, %s , 0 , 0)',
                           (dorm_id, building, capacity))

            # 更新宿舍楼的dorm_count属性
            cursor.execute('UPDATE dormitory_building SET dorm_count = dorm_count + 1 WHERE building_id = %s',
                           (building,))

            # 提交事务
            db.commit()

            messagebox.showinfo("成功", "添加宿舍成功")

        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {e}")

    # 个人信息界面,逻辑比较简单，不再详细注释
    def create_admin_information_widgets(self):
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
                       'from dorm_supervisor natural join dormitorystaff '
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
                           'where manager_id = %s', self.id)
            mana_building = cursor.fetchone()[0]
            Label5 = tk.Label(self.function_frame, text="管理宿舍楼: " + str(mana_building), font=button_font_big_title)
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
        cursor.execute('UPDATE dorm_supervisor SET Job_Content = %s WHERE job_number = %s',
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
        for child in self.admin_window.winfo_children():
            if isinstance(child, tk.Button):
                child.config(relief=tk.RAISED, bg='#ffffff')

        if function_name == "学生管理":
            self.create_student_management_widgets()
        elif function_name == "宿舍管理":
            self.create_dormitory_management_widgets()
        elif function_name == "我的信息":
            self.create_admin_information_widgets()

        # 设置当前选中按钮为凹陷状态
        for child in self.admin_window.winfo_children():
            if isinstance(child, tk.Button) and child.cget("text") == function_name:
                child.config(relief=tk.SUNKEN, bg='gold')


# if __name__ == "__main__":
#     admin = AdminSystem("20241315")
#     admin.admin_window.mainloop()
# # admin = AdminSystem(20241311)
