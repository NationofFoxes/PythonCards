import tkinter as tk
from PIL import Image, ImageTk
import random
import os

# Card class
class Card:
    def __init__(self, image, x, y, suit, value, face_up=False):
        self.image = image
        self.x = x
        self.y = y
        self.suit = suit
        self.value = value
        self.face_up = face_up
        self.selected = False  # Track if the card is selected
        self.drag_data = {"x": 0, "y": 0}

# Main application class
class Dealer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Card Dealer")

        self.canvas = tk.Canvas(self.window, width=800, height=600, bg="green")
        self.canvas.pack()

        self.cards = []
        card_dir = "images"
        for filename in os.listdir(card_dir):
            if filename.endswith(".png"):
                # Extract suit and value from filename
                suit, value = os.path.splitext(filename)[0].split("_")
                card_image = Image.open(os.path.join(card_dir, filename))
                card_image = card_image.resize((71, 96))
                card = Card(ImageTk.PhotoImage(card_image), 0, 0, suit, value)
                self.cards.append(card)
                print("Image loaded: ", filename)

        # Bind the canvas click event to the custom deal_card method
        self.canvas.bind("<Button-1>", self.deal_card)

        # Initialize the list to keep track of dealt cards
        self.dealt_cards = []

        self.window.mainloop()

    def deal_card(self, event):
        # Randomly select a card from the available cards
        random_card = random.choice(self.cards)

        # Set the coordinates where the card was clicked
        random_card.x, random_card.y = event.x, event.y

        # Draw the card on the canvas
        self.canvas.create_image(random_card.x - 40, random_card.y - 50, anchor=tk.NW, image=random_card.image)
        print(f"Dealt {random_card.value} of {random_card.suit} at coordinates {random_card.x},{random_card.y}")

        # Keep track of dealt cards
        self.dealt_cards.append(random_card)

if __name__ == "__main__":
    dealer = Dealer()
