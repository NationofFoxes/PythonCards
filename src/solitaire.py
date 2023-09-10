import tkinter as tk
from PIL import Image, ImageTk
import os
import random

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

    def get_image(self):
        if self.face_up:
            return self.image
        else:
            # Return a placeholder image or label when face_down
            return self.placeholder_image

class Solitaire:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Solitaire")

        self.canvas = tk.Canvas(self.window, width=1800, height=1600, bg="green")
        scale_x = 2
        scale_y = 2
        self.canvas.scale("all", 0, 0, scale_x, scale_y)
        self.canvas.pack()

        # Create a list of cards
        self.cards = []
        card_dir = "images"
        for filename in os.listdir(card_dir):
            if filename.endswith(".png"):
                # Extract suit and value from filename
                suit, value = os.path.splitext(filename)[0].split("_")
                card_image = Image.open(os.path.join(card_dir, filename))
                card_image = card_image.resize((71, 96))
                card = Card(ImageTk.PhotoImage(card_image), 0, 0, suit, value, face_up=False)
                self.cards.append(card)
                print("Image loaded: ", filename)

        # Shuffle the cards
        random.shuffle(self.cards)
        print("Deck shuffled")

        # Draw a random subset of cards on the canvas
        card_width = 79
        card_height = 96
        print("Dealing cards...")
        for i in range(7):
            for j in range(i + 1):
                card = self.cards.pop()
                card.x = 1 + i * (card_width + 10)  # Adjust the x coordinate based on card's position
                card.y = 1 + j * (card_height + 10)  # Adjust the y coordinate based on card's position
                self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card.image)
                print(f"{card.value} of {card.suit} dealt at ({card.x}, {card.y})")

        # Bind the canvas to mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.window.mainloop()

    def on_canvas_click(self, event):
        print("Clicked: ", event.x, ", ", event.y)
        # Check if any card was clicked
        for card in self.cards:
            if card.x <= event.x <= card.x + 71 and card.y <= event.y <= card.y + 96:
                card.selected = True
                card.drag_data["x"] = event.x - card.x
                card.drag_data["y"] = event.y - card.y
                self.draw_cards()

    def on_canvas_drag(self, event):
        for card in self.cards:
            if card.selected:
                card.x = event.x - card.drag_data["x"]
                card.y = event.y - card.drag_data["y"]
                self.draw_cards()

    def on_canvas_release(self, event):
        for card in self.cards:
            card.selected = False

    def draw_cards(self):
        self.canvas.delete("all")  # Clear the canvas
        for card in self.cards:
            if card.face_up:
                # Create an image for the card face
                card_face = card.get_image()
                self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card_face)

                # Display the card's value and suit as text
                text_x = card.x + 5  # Adjust text position
                text_y = card.y + 5  # Adjust text position
                self.canvas.create_text(text_x, text_y, anchor=tk.NW, text=f"{card.value} of {card.suit}")
            else:
                # Create an image for the card back (placeholder)
                card_back = card.get_image()
                self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card_back)


if __name__ == "__main__":
    solitaire = Solitaire()
