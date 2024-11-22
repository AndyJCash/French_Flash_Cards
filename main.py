from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
data_dict = data.to_dict(orient="records")
new_word_pair = {}


def generate_word():
    """Resets the 3-second timer and generates a new word-translation pair. Displays new word on front of card."""
    global new_word_pair, flip_timer
    window.after_cancel(flip_timer)
    new_word_pair = random.choice(data_dict)
    new_word = new_word_pair["French"]
    new_translation = new_word_pair["English"]
    canvas.itemconfig(card_image, image=flashcard_front_image)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=new_word, fill="black")
    flip_timer = window.after(3000, flip_card, new_translation)


def flip_card(english_word):
    """Changes flash card to the back of the card, where the English translation is displayed"""
    canvas.itemconfig(card_image, image=flashcard_back_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=english_word, fill="white")


def word_learned():
    """Removes current word-translation pair from old csv file (words to be tested) and adds it to a new csv file.
    Also updates pool of words to be tested on flashcards so current word-translation pair no longer appears."""
    with open("data/learned_words.csv", "a") as file:
        file.write(f"{new_word_pair['French']}, {new_word_pair['English']}\n")
    data_dict.remove(new_word_pair)
    words_to_learn = pandas.DataFrame(data_dict)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    generate_word()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flashcard_front_image = PhotoImage(file="images/card_front.png")
flashcard_back_image = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=flashcard_front_image)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
cross = Button(image=cross_image, bd=0, bg="grey", command=generate_word)
cross.grid(column=0, row=1)

tick_image = PhotoImage(file="images/right.png")
tick = Button(image=tick_image, bd=0, bg="grey", command=word_learned)
tick.grid(column=1, row=1)

generate_word()


window.mainloop()
