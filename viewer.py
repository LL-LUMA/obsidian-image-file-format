import tkinter as tk
from tkinter import filedialog
from PIL import Image
import argparse
import json
from pathlib import Path
import math
import sys

# ---------------- Load Color Data ----------------

def load_color_data(json_path):
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            return {color['hex'].upper(): color['name'] for color in data['colors']}
    except Exception as e:
        print(f"Error loading color data: {str(e)}")
        exit(1)

# ---------------- Parse .obs File ----------------

def parse_obs_file(image_path, color_map):
    with open(image_path, 'r') as file:
        lines = file.readlines()[1:]
        content = ''.join(line.strip().replace('|', '') for line in lines)
        chunk_size = 6
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

        pixels = []
        for chunk in chunks:
            hex_code = f"#{chunk}"
            color_name = color_map.get(hex_code.upper(), None)
            pixels.append({
                "text": color_name if color_name else chunk,
                "bg": hex_code,
                "fg": "black" if is_bright_color(hex_code) else "white"
            })
        return pixels

def is_bright_color(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    brightness = (r*299 + g*587 + b*114) / 1000
    return brightness > 128

# ---------------- GUI Application ----------------

class PixelGridApp:
    def __init__(self, root, pixels, image_path):
        self.root = root
        self.pixels = pixels
        self.image_path = image_path
        self.pixel_labels = []
        self.root.title("Obsidian Image Viewer")
        self.root.configure(bg="#1e1e2f")

        # Main grid container
        self.frame = tk.Frame(root, bg="#1e1e2f", padx=20, pady=20)
        self.frame.pack()

        # Controls (export + zoom)
        self.control_frame = tk.Frame(root, bg="#1e1e2f")
        self.control_frame.pack(pady=15)

        # Export Button (modern style)
        export_btn = tk.Button(
            self.control_frame,
            text="⬇ Export to PNG",
            command=self.export_to_png,
            bg="#3c3f4a",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=15,
            pady=5,
            activebackground="#50545f",
            activeforeground="white",
            bd=0
        )
        export_btn.pack(side=tk.LEFT, padx=20)

        # Zoom Scale (modern style)
        self.scale = tk.Scale(
            self.control_frame,
            from_=3, to=7,
            orient="horizontal",
            label="Zoom Level",
            command=self.update_grid_size,
            bg="#1e1e2f",
            fg="white",
            font=("Segoe UI", 9),
            troughcolor="#2a2d38",
            highlightthickness=0,
            bd=0,
            sliderrelief="flat",
            length=200
        )
        self.scale.set(6)
        self.scale.pack(side=tk.LEFT)

        self.create_grid()
        self.center_window()

    def create_grid(self):
        self.clear_grid()
        total_pixels = len(self.pixels)
        self.grid_size = math.isqrt(total_pixels)
        rows = cols = self.grid_size

        if rows * cols < total_pixels:
            cols += 1

        i = 0
        self.pixel_labels = []

        for r in range(rows):
            row_labels = []
            for c in range(cols):
                if i >= total_pixels:
                    break
                px = self.pixels[i]
                label = tk.Label(
                    self.frame,
                    width=self.scale.get(),
                    height=self.scale.get() // 2,
                    bg=px["bg"],
                    fg=px["fg"],
                    font=("Segoe UI", 9, "bold"),
                    relief="flat"
                )
                label.grid(row=r, column=c, padx=0, pady=0)
                row_labels.append(label)
                i += 1
            self.pixel_labels.append(row_labels)

    def clear_grid(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def update_grid_size(self, _):
        self.create_grid()

    def center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def export_to_png(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save image as"
        )
        if not filename:
            return

        pixel_size = 20
        rows = len(self.pixel_labels)
        cols = len(self.pixel_labels[0]) if rows else 0
        img = Image.new("RGB", (cols * pixel_size, rows * pixel_size))

        for r, row in enumerate(self.pixel_labels):
            for c, label in enumerate(row):
                hex_color = label.cget("bg")
                rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
                for y in range(pixel_size):
                    for x in range(pixel_size):
                        img.putpixel((c * pixel_size + x, r * pixel_size + y), rgb)

        img.save(filename)
        print(f"Image saved to {filename}")

# ---------------- Main Entry ----------------

def main():
    parser = argparse.ArgumentParser(description="Render .obs image file")
    parser.add_argument('--image', type=str, required=True, help='Path to .obs image file')
    args = parser.parse_args()

    COLOR_JSON_PATH = Path('C:/obsidian/.hex/pixels.json')
    color_map = load_color_data(COLOR_JSON_PATH)

    try:
        pixels = parse_obs_file(args.image, color_map)
    except Exception as e:
        print(f"Failed to process image: {str(e)}")
        sys.exit(1)

    root = tk.Tk()
    app = PixelGridApp(root, pixels, args.image)
    root.mainloop()

if __name__ == "__main__":
    main()
