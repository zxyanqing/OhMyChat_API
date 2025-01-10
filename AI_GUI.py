# -*- encoding: utf-8 -*-
'''
@Project_name    :  gui_test
@ProjectDescription: ..........
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/9/4 9:35     zxy       1.0         None
'''
import datetime
import threading
import tkinter as tk
import traceback

class MyThread(threading.Thread):
    """新增线程在GUI界面打印功能"""
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)
class AIGUI():
    def __init__(self):
        self.window_width, self.window_height = 800, 120
        self.history_content = """"""

    def build_root(self):
        """
            创建界面对象
        :return:
        """
        root = tk.Tk()
        root.title("AI chatBox")
        root.geometry('800x1200+10+10')
        root.resizable(False, True)  # 设置界面是否可以随意拉伸
        root.attributes("-alpha", 0.8)  # 设置透明度
        root.after(1000)
        return root

    def run_gui(self):
        global question_word, answer_word
        root = self.build_root()
        # 创建问题提示行
        question = tk.Label(root, text="USER (Only you can't think of it):")
        question.grid(row=0, column=0, sticky=tk.W, columnspan=5)
        # 创建问题输入框
        question_word = tk.Text(root, width=108, height=10)
        question_word.grid(row=1, column=0, columnspan=5)
        # 创建回复提示行
        answer = tk.Label(root, text="AI (Without it, I can't do it):")
        answer.grid(row=3, column=0, sticky=tk.W, columnspan=5)
        # 创建回复输入框
        answer_word = tk.Text(root, width=108, height=60)
        answer_word.grid(row=4, column=0, columnspan=5)

        def submit_button_run(is_need_clear=True):
            """提交按钮事件"""
            query = str(question_word.get(1.0, tk.END))
            if query == "\n":
                answer_word.delete(1.0, tk.END)
                text = "Please enter content"
                answer_word.insert(tk.END, text)
                return
            if is_need_clear:
                answer_word.delete(1.0, tk.END)
            print(f"User({str(datetime.datetime.now())[:19]}):" + query)
            answer_word.insert(tk.END, f"User({str(datetime.datetime.now())[:19]}):" + query + "\n")
            try:
                for line_data, index in self.get_qiuyu_chat3_api(query):
                    for text, is_warp in self.handler_qiuyu_chat3_api_result(line_data, index):
                        if is_warp:
                            if text is not None:
                                print(text)
                                answer_word.insert(tk.END, text + "\n")
                        else:
                            print(text, end="")
                            answer_word.insert(tk.END, text)
            except:
                traceback.print_exc()
                erro_text = "There is a problem with your API interface !!!"
                print(erro_text)
                answer_word.insert(tk.END, erro_text)

            self.history_content += "\n" + str(answer_word.get(1.0, tk.END))

        def clear_button_run():
            """清除按钮事件"""
            question_word.delete(1.0, tk.END)

        def history_button_run():
            """历史记录事件"""
            answer_word.delete(1.0, tk.END)
            answer_word.insert(tk.END, self.history_content)

        # 提交按钮
        submit_button = tk.Button(
            root,
            text="Submit",
            command=lambda :MyThread(submit_button_run))
        submit_button.grid(row=2, column=1, sticky=tk.N + tk.W + tk.W + tk.E)
        # 清除按钮
        clear_button = tk.Button(
            root,
            text="Clear",
            command=clear_button_run)
        clear_button.grid(row=2, column=2, sticky=tk.N + tk.W + tk.W + tk.E)
        # 历史记录按钮
        history_button = tk.Button(
            root,
            text="History",
            relief=tk.GROOVE,
            command=lambda :MyThread(history_button_run))
        history_button.grid(row=2, column=3)

        root.mainloop()


if __name__ == '__main__':
    X = AIGUI()
    X.run_gui() # Only you can't think of it. Without it, I can't do it
