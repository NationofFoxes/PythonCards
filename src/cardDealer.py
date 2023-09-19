import tkinter as tk
from PIL import Image, ImageTk
import random
import os

# Card class
class Card:
    def __init__(self, image, backImage, x, y, suit, value, face_up=False):
        self.image = image
        self.backImage = backImage
        self.x = x
        self.y = y
        self.suit = suit
        self.value = value
        self.face_up = face_up

    def toggle_face_up(self):
        self.face_up = not self.face_up

# Main application class
class Dealer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Card Dealer")
        
        self.canvas = tk.Canvas(self.window, width=800, height=600, bg="green")
        self.canvas.pack()

        self.cards = []
        card_dir = "images/cards"
        card_back_image = ImageTk.PhotoImage(Image.open(os.path.join("images/backs", "Back1_5.png")))
        for filename in os.listdir(card_dir):
            if filename.endswith(".png"):
                # Extract suit and value from filename
                suit, value = os.path.splitext(filename)[0].split("_")
                card_image = Image.open(os.path.join(card_dir, filename))
                card_image = card_image.resize((71, 96))
                card = Card(ImageTk.PhotoImage(card_image), card_back_image, 0, 0, suit, value, face_up=False)
                self.cards.append(card)
                print("Image loaded: ", filename)

        # Set the back of all cards to the same image
        # for card in self.cards:
        #     card.image_back = card_back_image

        # Shuffle the cards
        random.shuffle(self.cards)
        print("Deck shuffled")

        # Bind the canvas click events
        self.canvas.bind("<Button-1>", self.deal_card)
        self.canvas.bind("<Button-3>", self.toggle_face_up)

        # Initialize the list to keep track of dealt cards
        self.dealt_cards = []

        self.window.mainloop()

    def deal_card(self, event):
        # Randomly select a card from the available cards
        random_card = random.choice(self.cards)

        # Set the coordinates where the card was clicked
        random_card.x, random_card.y = event.x-35, event.y-50

        # Draw the card on the canvas
        if random_card.face_up:
            self.canvas.create_image(random_card.x, random_card.y, anchor=tk.NW, image=random_card.image)
        else:
            # Draw the back of the card
            self.canvas.create_image(random_card.x, random_card.y, anchor=tk.NW, image=random_card.backImage)

        print(f"Dealt {random_card.value} of {random_card.suit} at coordinates {random_card.x},{random_card.y}")

        # Keep track of dealt cards
        self.dealt_cards.append(random_card)

    def toggle_face_up(self, event):
        for card in self.dealt_cards:
            if card.x <= event.x <= card.x + 71 and card.y <= event.y <= card.y + 96:
                card.toggle_face_up()
                self.redraw_card(card)

    def redraw_card(self, card):
        if card.face_up:
            # Redraw the card face
            self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card.image)
        else:
            # Draw the back of the card
            self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card.backImage)

if __name__ == "__main__":
    dealer = Dealer()
