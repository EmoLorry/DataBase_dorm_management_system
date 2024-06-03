import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter import font
import pymysql

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


def modify_password(admin_id, stu_id):
    # 检查权限
    cursor = db.cursor()
    cursor.execute('SELECT dormitory_id '
                   'FROM student '
                   'WHERE student_id = %s', (stu_id,))
    stu_dorm = cursor.fetchone()
    if stu_dorm[0] is not None:
        cursor.execute('SELECT manager_id '
                       'FROM student_info_with_dorm '
                       'WHERE Student_id = %s', (stu_id,))
        manager_stu = cursor.fetchone()
        print(manager_stu, admin_id)
        # 只有该学生对应宿舍楼的普通管理员和超级管理员才有操作的权限
        if manager_stu[0] == admin_id or admin_id == "88888888":
            cursor = db.cursor()
            cursor.execute('UPDATE student '
                           'SET login_password = %s '
                           'WHERE Student_id = %s', ('123456', stu_id))
            db.commit()  # 提交事务
            messagebox.showinfo("信息提示", f"已重设学号为{stu_id}的学生系统登录密码为123456！")
        else:
            messagebox.showinfo("信息提示", f"重设失败，您不是学号为{stu_id}的学生所在宿舍楼的管理员，您无权进行操作！")
        cursor.close()  # 关闭游标
    elif admin_id == "88888888":
        cursor = db.cursor()
        cursor.execute('UPDATE student '
                       'SET login_password = %s '
                       'WHERE Student_id = %s', ('123456', stu_id))
        db.commit()  # 提交事务
        messagebox.showinfo("信息提示", f"已重设学号为{stu_id}的学生系统登录密码为123456！")
    else:
        messagebox.showinfo("信息提示", f"重设失败，学号为{stu_id}的学生暂未分配宿舍，而您不是一级管理员，无权进行操作！")
        cursor.close()  # 关闭游标


def update_student(admin_id, stu_id):
    # 检查权限
    cursor = db.cursor()
    cursor.execute('SELECT dormitory_id '
                   'FROM student '
                   'WHERE student_id = %s', (stu_id,))
    stu_dorm = cursor.fetchone()
    if stu_dorm[0] is not None:
        cursor.execute('SELECT manager_id '
                       'FROM student_info_with_dorm '
                       'WHERE Student_id = %s', (stu_id,))
        manager_stu = cursor.fetchone()
        print(manager_stu, admin_id)
        # 只有该学生对应宿舍楼的普通管理员和超级管理员才有操作的权限
        if manager_stu[0] == admin_id or admin_id == "88888888":
            create_widget(stu_id)
        else:
            messagebox.showinfo("信息提示",
                                f"操作失败，您不是学号为{stu_id}的学生所在宿舍楼的管理员，您无权进行信息修改操作！")
        cursor.close()  # 关闭游标

    elif admin_id == "88888888":

        create_widget(stu_id)
        cursor.close()  # 关闭游标
    else:
        messagebox.showinfo("信息提示",
                            f"操作失败，您不是学号为{stu_id}的学生所在宿舍楼的管理员，您无权进行信息修改操作！")
        cursor.close()  # 关闭游标


