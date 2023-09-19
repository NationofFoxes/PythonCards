import tkinter as tk
from PIL import Image, ImageTk
import os
import random
import time

class Card:
    def __init__(self, image, back_image, x, y, suit, value, face_up=False):
        self.image = image
        self.back_image = ImageTk.PhotoImage(Image.open(os.path.join("images/backs", "Back1_5.png")))
        self.x = x
        self.y = y
        self.suit = suit
        self.value = value
        self.face_up = face_up
        self.selected = False
        self.drag_data = {"x": 0, "y": 0} 

    def toggle_face_up(self):
        self.face_up = not self.face_up

    def get_image(self):
        if self.face_up:
            return self.image
        else:
            return self.back_image

class Memory:
    def __init__(self):
        self.window_width = 900
        self.window_height = 700
        self.window = tk.Tk()
        self.window.title("Solitaire")

        self.canvas = tk.Canvas(self.window, width=self.window_width, height=self.window_height, bg="green")
        scale_x = 2
        scale_y = 2
        self.canvas.scale("all", 0, 0, scale_x, scale_y)
        self.canvas.pack()

        # Create a list of cards
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

        # Shuffle the cards
        random.shuffle(self.cards)
        print("Deck shuffled")

        # Initialize the index for dealing cards
        self.deal_index = 0

        # Delay between dealing cards in milliseconds
        self.delay = 500

        self.window.after(self.delay, self.deal_cards_with_delay)  # Start dealing cards

        # Bind the canvas to mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.window.mainloop()

    def deal_cards_with_delay(self):
        if self.deal_index < len(self.cards):
            card = self.cards[self.deal_index]

            # Calculate the position for the current card
            row = self.deal_index % 7
            col = self.deal_index // 7
            card.x = 20 + col * 89
            card.y = 20 + row * 106

            self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card.back_image)  # Use the back image
            print(f"Card dealt at ({card.x}, {card.y})")
            self.deal_index += 1
            self.window.after(self.delay, self.deal_cards_with_delay)  # Deal the next card
        else:
            print("All cards dealt")


    def draw_card(self, card):
        self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card.image)
        print(f"{card.value} of {card.suit} dealt at ({card.x}, {card.y})")

        # Bind the canvas to mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        

    def on_canvas_click(self, event):
        print("Clicked: ", event.x, ", ", event.y)
        # Check if any card was clicked
        for card in self.cards:
            if card.x <= event.x <= card.x + 71 and card.y <= event.y <= card.y + 96:
                card.toggle_face_up()
                self.redraw_card(card)

    def toggle_face_up(self, event):
        for card in self.cards:
            if card.x <= event.x <= card.x + 71 and card.y <= event.y <= card.y + 96:
                card.toggle_face_up()
                self.redraw_card(card)

    def redraw_card(self, card):
        if card.face_up:
            # Redraw the card face
            self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card.image)
        else:
            # Draw the back of the card
            self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card.back_image)

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
        # self.canvas.delete("all")  # Clear the canvas
        for card in self.cards:
            if card.face_up:
                # Create an image for the card face
                card_face = card.get_image()
                self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card_face)
            else:
                # Create an image for the card back (placeholder)
                card_back = card.get_image()
                self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card_back)


if __name__ == "__main__":
    solitaire = Memory()
    solitaire.window.mainloop()
