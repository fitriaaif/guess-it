import tkinter as tk
import ai
import numpy as np
from PIL import Image, ImageTk, ImageDraw

model = ai.load_ai()
git 
window = tk.Tk()

img = Image.new(mode="1", size=(500,500), color=0)
tkImage = ImageTk.PhotoImage(img)
canvas = tk.Label(window, image=tkImage)
canvas.pack()

draw = ImageDraw.Draw(img)

last_point = (0,0)
prediction = tk.StringVar()
label = tk.Label(window, textvariable=prediction)

def draw_image(event):
    global last_point, tkImage, prediction
    current_point = (event.x, event.y)
    draw.line([last_point, current_point], fill=255, width=20)
    last_point = current_point
    tkImage = ImageTk.PhotoImage(img)
    canvas['image'] = tkImage
    canvas.pack()
    img_temp = img.resize((28, 28))
    img_temp = np.array(img_temp)
    img_temp = img_temp.flatten()
    output = model.predict([img_temp])

    if (output[0] == 0):
        prediction.set("Kotak")
    elif (output[0] == 1):
        prediction.set("Lingkaran")
    else:
        prediction.set("Segitiga")
    label.pack()

def start_draw(event):
    global last_point
    last_point = (event.x, event.y)

def reset_canvas(event):
    global tkImage, img, draw
    tkImage = ImageTk.PhotoImage(img)
    img = Image.new(mode="1", size=(500,500), color=0)
    draw = ImageDraw.Draw(img)
    canvas['image'] = tkImage
    canvas.pack()

kotak = 0
lingkaran = 0
segitiga = 0

def save_image(event):
    global kotak, lingkaran, segitiga
    img_temp = img.resize((28, 28))
    if (event.char == "k"):
        img_temp.save(f"kotak/{kotak}.png")
        kotak += 1
    elif (event.char == "l"):
        img_temp.save(f"lingkaran/{lingkaran}.png")
        lingkaran += 1
    elif (event.char == "s"):
        img_temp.save(f"segitiga/{segitiga}.png")
        segitiga += 1

window.bind("<B1-Motion>", draw_image)
window.bind("<ButtonPress-1>", start_draw)
window.bind("<ButtonPress-3>", reset_canvas)
window.bind("<Key>", save_image)

window.mainloop()