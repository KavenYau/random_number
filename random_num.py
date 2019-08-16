# *_*coding:utf-8 *_*
# Created by Kaven on 2019/3/29.
import random
import threading
import tkinter

import time
from PIL import ImageTk, Image


Version = '1.0.0'
running = True
generate_number = False
number_had_got = set()


def change_generate_number(*args):
    global generate_number, running, number_had_got
    generate_number = not generate_number
    if generate_number:
        btn_var.set('Stop')
    else:
        btn_var.set('Start')
        number_had_got.add(ret_number.get())
        print('had got number:', number_had_got)


def random_number_handler():
    global generate_number, running, number_had_got
    while running:
        # print(generate_number)
        time.sleep(0.01)
        if generate_number:
            number = random.randint(from_num.get(), to_num.get())
            if number in number_had_got:
                continue
            ret_number.set(number)


if __name__ == '__main__':
    root = tkinter.Tk()
    img_path = r'image/bg.jpg'
    icon_path = r'image/favicon.ico'
    from_num = tkinter.IntVar()
    to_num = tkinter.IntVar()
    ret_number = tkinter.IntVar()
    btn_var = tkinter.StringVar()
    to_num.set(38)
    from_num.set(1)
    btn_var.set('Start')

    root.title('学号抽号器 V{0} by Kaven'.format(Version))
    root.iconbitmap(icon_path)

    img = Image.open(img_path)
    photo = ImageTk.PhotoImage(img)
    canvas = tkinter.Canvas(root, width=photo.width(), height=photo.height(), bd=0, highlightthickness=0)
    canvas.create_image(photo.width() / 2, photo.height() / 2, image=photo)
    canvas.pack()

    number_label = tkinter.Label(root, textvariable=ret_number, background='white', font=('Arial', 120))
    number_label.pack()
    canvas.create_window(photo.width() / 2 + 5, photo.height() / 2 + 70, width=200, height=200,
                         window=number_label)

    fm1 = tkinter.Frame(root)
    num_from_entry = tkinter.Entry(fm1, textvariable=from_num, width=10)
    num_from_label = tkinter.Label(fm1, text='number from: ')
    num_from_label.pack(side=tkinter.LEFT, expand=tkinter.YES)
    num_from_entry.pack(side=tkinter.LEFT, expand=tkinter.YES)
    num_to_entry = tkinter.Entry(fm1, textvariable=to_num, width=10)
    num_to_label = tkinter.Label(fm1, text='number to: ')
    num_to_label.pack(side=tkinter.LEFT, expand=tkinter.YES)
    num_to_entry.pack(side=tkinter.LEFT, expand=tkinter.YES)
    ctl_btn = tkinter.Button(fm1, text='Start',font=('Arial', 12), textvariable=btn_var, command=change_generate_number,
                             width=20)
    ctl_btn.pack(side=tkinter.LEFT, expand=tkinter.YES)
    fm1.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)

    th = threading.Thread(target=random_number_handler)
    th.start()

    root.mainloop()
    running = False
    th.join()
