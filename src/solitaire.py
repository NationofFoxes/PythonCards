import tkinter as tk
from PIL import Image, ImageTk
import os
import random

class Tile:
    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)


class Deck(Tile):
    def __init__(self):
        super().__init__(50, 35)  # Fixed position for the deck

    def show_deck(self):
        # Return a list of card backs to represent the deck
        return [card.back_image for card in self.cards]

class Fan(Tile):
    def __init__(self):
        super().__init__(160, 35)

    def show_fan(self):
        return [card.image for card in self.cards if card.face_up]
    
class Foundation(Tile):
    def __init__(self, position_x, position_y):
        super().__init__(position_x, position_y)

    def show_foundation(self):
        return [card.image for card in self.cards]
    
class Tableau(Tile):
    def __init__(self, position_x, position_y):
        super().__init__(position_x, position_y)

    def show_cascade(self):
        return [card.image for card in self.cards]

    def show_top_card(self):
        if self.cards:
            return self.cards[-1].image
        else:
            return None

class Card:
    def __init__(self, image, back_image, x, y, suit, value, face_up=False):
        self.image = image
        self.back_image = back_image
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

class Solitaire:
    def __init__(self):
        self.window_width = 825
        self.window_height = 625
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
        print("Cards: ", len(self.cards))

        # Initialize the index for dealing cards
        self.deal_index = 0

        # Delay between dealing cards in milliseconds
        self.delay = 100

        # Create instances of tiles with black outlines
        self.tableaus = [Tableau(50 + i * 109, 165) for i in range(7)]
        self.foundations = [Foundation(377 + i * 109, 35) for i in range(4)]  # Adjust positions as needed
        self.deck = Deck()
        self.fan = Fan()

        # Initializa list for dragging stack of cards, and also boolean to control the function
        self.selected_cards = []
        self.dragging = False

        # Initialize the last clicked card as None
        self.last_clicked_card = None


        # Draw black outlines for the tiles
        for tableau, num in zip(self.tableaus, range(1,8)):
            self.draw_tile_outline(tableau)
            print(f"Tableau {num}: ", tableau.position_x, tableau.position_y)
        for foundation in self.foundations:
            self.draw_tile_outline(foundation)
        self.draw_tile_outline(self.deck)
        self.draw_tile_outline(self.fan)

        self.deal_cards()
        self.draw_cards()

        # Bind the canvas to mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.window.mainloop()

    def draw_tile_outline(self, tile):
        outline_width = 71
        outline_height = 96
        self.canvas.create_rectangle(
            tile.position_x, tile.position_y, tile.position_x + outline_width, tile.position_y + outline_height,
            outline="black", width=2
        )

    def deal_cards(self):
        tableau_index = 0
        cards_to_deal = iter(self.cards)  # Create an iterator from self.cards

        for num in range(1, 8):  # This generates 1, 2, 3, ..., 7
            tableau = self.tableaus[tableau_index]
            for _ in range(num):
                card = next(cards_to_deal)  # Get the next card from the iterator
                card.x = tableau.position_x  # Set the x coordinate of the card to the tableau's position
                card.y = tableau.position_y + len(tableau.cards) * 30  # Adjust the y coordinate based on the number of cards in the tableau
                self.tableaus[tableau_index].add_card(card)
            print(f"Tableau {tableau_index + 1}: {', '.join(f'{card.value} of {card.suit}' for card in tableau.cards)}")
            tableau_index = (tableau_index + 1) % 7

        # Deal remaining cards to Deck
        for card in cards_to_deal:
            card.x, card.y = self.deck.position_x, self.deck.position_y
            self.deck.add_card(card)
        print(f"Deck: {', '.join(f'{card.value} of {card.suit}' for card in self.deck.cards)}")

        self.draw_cards()


    def draw_cards(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Draw cards on Tableaus
        for tableau in self.tableaus:
            for card in tableau.cards:
                card_face = card.get_image()
                self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card_face)

        # Draw cards on Foundations
        for foundation in self.foundations:
            for card in foundation.cards:
                card_face = card.get_image()
                self.canvas.create_image(card.x, card.y, anchor=tk.NW, image=card_face)

        # Draw cards on Deck
        for i, card in enumerate(self.deck.cards):
            card_back_image = card.get_image()
            self.canvas.create_image(self.deck.position_x + i, self.deck.position_y, anchor=tk.NW, image=card_back_image)

        # Draw cards in the Fan
        for card in self.fan.cards:
            card_face = card.get_image()
            self.canvas.create_image(self.fan.position_x, self.fan.position_y, anchor=tk.NW, image=card_face)

        # Bind the canvas to mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        

    # def on_canvas_click(self, event):
    #     print("Clicked: ", event.x, ", ", event.y)

    #     # Check if the clicked card is the last card in a tableau
    #     for tableau in self.tableaus:
    #         if tableau.cards and tableau.cards[-1].x <= event.x <= tableau.cards[-1].x + 71 and tableau.cards[-1].y <= event.y <= tableau.cards[-1].y + 96:
    #             top_card = tableau.cards[-1]
    #             if not top_card.face_up:
    #                 # Toggle the face-up state for the last card in the tableau
    #                 top_card.toggle_face_up()
    #                 self.redraw_card(top_card)
    #             self.draw_cards()
    #             return  # Exit the function after handling the click on the tableau's top card

    #     # Variables to track the selected tableau and cards to drag
    #     selected_tableau = None
    #     cards_to_drag = []

    #     # Check if a card within a tableau was clicked
    #     for tableau in self.tableaus:
    #         for card in tableau.cards:
    #             if card.x <= event.x <= card.x + 71 and card.y <= event.y <= card.y + 96:
    #                 if card.face_up:
    #                     # Select this card and all cards on top of it in the tableau
    #                     selected_tableau = tableau
    #                     cards_to_drag = tableau.cards[tableau.cards.index(card):]
    #                     print("dragging")
    #                     break  # Exit the loop

    #     if selected_tableau and cards_to_drag:
    #         # Mark the selected cards for dragging
    #         for card in cards_to_drag:
    #             card.selected = True
    #             # Record the initial offset to maintain relative positions when dragging
    #             card.drag_data["x"] = event.x - card.x
    #             card.drag_data["y"] = event.y - card.y

    #     self.draw_cards()


    # def on_canvas_drag(self, event):
    #     for card in self.cards:
    #         if card.selected:
    #             card.x = event.x - card.drag_data["x"]
    #             card.y = event.y - card.drag_data["y"]
    #     self.draw_cards()

    # def on_canvas_release(self, event):
    #     if any(card.selected for card in self.cards):
    #         for tableau in self.tableaus:
    #             if tableau != cards_to_drag[0].current_tableau:
    #                 if tableau.cards:
    #                     top_card = tableau.cards[-1]
    #                     if top_card.x <= event.x <= top_card.x + 71 and top_card.y <= event.y <= top_card.y + 96:
    #                         # Move the selected cards to the target tableau
    #                         for card in cards_to_drag:
    #                             card.current_tableau.remove_card(card)
    #                             tableau.add_card(card)
    #                             card.current_tableau = tableau  # Update the current tableau for the card
    #                         self.draw_cards()
    #                         break
    #         # Reset the dragging flag and selected cards list
    #         for card in cards_to_drag:
    #             card.selected = False
    #         self.draw_cards()

    def on_canvas_click(self, event):
        print("Clicked: ", event.x, ", ", event.y)
        
        # Check if the clicked card is the last card in a tableau
        for tableau in self.tableaus:
            if tableau.cards and tableau.cards[-1].x <= event.x <= tableau.cards[-1].x + 71 and tableau.cards[-1].y <= event.y <= tableau.cards[-1].y + 96:
                top_card = tableau.cards[-1]
                if not top_card.face_up:
                    # Toggle the face-up state for the last card in the tableau
                    top_card.toggle_face_up()
                    self.redraw_card(top_card)
                # Remember the last card clicked
                self.last_clicked_card = top_card
                self.draw_cards()
                return  # Exit the function after handling the click on the tableau's top card

    def on_canvas_drag(self, event):
        # Check if the last clicked card (if any) is face-up
        if self.last_clicked_card and self.last_clicked_card.face_up:
            for card in self.cards:
                if card == self.last_clicked_card:
                    card.x = event.x - card.drag_data["x"]
                    card.y = event.y - card.drag_data["y"]
                self.draw_cards()

    def on_canvas_release(self, event):
        if self.last_clicked_card and self.last_clicked_card.face_up:
            for card in self.cards:
                if card == self.last_clicked_card:
                    for tableau in self.tableaus:
                        if tableau != card.current_tableau:
                            if tableau.cards:
                                top_card = tableau.cards[-1]
                                if top_card.x <= event.x <= top_card.x + 71 and top_card.y <= event.y <= top_card.y + 96:
                                    # Move the last clicked card to the target tableau
                                    card.current_tableau.remove_card(card)
                                    tableau.add_card(card)
                                    card.current_tableau = tableau  # Update the current tableau for the card
                                    self.draw_cards()
                                    break
                    self.draw_cards()

    



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
    solitaire = Solitaire()
    solitaire.window.mainloop()
