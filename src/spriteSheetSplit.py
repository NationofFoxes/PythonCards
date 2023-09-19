from PIL import Image

# Load the sprite sheet image
sprite_sheet = Image.open("PC Computer - Solitaire - Cards.png")

# Crop to remove the 1px border if needed
# sprite_sheet = sprite_sheet.crop((1, 1, sprite_sheet.width - 1, sprite_sheet.height - 1))

card_width = 71  # Width of each card
card_height = 96  # Height of each card

card_images = []

suits = ["Spades", "Hearts", "Clubs", "Diamonds", "Back1", "Back2"]
values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]


for row in range(6):
    for col in range(13):
        
        x = col * (card_width)
        y = row * (card_height)

        # Crop the card image based on the coordinates and dimensions
        card_image = sprite_sheet.crop((x, y, x + card_width, y + card_height))

        # Get the suit and value for this card
        suit = suits[row]
        value = values[col]

        # Append the card image to the list
        card_images.append(card_image)

        # Construct the card name (e.g., "Hearts_Ace")
        card_name = f"{suit}_{value}.png"
        card_image.save(card_name)

# Saves each card with different filenames
# for i, card_image in enumerate(card_images):
#     card_image.save(card_name)