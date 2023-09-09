from PIL import Image

# Load the sprite sheet image
sprite_sheet = Image.open("images\windows-playing-cards.png")

# Crop to remove the 1px border
sprite_sheet = sprite_sheet.crop((1, 1, sprite_sheet.width - 1, sprite_sheet.height - 1))

card_width = 71  # Width of each card
card_height = 96  # Height of each card

card_images = []

suits = ["Clubs", "Hearts", "Spades", "Diamonds"]
values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]


for row in range(4):
    for col in range(13):
        xBorder = 0
        x = col * (card_width + 2) + 1
        y = row * (card_height + 2) + 1

        # Crop the card image based on the coordinates and dimensions
        card_image = sprite_sheet.crop((x + xBorder, y, x + card_width, y + card_height))

        # Get the suit and value for this card
        suit = suits[row]
        value = values[col]

        # Append the card image to the list
        card_images.append(card_image)

        # Construct the card name (e.g., "Hearts_Ace")
        card_name = f"images/{suit}_{value}.png"
        card_image.save(card_name)

        xBorder += 2

# Saves each card with different filenames
# for i, card_image in enumerate(card_images):
#     card_image.save(card_name)