def create_widget(stu_id):
    def update_student_info():
        # 获取输入框中的新值
        new_college = entry_college.get()
        new_name = entry_name.get()

        # 检查字符串长度是否超限
        if len(new_college) > 25:
            messagebox.showerror("错误提示", "所在学院长度超过限制（最多25个字符）！")
            return
        elif len(new_name) > 20:
            messagebox.showerror("错误提示", "姓名长度超过限制（最多20个字符）！")
            return

        # 检查更新后的值是否为空
        if new_college == "" or new_name == "":
            confirm = messagebox.askyesno("确认更新",
                                          "检测到一些更新后的值为空，更新后原有的值将永久性地不能恢复，您是否确定要继续更新？")
            if not confirm:
                return  # 取消更新操作
        else:
            confirm = messagebox.askyesno("确认更新",
                                          "更新后原有的值将永久性地不能恢复，您是否确定要继续更新？")
            if not confirm:
                return  # 取消更新操作
        # 更新数据库中的学生信息
        cursor.execute('UPDATE student '
                       'SET Stu_College = %s, Stu_Name = %s '
                       'WHERE Student_id = %s', (new_college, new_name, stu_id))
        db.commit()
        messagebox.showinfo("信息提示", "学生信息已更新！")

    def after_update_student_info(entry_college, entry_name):
        entry_college.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        cursor.execute('SELECT Stu_College, Stu_Name, Stu_Sex '
                       'FROM student '
                       'WHERE student_id = %s', (stu_id,))
        student_now = cursor.fetchone()
        entry_college.insert(0, str(student_now[0]))
        entry_name.insert(0, str(student_now[1]))

    def remove_student(old_canvas):
        cursor.execute('SELECT dormitory_id '
                       'FROM student '
                       'WHERE student_id = %s', stu_id)
        dorm_id = cursor.fetchone()[0]
        confirm = messagebox.askyesno("确认移出",
                                      "此操作将会把学生从原宿舍中移出，此学生将会变为未分配宿舍状态，是否确认操作？")
        if not confirm:
            return  # 取消更新操作

        try:
            # 开始事务
            db.begin()
            # 更新数据库中的学生信息
            cursor.execute('UPDATE student '
                           'SET dormitory_id = NULL, stu_seat = NULL '
                           'WHERE Student_id = %s', stu_id)
            cursor.execute('SELECT stu_count '
                           'FROM dorm '
                           'WHERE dormitory_id = %s', dorm_id)
            stu_count = cursor.fetchone()[0]
            stu_count = str(int(stu_count) - 1)
            cursor.execute('UPDATE dorm '
                           'SET Stu_count = %s '
                           'WHERE dormitory_id = %s', (stu_count, dorm_id))
            db.commit()
            # U_label_dorm.config(text="宿舍号: None")
            # U_label_seat.config(text="床位号: None")
            # button_delete.destroy()
            # label = tk.Label(canvas, text="新分配安排宿舍", font=button_font_big_title)
            # label.place(x=345, y=0)
            messagebox.showinfo("信息提示", "学生信息已更新！")
            new_window.destroy()
            create_widget(stu_id)

        # 发生异常时回滚事务
        except Exception as e:
            db.rollback()
            messagebox.showerror("错误提示", f"移出学生操作失败：{str(e)}")

    def change_seat_action(stu_dorm, new_seat, old_canvas):
        cursor.execute('SELECT dormitory_resident '
                       'FROM dorm '
                       'WHERE dormitory_id = %s', (stu_dorm,))
        cap = int(cursor.fetchone()[0])
        if new_seat.strip() == "":
            messagebox.showerror("错误提示", "请输入不为空的床位号！")
            return
        if not new_seat.isdigit():
            messagebox.showerror("错误提示", "床位号必须为整数！")
            return
        # 检查新的床位号是否在有效范围内
        if not (1 <= int(new_seat) <= cap):
            messagebox.showerror("错误提示", f"该宿舍人数容量为{cap}，新的床位号必须在1到{cap}之间！")
            return

        cursor.execute('SELECT stu_seat '
                       'FROM student '
                       'WHERE student_id = %s', (stu_id,))
        old_seat = cursor.fetchone()[0]
        print(old_seat, stu_dorm, new_seat)
        if str(old_seat) == str(new_seat):
            messagebox.showerror("错误提示", f"修改学生床位号失败：请输入与原床位号不同的床位！")
            return
        cursor.execute('SELECT count(*) from student '
                       'WHERE dormitory_id = %s and stu_seat =%s', (stu_dorm, str(new_seat)))
        count = cursor.fetchone()[0]
        if count == 0:
            try:
                # 开始事务
                db.begin()
                # 更新数据库中的学生seat信息
                cursor.execute('UPDATE student '
                               'SET Stu_seat = %s '
                               'WHERE student_id = %s', (new_seat, stu_id))
                db.commit()
                # label = tk.Label(old_canvas, text="床位号: " + str(new_seat))
                # label.place(x=410, y=50)
                messagebox.showinfo("信息提示", "学生信息已更新！")
                new_window.destroy()
                create_widget(stu_id)

            # 发生异常时回滚事务
            except Exception as e:
                db.rollback()
                messagebox.showerror("错误提示", f"修改学生床位号失败：{str(e)}")
        else:
            messagebox.showerror("错误提示", f"修改学生床位号失败：床位占有冲突！")

    def change_dorm(new_dorm, new_seat, old_canvas):
        if new_seat.strip() == "":
            messagebox.showerror("错误提示", "请输入不为空的床位号！")
            return
        if not new_seat.isdigit():
            messagebox.showerror("错误提示", "床位号必须为整数！")
            return
        cursor.execute('SELECT stu_sex FROM student '
                       'WHERE student_id = %s ', stu_id)
        sex = cursor.fetchone()[0]
        # 只考虑男女两种性别
        if sex != "男" and sex != "女":
            messagebox.showerror("错误提示", f"请明确该学生性别后再操作！可以在基本信息修改栏目中设置")
            return
        # ----------------------------------------------------------------
        # 使用储存控制下的更新操作
        # 该操作主要完成的是更新dorm表stu_count属性
        # 以及student表中的dormitory_id属性，
        # 该存储过程接受新宿舍号、安排床位号为输入参数，
        # 来完成dormitory_id属性与原宿舍stu_count减1和新宿舍stu_count加1的更新。
        # 在更新之前，
        # 会先检查宿舍号输入是否存在，
        # 然后检查新宿舍stu_count属性是否等于dormitory_count属性，
        # 再检查转入的宿舍所在宿舍楼的性别是否与当前学生性别一致，
        # 再检查输入的整数床位号是否在1到新宿舍最大人数容量之间，
        # 最后再检查提交的床位号是否与原有床位号冲突，
        # 当这五个条件判断依次为：true、false、true、true、false
        # 才成功执行转宿舍操作，
        # 否则抛出错误。
        # --------------------------------------------------------
        # 确保参数类型
        new_dorm = str(new_dorm)
        new_seat = int(new_seat)
        # print(stu_id)
        # print(type(stu_id))

        try:
            # 执行存储过程
            cursor.callproc("change_dorm_proc", (new_dorm, new_seat, stu_id, None))

            messagebox.showinfo("信息提示", "学生信息已更新！")
            new_window.destroy()
            create_widget(stu_id)

        except Exception as e:
            # 捕获可能的异常并进行处理
            messagebox.showerror("错误提示", f"执行存储过程时出错：{str(e)}")

    def arr_dorm(dorm, seat, old_canvas):
        pass

    new_window = tk.Toplevel()
    new_window.title("更新学生信息")
    window_width = 600
    window_height = 400
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    button_font_big_title = font.Font(family="楷体", size=24, weight="bold")
    canvas = tk.Canvas(new_window, width=600, height=400)
    canvas.place(x=0, y=0)
    line = canvas.create_line(300, 0, 300, 400)
    canvas.itemconfig(line, fill="green", width=3)
    line1 = canvas.create_line(305, 270, 595, 270)
    canvas.itemconfig(line1, fill="red", width=3)

    U_label = tk.Label(canvas, text="基本信息修改", font=button_font_big_title)
    U_label.place(x=50, y=0)

    cursor = db.cursor()
    cursor.execute('SELECT Stu_College, Stu_Name, Stu_Sex, dormitory_id, stu_seat '
                   'FROM student '
                   'WHERE student_id = %s', (stu_id,))
    student_info = cursor.fetchone()

    # 显示学院、姓名和性别信息
    tk.Label(new_window, text="学院: ").place(x=50, y=50)
    entry_college = tk.Entry(new_window)
    entry_college.insert(0, str(student_info[0]))
    entry_college.place(x=100, y=50)

    tk.Label(new_window, text="姓名: ").place(x=50, y=100)
    entry_name = tk.Entry(new_window)
    entry_name.insert(0, str(student_info[1]))
    entry_name.place(x=100, y=100)

    if student_info[3] is None:

        U_label = tk.Label(canvas, text="在宿舍管理模块\n"
                                        "选择“添加学生”\n"
                                        "给该学生安排宿舍", font=button_font_big_title)
        U_label.place(x=320, y=0)

    else:
        U_label = tk.Label(canvas, text="更换床位或宿舍", font=button_font_big_title)
        U_label.place(x=345, y=0)

        U_label_dorm = tk.Label(canvas, text="宿舍号: " + str(student_info[3]))
        U_label_dorm.place(x=410, y=80)
        U_label_seat = tk.Label(canvas, text="床位号: " + str(student_info[4]))
        U_label_seat.place(x=410, y=50)

        # 创建标签和输入框
        new_seat_self = tk.Label(new_window, text="新床位号: ")
        new_seat_self.place(x=350, y=170)
        entry_new_seat = tk.Entry(new_window)
        entry_new_seat.place(x=420, y=170)

        button_change_seat = tk.Button(new_window, text="更换床位",
                                       command=lambda: change_seat_action(student_info[3],
                                                                          str(entry_new_seat.get()),
                                                                          canvas))
        button_change_seat.place(x=420, y=210)

        # 创建标签和输入框
        new_dorm_with_dorm = tk.Label(new_window, text="新宿舍号: ")
        new_dorm_with_dorm.place(x=350, y=290)
        entry_new_dorm = tk.Entry(new_window)
        entry_new_dorm.place(x=420, y=290)

        # 创建标签和输入框
        new_seat_with_dorm = tk.Label(new_window, text="新床位号: ")
        new_seat_with_dorm.place(x=350, y=320)
        entry_new_seat_with_dorm_changed = tk.Entry(new_window)
        entry_new_seat_with_dorm_changed.place(x=420, y=320)

        button_change_dorm = tk.Button(new_window, text="更换宿舍",
                                       command=lambda: change_dorm(str(entry_new_dorm.get()),
                                                                   str(entry_new_seat_with_dorm_changed.get()),
                                                                   canvas, ))
        button_change_dorm.place(x=420, y=350)

        button_delete = tk.Button(new_window, text="移出宿舍", command=lambda: remove_student(canvas))
        button_delete.place(x=120, y=350)

    button_update = tk.Button(new_window, text="更新信息",
                              command=lambda: [update_student_info(),
                                               after_update_student_info(entry_college, entry_name)])
    button_update.place(x=120, y=200)
    new_window.mainloop()


