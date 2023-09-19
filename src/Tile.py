class Tile:
    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

class Tableau(Tile):
    def __init__(self, position_x, position_y):
        super().__init__(position_x, position_y)

    def show_cascade(self):
        return self.cards

    def show_top_card(self):
        if self.cards:
            return self.cards[-1]
        else:
            return None

class Deck(Tile):
    def __init__(self):
        super().__init__(20, 20)  # Fixed position for the deck

    def show_deck(self):
        # Return a list of card backs to represent the deck
        return [card.back_image for card in self.cards]

class Foundation(Tile):
    def __init__(self, position_x, position_y):
        super().__init__(position_x, position_y)

    def show_foundation(self):
        return self.cards

class Fan(Tile):
    def __init__(self, position_x, position_y):
        super().__init__(position_x, position_y)

    def show_fan(self):
        return self.cards
