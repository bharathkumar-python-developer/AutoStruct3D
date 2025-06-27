# gui_app.py (Enhanced Version with Auto Alignment, Building Rules, and Automation)
import os
import json
import tkinter as tk
from tkinter import messagebox, colorchooser
from PIL import Image, ImageTk, ImageSequence
from reportlab.pdfgen import canvas
from main import generate_all_outputs, ai_suggested_room_sizes, generate_whatsapp_share_link

app = tk.Tk()
app.title("AutoStruct3D - Smart Structure Designer")
app.geometry("620x800")

config_data = {}
current_step = 0
steps = []
preview_color_frame = None

def next_step():
    global current_step
    if current_step < len(steps) - 1:
        steps[current_step].pack_forget()
        current_step += 1
        steps[current_step].pack()

def prev_step():
    global current_step
    if current_step > 0:
        steps[current_step].pack_forget()
        current_step -= 1
        steps[current_step].pack()

# ================== Step 1 ==================
def collect_step1():
    try:
        config_data["rooms"] = int(room_var.get())
        config_data["bedroom_size"] = [float(bedroom_w.get()), float(bedroom_h.get())]
        config_data["bathroom_size"] = [float(bathroom_w.get()), float(bathroom_h.get())]

        config_data["kitchen_size"] = [float(kitchen_w.get()), float(kitchen_h.get())] if include_kitchen.get() else None
        config_data["hall_size"] = [float(hall_w.get()), float(hall_h.get())] if include_hall.get() else None
        config_data["balcony_size"] = [float(balcony_w.get()), float(balcony_h.get())] if include_balcony.get() else None
        config_data["garage_size"] = [float(garage_w.get()), float(garage_h.get())] if include_garage.get() else None
        config_data["veranda_size"] = [float(veranda_w.get()), float(veranda_h.get())] if include_veranda.get() else None

        config_data["auto_layout"] = True
        next_step()
    except Exception as e:
        messagebox.showerror("Input Error", f"Please enter valid numeric values.\n{e}")

def auto_suggest():
    try:
        r = int(room_var.get())
        b = int(bathroom_var.get())
        br_size, ba_size = ai_suggested_room_sizes(r, b)
        bedroom_w.set(str(br_size[0])); bedroom_h.set(str(br_size[1]))
        bathroom_w.set(str(ba_size[0])); bathroom_h.set(str(ba_size[1]))
        kitchen_w.set("10"); kitchen_h.set("8")
        hall_w.set("15"); hall_h.set("12")
        balcony_w.set("6"); balcony_h.set("4")
        garage_w.set("14"); garage_h.set("10")
        veranda_w.set("10"); veranda_h.set("4")
        messagebox.showinfo("Auto-Suggest", "Room sizes auto-filled based on AI recommendations and regulations.")
    except Exception as e:
        messagebox.showerror("AI Error", str(e))

# ================== Step 2 ==================
def pick_color(var):
    color = colorchooser.askcolor()[1]
    if color:
        var.set(color)
        update_preview_color()

def update_preview_color(*args):
    if preview_color_frame:
        preview_color_frame.config(bg=wall_color.get())

# ================== Step 3 ==================
def submit_final():
    try:
        config_data["cupboards"] = cupboard_var.get()
        config_data["colors"] = {
            "bedroom": bedroom_color.get(),
            "bathroom": bathroom_color.get(),
            "walls": wall_color.get()
        }
        config_data["door_direction"] = door_dir_var.get()

        config_data["floor_height"] = float(floor_height.get()) if floor_height.get() else 10.0
        config_data["steps"] = staircase_var.get()
        config_data["floors"] = int(floor_count.get()) if floor_count.get() else 1

        os.makedirs("data", exist_ok=True)
        with open("data/sample_input.json", "w") as f:
            json.dump(config_data, f, indent=4)

        result = generate_all_outputs(config_data)
        messagebox.showinfo("Success", f"Layouts created.\nGIF: {result['gif_path']}")
    except Exception as e:
        messagebox.showerror("Generation Error", str(e))

def preview_image():
    path = "output/floor_1/layout.png"
    if os.path.exists(path):
        img = Image.open(path)
        img.thumbnail((400, 300))
        img_tk = ImageTk.PhotoImage(img)
        top = tk.Toplevel()
        tk.Label(top, image=img_tk).pack()
        top.image = img_tk
    else:
        messagebox.showwarning("Not Found", "Generate model first.")

def export_pdf():
    from reportlab.lib.pagesizes import A4
    try:
        c = canvas.Canvas("output/layouts_combined.pdf", pagesize=A4)
        for i in range(config_data.get("floors", 1)):
            path = f"output/floor_{i+1}/layout.png"
            if os.path.exists(path):
                img = Image.open(path)
                img.thumbnail((500, 700))
                img.save("output/temp.jpg")
                c.drawImage("output/temp.jpg", 50, 100)
                c.showPage()
        c.save()
        os.remove("output/temp.jpg")
        messagebox.showinfo("PDF Exported", "Layouts saved as PDF.")
    except Exception as e:
        messagebox.showerror("PDF Error", str(e))

def view_gif():
    path = "output/floor_animation.gif"
    if not os.path.exists(path):
        messagebox.showwarning("Not Found", "Generate GIF first.")
        return
    win = tk.Toplevel()
    lbl = tk.Label(win)
    lbl.pack()
    gif = Image.open(path)
    frames = [ImageTk.PhotoImage(f.convert("RGBA")) for f in ImageSequence.Iterator(gif)]
    def animate(i):
        lbl.config(image=frames[i])
        win.after(200, animate, (i+1)%len(frames))
    animate(0)