# ----------------------------------------------------------------
# 从宿舍移出学生，隶属于宿舍管理模块，
# ----------------------------------------------------------------

def delete_student(admin_id, stu_id):
    # 检查权限
    cursor = db.cursor()
    cursor.execute('SELECT dormitory_id '
                   'FROM student '
                   'WHERE student_id = %s', (stu_id,))
    stu_dorm = cursor.fetchone()
    cursor.execute('SELECT manager_id '
                   'FROM student_info_with_dorm '
                   'WHERE Student_id = %s', (stu_id,))
    manager_stu = cursor.fetchone()
    print(manager_stu, admin_id)
    # 只有该学生对应宿舍楼的普通管理员和超级管理员才有操作的权限
    if manager_stu[0] == admin_id or admin_id == "88888888":
        delete_student_action(stu_id, stu_dorm)
        messagebox.showinfo("操作成功", f"成功将学号为{stu_id}的学生移出宿舍{stu_dorm}")
    else:
        messagebox.showinfo("信息提示",
                            f"操作失败，您不是学号为{stu_id}的学生所在宿舍楼的管理员，您无权进行信息修改操作！")
    cursor.close()  # 关闭游标


def delete_student_action(stu_id, stu_dorm):
    cursor = db.cursor()
    cursor.execute('update student '
                   'set dormitory_id = NULL,'
                   'stu_seat = NULL '
                   'where student_id =%s', stu_id)
    cursor.execute('update dorm '
                   'set stu_count = stu_count -1 '
                   'where dormitory_id =%s', stu_dorm)
    db.commit()


