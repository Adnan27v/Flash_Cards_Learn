from tkinter import *
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT=("Arial",40,"italic")
WORD_FONT=("Arial",60,"bold")
current_card = {}
to_learn = {}

try:
    data = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # Creates a list of dictionaries where each dictionary is a card containing French and English translation
    to_learn = data.to_dict(orient="records")


def random_french_word():

    global current_card,timer
    window.after_cancel(timer)
    current_card = choice(to_learn)

    canvas.itemconfig(image, image=card_front_image)
    canvas.itemconfig(language, text=f"French",fill="black")
    canvas.itemconfig(word,text=f"{current_card["French"]}",fill="black")

    timer = window.after(3000, func=english_translation)

def english_translation():
    canvas.itemconfig(image,image=card_back_image)
    canvas.itemconfig(language,text="English",fill="white")
    canvas.itemconfig(word, text=f"{current_card["English"]}",fill="white")

def is_known():
    """Removes the known word from to learn list and saves the rest to to_learn words csv"""

    to_learn.remove(current_card)
    random_french_word()

    data1 = pd.DataFrame(to_learn)
    data1.to_csv("data/words_to_learn.csv",index=False)

window = Tk()
window.title("Flashcards")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)

timer = window.after(3000, func=english_translation)

canvas = Canvas(width=800,height=526,bg=BACKGROUND_COLOR,highlightthickness=0)

#Image on canvas
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
image = canvas.create_image(400,263,image=card_front_image)

#texts on canvas
language = canvas.create_text(400,150,text="",font=LANGUAGE_FONT)
word = canvas.create_text(400,263,text="",font=WORD_FONT)

canvas.grid(row=0,column=0,columnspan=2)

#Right/Tick Button
tick_image = PhotoImage(file="./images/right.png")
tick = Button(image=tick_image, highlightthickness = 0,command=is_known)
tick.grid(row=1,column=1)

#Wrong/Cross Button
cross_image = PhotoImage(file="./images/wrong.png")
cross = Button(image=cross_image, highlightthickness=0,command=random_french_word)
cross.grid(row=1,column=0)

random_french_word()

window.mainloop()