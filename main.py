BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas
import random

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")

to_learn = data.to_dict(orient="records")
print(len(to_learn))
index = 0

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=1, column=1, columnspan=2)
canvas_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "italic"))


def edit():
    global flip_timer, index
    window.after_cancel(flip_timer)
    index = random.randint(0, len(to_learn) - 1)
    french_word = to_learn[index]["French"]
    canvas.itemconfig(canvas_word, text=french_word, fill="black")
    canvas.itemconfig(canvas_title, text="French", fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    flip_timer = window.after(3000, english_card)


def english_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(canvas_title, text="English", fill="white")
    english_word = to_learn[index]["English"]
    canvas.itemconfig(canvas_word, text=english_word, fill="white")


def is_known():
    to_learn.remove(to_learn[index])
    df = pandas.DataFrame(to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)
    edit()

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=edit)
wrong_button.grid(row=2, column=1)

correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, highlightthickness=0, command=is_known)
correct_button.grid(row=2, column=2)

flip_timer = window.after(3000, func=english_card)
edit()

window.mainloop()
