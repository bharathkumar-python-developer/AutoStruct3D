# AutoStruct3D - main.py (Final Full Version)
import os
import json
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def ai_suggested_room_sizes(num_rooms, num_bathrooms):
    return [12 + num_rooms // 2, 10 + num_rooms // 3], [6 + num_bathrooms // 3, 6 + num_bathrooms // 3]

def generate_all_outputs(config):
    output_dir = "output/floor_1"
    os.makedirs(output_dir, exist_ok=True)
    img = Image.new("RGB", (800, 600), config['colors'].get('walls', 'white'))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    rooms = [
        ("Bedroom", config["bedroom_size"], config['colors']['bedroom'], (30, 30)),
        ("Bathroom", config["bathroom_size"], config['colors']['bathroom'], (230, 30)),
        ("Kitchen", config.get("kitchen_size", [8, 6]), "orange", (430, 30)),
        ("Living Room", [20, 15], "pink", (30, 200)),
        ("Balcony", config.get("balcony_size", [6, 4]), "skyblue", (230, 200)),
        ("Garage", [15, 10], "gray", (430, 200)),
        ("Veranda", [10, 4], "lightyellow", (30, 400)),
        ("Stairs", [5, 5], "brown", (230, 400)),
    ]

    scale = 10
    for name, size, color, (x, y) in rooms:
        w, h = int(size[0]*scale), int(size[1]*scale)
        draw.rectangle([x, y, x+w, y+h], fill=color, outline="black", width=2)
        draw.text((x+5, y+5), f"{name}\n{size[0]}' x {size[1]}'", fill="black", font=font)

    # Save image
    image_path = os.path.join(output_dir, "layout.png")
    img.save(image_path)

    # Save PDF
    pdf_path = "output/layouts_combined.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    img.thumbnail((500, 700))
    img.save("output/temp.jpg")
    c.drawImage("output/temp.jpg", 50, 100)
    c.save()
    os.remove("output/temp.jpg")

    # Save GIF
    gif_path = "output/floor_animation.gif"
    img.save(gif_path, save_all=True, append_images=[img], duration=800, loop=0)

    return {"png_paths": [image_path], "pdf_path": pdf_path, "gif_path": gif_path}

def generate_whatsapp_share_link(file_path):
    import urllib.parse
    return f"https://wa.me/?text=View%20your%20AutoStruct3D%20layout%20here:%20{urllib.parse.quote(file_path)}"
