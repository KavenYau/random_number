# *_*coding:utf-8 *_*
# Created by Kaven on 2019/3/29.
import random
import threading
import tkinter
import time
import configparser
from PIL import ImageTk, Image


Version = '1.0.1'
running = True
generate_number = False
number_had_got = set()
config_file_name = 'config.ini'

def change_generate_number(*args):
    global generate_number, running, number_had_got
    generate_number = not generate_number
    if generate_number:
        btn_var.set('Stop')
    else:
        btn_var.set('Start')
        number_had_got.add(ret_number.get())
        print('had got number:', number_had_got)
    save_config(config_file_name)

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


def reset_record_numbers(*arg):
    global number_had_got
    number_had_got.clear()
    print('reset record numbers, now had got number:', number_had_got)


def config_option_read(config, section, key, default_value):
    while True:
        try:
            return config.get(section, key)
        except configparser.NoSectionError:
            print('no section {}, create it'.format(section))
            config.add_section(section)
        except configparser.NoOptionError:
            print('no key {} in section {}, create it'.format(key, section))
            config.set(section, key, default_value)
            return default_value
         

def config_option_write(config, section, key, default_value):
    while True:
        try:
            config.set(section, key, default_value)
            return True
        except configparser.NoSectionError:
            print('no section {}, create it'.format(section))
            config.add_section(section)


def config_init(file_name):
    global from_num_from_config, to_num_from_config
    # try:
    #     config.add_section("Home")
    #     config.set("Home", "IP", "10.12.23.56")
    #     config.set("Home", "Mask", "255.255.255.0")
    # except configparser.DuplicateSectionError:
    #     print("Section 'Home' already exists")

    # config.write(open(file_name, "w"))\
     # try:
    config.read(file_name)
    from_num_from_config = config_option_read(config, "Commom", "from_num", "1")
    to_num_from_config = config_option_read(config, "Commom", "to_num", "43")
    config.write(open(file_name, "w"))


def save_config(file_name):
    global from_num_from_config, to_num_from_config
    from_num_get = from_num.get()
    change = False
    if from_num_get != from_num_from_config:
        config.set("Commom", "from_num", str(from_num_get))
        from_num_from_config = from_num_get
        change = True

    to_num_get = to_num.get()
    if to_num_get != to_num_from_config:
        config.set("Commom", "to_num", str(to_num_get))
        to_num_from_config = to_num_get
        change = True

    if change:
        config.write(open(file_name, "w"))


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config_init(config_file_name)
    # config.read(config_file_name)
    # from_num_from_config = config_read(config, "Commom", "from_num", "1")
    # to_num_from_config = config_read(config, "Commom", "to_num", "43")
    # config.write(open(config_file_name, "w"))

    root = tkinter.Tk()
    img_path = r'image/bg.jpg'
    icon_path = r'image/favicon.ico'
    from_num = tkinter.IntVar()
    to_num = tkinter.IntVar()
    ret_number = tkinter.IntVar()
    btn_var = tkinter.StringVar()
    to_num.set(to_num_from_config)
    from_num.set(from_num_from_config)
    btn_var.set('Start')
    reset_btn_var = tkinter.StringVar()
    reset_btn_var.set('Reset')

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
    reset_btn = tkinter.Button(fm1, text='Reset',font=('Arial', 12), textvariable=reset_btn_var, command=reset_record_numbers,
                             width=10)
    ctl_btn = tkinter.Button(fm1, text='Start',font=('Arial', 12), textvariable=btn_var, command=change_generate_number,
                             width=10)
    reset_btn.pack(side=tkinter.LEFT, expand=tkinter.YES)
    ctl_btn.pack(side=tkinter.LEFT, expand=tkinter.YES)
    fm1.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=tkinter.YES)

    th = threading.Thread(target=random_number_handler)
    th.start()

    root.mainloop()
    running = False
    th.join()
