import os
from PIL import Image

class SlotMachineVisualizer:
    def __init__(self, background_image="background.png", border_image="border.png"):
        """
        Initialize the visualizer with a list of symbols and custom border image.
        Args:
            background_image (str): Path to the background image.
            border_image (str): Path to the border image to be used around each symbol.
            special_symbol_image (str): Path to the special symbol image.
        """
        self.symbol_images = {}
        self.background_image = background_image
        self.border_image = border_image

    def generate_image(self, spin_result, output_path="slot_result.png"):
        """
        Generate an image to display the spin result with custom borders.

        Args:
            spin_result (list of list of str): The 3x3 spin result where symbols are file paths.
            output_path (str): Path to save the generated image.
        """
        try:
            bg_img = Image.open(self.background_image)
        except FileNotFoundError:
            print(f"Background image '{self.background_image}' not found!")
            return

        try:
            border_img = Image.open(self.border_image)
        except FileNotFoundError:
            print(f"Border image '{self.border_image}' not found!")
            return

        symbol_size = 100
        padding = 20
        grid_size = len(spin_result)

        img_width = grid_size * symbol_size + (grid_size + 1) * padding
        img_height = grid_size * symbol_size + (grid_size + 1) * padding
        bg_img = bg_img.resize((img_width, img_height))

        border_resized = border_img.resize((symbol_size + padding, symbol_size + padding))

        for row in range(grid_size):
            for col in range(grid_size):
                symbol_path = spin_result[row][col]

                image_path = symbol_path
                try:
                    symbol_img = Image.open(image_path)

                    if symbol_img.mode in ("RGBA", "P"):
                        symbol_img = symbol_img.convert("RGBA")
                    else:
                        symbol_img = symbol_img.convert("RGB")

                    smaller_symbol_size = 60
                    symbol_img = symbol_img.resize((smaller_symbol_size, smaller_symbol_size))

                    x = padding + col * (symbol_size + padding)
                    y = padding + row * (symbol_size + padding)

                    bg_img.paste(border_resized, (x, y), border_resized.convert("RGBA").split()[3])  # Use alpha channel as mask

                    symbol_x = x + (symbol_size + padding - smaller_symbol_size) // 2
                    symbol_y = y + (symbol_size + padding - smaller_symbol_size) // 2
                    bg_img.paste(symbol_img, (symbol_x, symbol_y), symbol_img.convert("RGBA").split()[3])  # Use alpha channel as mask

                except FileNotFoundError:
                    print(f"Image file not found for symbol: {symbol_path}")

        bg_img.save(output_path)
