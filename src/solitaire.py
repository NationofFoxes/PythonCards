import tkinter as tk
from PIL import Image, ImageTk

class Solitaire:
    def __init__(self):

        # Create a main application window

        self.window = tk.Tk()
        self.window.title("Solitaire")

        self.canvas = tk.Canvas(self.window, width=800, height=600, bg="green")
        self.canvas.pack()
        # Load a card image
        card_image = Image.open("images/Spades_Ace.png")
        card_image = card_image.resize((71, 96))  # Resize to fit your card dimensions

        # Create a PhotoImage object from the card image
        self.card_image = ImageTk.PhotoImage(card_image)

        # Place the card image on the canvas
        self.canvas.create_image(400, 300, anchor=tk.NW, image=self.card_image)

        self.window.mainloop()

if __name__ == "__main__":
    solitaire = Solitaire()