def share_on_whatsapp():
    path = "output/layouts_combined.pdf"
    if os.path.exists(path):
        link = generate_whatsapp_share_link(path)
        messagebox.showinfo("WhatsApp", f"Share using this link:\n{link}")
    else:
        messagebox.showwarning("No PDF", "Please export to PDF first.")

# ========== UI Frames ==========
frame1 = tk.Frame(app)
room_var = tk.StringVar(); bedroom_w = tk.StringVar(); bedroom_h = tk.StringVar()
bathroom_w = tk.StringVar(); bathroom_h = tk.StringVar(); bathroom_var = tk.StringVar()
kitchen_w = tk.StringVar(); kitchen_h = tk.StringVar(); include_kitchen = tk.BooleanVar()
hall_w = tk.StringVar(); hall_h = tk.StringVar(); include_hall = tk.BooleanVar()
balcony_w = tk.StringVar(); balcony_h = tk.StringVar(); include_balcony = tk.BooleanVar()
garage_w = tk.StringVar(); garage_h = tk.StringVar(); include_garage = tk.BooleanVar()
veranda_w = tk.StringVar(); veranda_h = tk.StringVar(); include_veranda = tk.BooleanVar()

labels = ["Rooms", "Bedroom Size (W x H)", "Bathrooms", "Bathroom Size"]
for l in labels:
    tk.Label(frame1, text=l, font=('Arial', 10, 'bold')).pack()
tk.Entry(frame1, textvariable=room_var).pack()
tk.Entry(frame1, textvariable=bedroom_w).pack(); tk.Entry(frame1, textvariable=bedroom_h).pack()
tk.Entry(frame1, textvariable=bathroom_var).pack()
tk.Entry(frame1, textvariable=bathroom_w).pack(); tk.Entry(frame1, textvariable=bathroom_h).pack()

for label, check, w, h in [
    ("Kitchen", include_kitchen, kitchen_w, kitchen_h),
    ("Hall", include_hall, hall_w, hall_h),
    ("Balcony", include_balcony, balcony_w, balcony_h),
    ("Garage", include_garage, garage_w, garage_h),
    ("Veranda", include_veranda, veranda_w, veranda_h)
]:
    tk.Checkbutton(frame1, text=f"Include {label}", variable=check).pack()
    tk.Entry(frame1, textvariable=w).pack(); tk.Entry(frame1, textvariable=h).pack()

tk.Button(frame1, text="Auto-Suggest Sizes", command=auto_suggest).pack(pady=5)
tk.Button(frame1, text="Next", command=collect_step1).pack(pady=10)

frame2 = tk.Frame(app)
cupboard_var = tk.BooleanVar(); bedroom_color = tk.StringVar(); bathroom_color = tk.StringVar(); wall_color = tk.StringVar(); door_dir_var = tk.StringVar()
bedroom_color.set("lightblue"); bathroom_color.set("white"); wall_color.set("gray")
tk.Checkbutton(frame2, text="Include Cupboards", variable=cupboard_var).pack()
tk.Label(frame2, text="Bedroom Color").pack(); tk.Button(frame2, text="Pick Color", command=lambda: pick_color(bedroom_color)).pack()
tk.Label(frame2, text="Bathroom Color").pack(); tk.Button(frame2, text="Pick Color", command=lambda: pick_color(bathroom_color)).pack()
tk.Label(frame2, text="Wall Color").pack(); tk.Button(frame2, text="Pick Color", command=lambda: pick_color(wall_color)).pack()
tk.Label(frame2, text="Live Preview").pack()
preview_color_frame = tk.Frame(frame2, bg=wall_color.get(), width=50, height=30)
preview_color_frame.pack(pady=5)
tk.Label(frame2, text="Door Direction").pack()
tk.OptionMenu(frame2, door_dir_var, "north", "south", "east", "west").pack()
tk.Button(frame2, text="Back", command=prev_step).pack(side='left', padx=10)
tk.Button(frame2, text="Next", command=next_step).pack(side='right', padx=10)

frame3 = tk.Frame(app)
floor_height = tk.StringVar(); floor_count = tk.StringVar(); staircase_var = tk.BooleanVar()
tk.Label(frame3, text="Floor Height").pack(); tk.Entry(frame3, textvariable=floor_height).pack()
tk.Label(frame3, text="Floors").pack(); tk.Entry(frame3, textvariable=floor_count).pack()
tk.Checkbutton(frame3, text="Include Staircase", variable=staircase_var).pack()
tk.Button(frame3, text="Back", command=prev_step).pack(side='left', padx=10)
tk.Button(frame3, text="Generate Model", command=submit_final).pack(side='right', padx=10)
tk.Button(frame3, text="Preview Image", command=preview_image).pack(pady=5)
tk.Button(frame3, text="View Floor GIF", command=view_gif).pack(pady=5)
tk.Button(frame3, text="Export PDF", command=export_pdf).pack(pady=5)
tk.Button(frame3, text="Share via WhatsApp", command=share_on_whatsapp).pack(pady=5)

steps = [frame1, frame2, frame3]
steps[current_step].pack()
app.mainloop()
