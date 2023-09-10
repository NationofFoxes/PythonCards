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

    def toggle_face_up(self):
        self.face_up = not self.face_up

# Main application class
class Dealer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Card Dealer")
        
        scale_x = 2
        scale_y = 2
        
        self.canvas = tk.Canvas(self.window, width=1800, height=1600, bg="green")
        self.canvas.scale("all", 0, 0, scale_x, scale_y)
        self.canvas.pack()

        self.cards = []
        card_dir = "images"
        for filename in os.listdir(card_dir):
            if filename.endswith(".png"):
                # Extract suit and value from filename
                suit, value = os.path.splitext(filename)[0].split("_")
                card_image = Image.open(os.path.join(card_dir, filename))
                card_image = card_image.resize((79, 96))
                card = Card(ImageTk.PhotoImage(card_image), 0, 0, suit, value, face_up=False)
                self.cards.append(card)
                print("Image loaded: ", filename)

        # Shuffle the cards
        random.shuffle(self.cards)
        print("Deck shuffled")


        # Create a label as a placeholder for card back
        card_back_label = tk.Label(self.canvas, text="card_back", width=7, height=9, bg="white")
        card_back_label.place(x=0, y=0)

        # Bind the canvas click event to the custom deal_card method
        self.canvas.bind("<Button-1>", self.deal_card)
        self.canvas.bind("<Button-3>", self.toggle_face_up)  # Right-click to toggle face up

        # Initialize the list to keep track of dealt cards
        self.dealt_cards = []

        self.window.mainloop()

    def deal_card(self, event):
        # Randomly select a card from the available cards
        random_card = random.choice(self.cards)

        # Set the coordinates where the card was clicked
        random_card.x, random_card.y = event.x, event.y

        # Draw the card on the canvas
        if random_card.face_up:
            self.canvas.create_image(random_card.x, random_card.y, anchor=tk.NW, image=random_card.image)
        else:
            # Draw card back label if the card is face down
            card_back_label = tk.Label(self.canvas, text="card_back", width=7, height=9, bg="white")
            card_back_label.place(x=random_card.x, y=random_card.y)

        print(f"Dealt {random_card.value} of {random_card.suit} at coordinates {random_card.x},{random_card.y}")

        # Keep track of dealt cards
        self.dealt_cards.append(random_card)

    def toggle_face_up(self, event):
        # Check if any card was clicked
        for card in self.dealt_cards:
            if card.x <= event.x <= card.x + 71 and card.y <= event.y <= card.y + 96:
                card.toggle_face_up()
                self.canvas.delete("all")
                self.draw_cards()

    def draw_cards(self):
        for card in self.dealt_cards:
            if card.face_up:
                # Create an image for the card face
                self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card.image)
            else:
                # Draw card back label if the card is face down
                card_back_label = tk.Label(self.canvas, text="card_back", width=7, height=9, bg="white", str="Card_Back")
                card_back_label.place(x=card.x, y=card.y)

if __name__ == "__main__":
    dealer = Dealer()