# ----------------------------------------------------------------
# 添加学生，隶属于宿舍管理模块，
# ----------------------------------------------------------------

def add_student(admin_id, dorm_id):
    # 检查权限
    cursor = db.cursor()
    cursor.execute('SELECT manager_id '
                   'FROM dorm natural join dormitory_building '
                   'WHERE dormitory_id = %s', (dorm_id,))
    manager_stu = cursor.fetchone()
    print(manager_stu, admin_id)
    # 只有该学生对应宿舍楼的普通管理员和超级管理员才有操作的权限
    if manager_stu[0] == admin_id or admin_id == "88888888":
        create_add_student_widget(dorm_id)
    else:
        messagebox.showinfo("信息提示", f"您不是宿舍号为{dorm_id}的学生所在宿舍楼的管理员，您无权进行操作！")
    cursor.close()  # 关闭游标


def create_add_student_widget(stu_dorm):
    add_student_window = tk.Toplevel()
    add_student_window.geometry('500x300')  # Set window size to 800x600
    add_student_window.title('Add Student')
    button_font = ('Arial', 12)  # Define the font
    button_font = font.Font(family="宋体", size=12, weight="bold")

    # 创建学号输入框
    stu_id_label = tk.Label(add_student_window, text="学号：", font=button_font)
    stu_id_label.place(x=160, y=50)
    stu_id = tk.Entry(add_student_window)
    stu_id.place(x=220, y=50)

    # 创建宿舍床位输入框
    name_label = tk.Label(add_student_window, text="床位号：", font=button_font)
    name_label.place(x=150, y=100)
    stu_seat = tk.Entry(add_student_window)
    stu_seat.place(x=220, y=100)

    add_button = tk.Button(add_student_window, text="添加",
                           command=lambda: add_student_action(
                               stu_id.get(),
                               stu_seat.get(),
                               stu_dorm,
                               add_student_window),
                           width=20, height=3, font=button_font)
    add_button.place(x=160, y=150)


