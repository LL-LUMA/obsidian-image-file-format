from PIL import Image
import argparse

def convert_png_to_obs(png_path, output_path, grid_size=None):
    try:
        # Load and optionally resize
        image = Image.open(png_path).convert("RGB")

        if grid_size:
            image = image.resize(grid_size)

        width, height = image.size

        with open(output_path, 'w') as f:
            f.write(f"dis:{width}x{height}px\n")  # Header line

            for y in range(height):
                row = []
                for x in range(width):
                    r, g, b = image.getpixel((x, y))
                    hex_color = f"{r:02X}{g:02X}{b:02X}"
                    row.append(hex_color)
                f.write('|'.join(row) + '\n')

        print(f"✅ PNG converted to .obs format at: {output_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PNG to custom .obs format")
    parser.add_argument("--input", type=str, required=True, help="Input PNG path")
    parser.add_argument("--output", type=str, required=True, help="Output .obs path")
    parser.add_argument("--size", type=str, help="Resize image to WIDTHxHEIGHT (e.g. 15x15)")
    args = parser.parse_args()

    size = None
    if args.size:
        try:
            w, h = map(int, args.size.lower().split('x'))
            size = (w, h)
        except:
            print("❌ Invalid size format. Use WIDTHxHEIGHT (e.g. 15x15)")
            exit(1)

    convert_png_to_obs(args.input, args.output, grid_size=size)
