import tkinter as tk
from tkinter import *
from tkinter import filedialog
import numpy as np
from PIL import Image
from PIL import ImageTk
from Filter import filter
from carv import carv
import imageio
import matplotlib
matplotlib.use('TkAgg')


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)


def hide_me(event):
    event.widget.pack_forget()


class MainView(tk.Frame):
    global filename
    global e1
    global e2
    data = np.zeros((100, 100, 3))
    global_img = Image.fromarray(data, 'RGB')
    entry1 = 0
    entry2 = 0

    def opening_pic(self):
        print("Opening a picture!")
        global filename
        global global_img
        filename = filedialog.askopenfilename()
        global_img = Image.open(filename)
        img_data = np.asarray(global_img)
        file = ImageTk.PhotoImage(global_img)

        if img_data.ndim == 3:
            ht, wt, color = img_data.shape
        else:
            ht, wt = img_data.shape
        if (ht > wt and ht > 800):
            global_img = global_img.resize((int(wt * 780 / ht), 780))
            print("first hw: ", ht)
            print("first wt: ", wt)
        if (wt > ht and wt > 800):
            global_img = global_img.resize((780, int(780 * ht / wt)))
            print("first hw: ", ht)
            print("first wt: ", wt)

        global canvas
        canvas = Canvas(root, height=ht, width=wt)
        canvas.image = file  # file is photoimage

        # create image through passing in photo_object
        canvas.create_image(0, 0, anchor='nw', image=file)
        canvas.pack(side="bottom", fill="both", expand="yes")

    def opening_pic_sharp(self):
        print("Opening a picture!")

        global global_img
        img_data = np.asarray(global_img)

        ht, wt, color = img_data.shape
        if (ht > wt and ht > 800):
            global_img = global_img.resize((int(wt * 780 / ht), 780))
            print("second hw: ", ht)
            print("second wt: ", wt)
        if (wt > ht and wt > 800):
            global_img = global_img.resize((780, int(780 * ht / wt)))
            print("second hw: ", ht)
            print("second wt: ", wt)
        # filter and return image matrix
        sharpened_image = filter(img_data, 'sharpen')
        # convert image matrix into image object
        sharpened_image_object = Image.fromarray(sharpened_image)

        # convert image object into photoimage
        file = ImageTk.PhotoImage(sharpened_image_object)
        print("test")
        global canvas
        canvas.image = file  # file is photoimage
        canvas.itemconfig(file)
        # create image through passing in photo_object
        canvas.create_image(0, 0, anchor='nw', image=file)
        canvas.pack(side="bottom", fill="both", expand="yes")

        # update global image which is an image object
        global_img = sharpened_image_object

    def opening_pic_blur(self):
        print("Opening a picture!")

        global global_img
        img_data = np.asarray(global_img)

        ht, wt, color = img_data.shape
        if (ht > wt and ht > 800):
            global_img = global_img.resize((int(wt * 780 / ht), 780))
        if (wt > ht and wt > 800):
            global_img = global_img.resize((780, int(780 * ht / wt)))
        # filter and return image matrix
        blurred_image = filter(img_data, 'blur')
        # convert image matrix into image object
        blurred_image_object = Image.fromarray(blurred_image)

        # convert image object into photoimage
        file = ImageTk.PhotoImage(blurred_image_object)
        print("test")
        global canvas
        canvas.image = file  # file is photoimage
        canvas.itemconfig(file)
        # create image through passing in photo_object
        canvas.create_image(0, 0, anchor='nw', image=file)
        canvas.pack(side="bottom", fill="both", expand="yes")

        # update global image which is an image object
        global_img = blurred_image_object

    def opening_pic_unsharp(self):
        print("Opening a picture!")

        global global_img
        img_data = np.asarray(global_img)

        ht, wt, color = img_data.shape
        if (ht > wt and ht > 800):
            global_img = global_img.resize((int(wt * 780 / ht), 780))
        if (wt > ht and wt > 800):
            global_img = global_img.resize((780, int(780 * ht / wt)))

        # filter and return image matrix
        sharpened_image = filter(img_data, 'unsharp')
        # convert image matrix into image object
        sharpened_image_object = Image.fromarray(sharpened_image)

        # convert image object into photoimage
        file = ImageTk.PhotoImage(sharpened_image_object)
        print("test")
        global canvas
        canvas.image = file  # file is photoimage
        canvas.itemconfig(file)
        # create image through passing in photo_object
        canvas.create_image(0, 0, anchor='nw', image=file)
        canvas.pack(side="bottom", fill="both", expand="yes")

        # update global image which is an image object
        global_img = sharpened_image_object

    def carv_pic(self):
        global entry1
        global entry2
        global e1
        global e2
        global global_img
        global canvas
        entry1 = e1.get()
        data = np.asarray(global_img)
        entry2 = e2.get()
        print(entry1)
        print(entry2)
        carved_arr, T = carv(np.uint8(data), int(entry1), int(entry2))

        # convert image object into photoimage
        carved_image = Image.fromarray(carved_arr, 'RGB')
        file = ImageTk.PhotoImage(carved_image)
        canvas.image = file  # file is photoimage
        canvas.itemconfig(file)
        # create image through passing in photo_object
        canvas.create_image(0, 0, anchor='nw', image=file)
        canvas.pack(side="bottom", fill="both", expand="yes")

        # update global image which is an image object
        global_img = carved_image

    def save(self):
        global global_img
        #global_img = Image.open(filename)
        global_img.save(filename + "_New.jpg", 'JPEG')

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", expand=True)

        p1.place(in_=container, x=10, y=1000, relwidth=10, relheight=10)
        p2.place(in_=container, x=10, y=1000, relwidth=10, relheight=10)

        b1 = tk.Button(buttonframe, text="Open")
        b1["command"] = self.opening_pic
        b3 = tk.Button(buttonframe, text="Sharpen")
        b3["command"] = self.opening_pic_sharp
        b4 = tk.Button(buttonframe, text="Blur")
        b4["command"] = self.opening_pic_blur
        b5 = tk.Button(buttonframe, text="'Unsharp' Mask")
        b5["command"] = self.opening_pic_unsharp

        global e1
        global rows
        global e2
        global columns
        e1 = tk.Entry(buttonframe, text="rows", width=4)
        e2 = tk.Entry(buttonframe, text="column", width=4)
        e1.pack(side="right")
        e2.pack(side="right")
        b6 = tk.Button(buttonframe, text="Resize")
        b6.pack(side="right")
        b6["command"] = self.carv_pic

        b7 = tk.Button(buttonframe, text="Save")
        b7["command"] = self.save

        b1.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")
        b5.pack(side="left")
        b7.pack(side="left")

        p1.show()


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x800")
    root.mainloop()