def add_student_action(stu_id, stu_seat, stu_dorm, add_student_window):
    cursor = db.cursor()
    cursor = db.cursor()
    cursor.execute('SELECT count(*) FROM '
                   'student '
                   'WHERE dormitory_id is not NULL and student_id = %s', (stu_id,))
    reason = cursor.fetchone()[0]
    if reason == 1:
        messagebox.showerror("添加失败", f"该学生已经分配宿舍！")
        add_student_window.destroy()
        return
    cursor.execute('select count(*) from student '
                   'where dormitory_id = %s and stu_seat = %s', (stu_dorm, stu_seat))
    count = int(cursor.fetchone()[0])
    cursor.execute('select dormitory_resident from dorm '
                   'where dormitory_id = %s ', stu_dorm)
    capacity = int(cursor.fetchone()[0])

    if stu_seat.isdigit():  # 检查床位号是否为数字
        seat = int(stu_seat)
        if 1 <= seat <= capacity:
            if count == 0:
                try:
                    # Insert student record into the student table
                    cursor.execute('''
                           update student 
                           set dormitory_id = %s, 
                           stu_seat = %s 
                           where student_id = %s
                       ''', (stu_dorm, stu_seat, stu_id))

                    # Update the stu_count in the dorm table
                    cursor.execute('''
                           UPDATE dorm
                           SET stu_count = stu_count + 1
                           WHERE dormitory_id = %s
                       ''', (stu_dorm,))

                    # Commit the transaction
                    db.commit()
                    messagebox.showinfo("添加成功", f"你已成功向宿舍{stu_dorm}添加一位学生！")
                    print("Student added successfully.")

                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                messagebox.showerror("添加失败", f"床位冲突，请重试！")
        else:
            messagebox.showerror("添加失败", f"床位不合法！")
    else:
        messagebox.showerror("添加失败", f"请输入整数！")
    add_student_window.destroy()


def delete_dorm(admin_id, dorm_id, window):
    # 检查权限
    cursor = db.cursor()
    cursor.execute('SELECT manager_id '
                   'FROM dorm natural join dormitory_building '
                   'WHERE dormitory_id = %s', (dorm_id,))
    manager_id = cursor.fetchone()[0]

    if admin_id == "88888888":
        # 超级管理员有权限删除任何宿舍
        # 进行删除操作
        delete_dorm_action(dorm_id, window)

    elif manager_id is None:
        messagebox.showinfo("信息提示", f"宿舍号为{dorm_id}的宿舍不存在或者没有分配管理员！")
    else:
        # 只有对应宿舍楼的普通管理员才有操作的权限
        if admin_id == manager_id:
            # 进行删除操作
            delete_dorm_action(dorm_id, window)

        else:
            messagebox.showinfo("信息提示",
                                f"操作失败，您不是宿舍号为{dorm_id}的学生所在宿舍楼的管理员，您无权进行信息修改操作！")

    cursor.close()  # 关闭游标


def delete_dorm_action(dorm_id, window):
    try:
        # 创建游标对象
        cursor = db.cursor()
        # 执行储存过程
        dorm_id = str(dorm_id)

        cursor.callproc("delete_dorm_procedure", [dorm_id])
        # 提交
        db.commit()
        messagebox.showinfo("信息提示", f"宿舍{dorm_id}删除成功！")
        window.destroy()
        print(f"宿舍{dorm_id}删除成功！")

    except Exception as e:
        # 捕获可能的异常并进行处理
        messagebox.showerror("错误提示", f"执行删除事务过程中出错，已回滚：{str(e)}")


# if __name__ == "__main__":
#     create_widget("2510009")
#     # create_widget("2552523")
