import tkinter as tk
import json
import os
from PIL import Image, ImageTk

window = tk.Tk()

window.title("Applications")
window.geometry("1080x720")
window.minsize(760, 480)

def show_frame(frame):
    frame.tkraise()

def open_file(file):
    os.startfile(file)

def load_file():
    try:
        with open("base.json", "r") as file:
            return json.load(file)
    except:
        return {}

def write_file(data):
    with open("base.json", "w") as file:
        json.dump(data, file, indent=4)

def submit_form():
    nom = entry_nom.get()
    logo = entry_logo.get()
    url = entry_url.get()

    data = load_file()

    data[nom] = {
        "logo": logo,
        "url": url
    }
    write_file(data)

    show_frame(page1)

def put_app():
    for widget in content_app.winfo_children():
        widget.destroy()
    data = load_file()
    for nom, infos in data.items():
        logo = infos["logo"]
        chemin = infos["url"]
        if logo and os.path.exists(logo):
            img = Image.open(logo)
            img = img.resize((100, 100))

            photo = ImageTk.PhotoImage(img)
        else:
            img = Image.open("ifnoimage.ico")
            img = img.resize((100, 100))

            photo = ImageTk.PhotoImage(img)

        btn = tk.Button(content_app, image=photo, text=nom, font=("Arial", 16), command=lambda p=chemin: (open_file(p)))
        btn.pack(side="left", padx=(5))
        btn.image = photo

def on_creat():
    submit_form()
    put_app()


containeur = tk.Frame(window)
containeur.pack()

page1 = tk.Frame(containeur)
page2 = tk.Frame(containeur)

show_frame(page1)

for frame in (page1, page2):
    frame.grid(row=0, column=0, sticky="nsew")

# Page 1
tk.Label(page1, text="Bienvenue", font=("Arial", 25)).pack()
tk.Label(page1, text="Lancez vos application", font=("Arial", 18)).pack()
tk.Button(page1, text="Ajouter manuellement", command=lambda: show_frame(page2)).pack()
content_app = tk.Frame(page1)
content_app.pack(pady=(25, 0))
put_app()


# Page 2
tk.Label(page2, text="Configurer une nouvelle application", font=("Arial", 25)).pack()

content_nom = tk.Frame(page2)
tk.Label(content_nom, text="Nom de l'application", font=("Arial", 16)).pack()
entry_nom = tk.Entry(content_nom, width=50, font=("Arial", 14))
entry_nom.pack()
content_nom.pack(pady=(25, 0))

content_logo = tk.Frame(page2)
tk.Label(content_logo, text="Logo de l'application", font=("Arial", 16)).pack()
entry_logo = tk.Entry(content_logo, width=50, font=("Arial", 14))
entry_logo.pack()
content_logo.pack(pady=(25, 0))

content_url = tk.Frame(page2)
tk.Label(content_url, text="Chemin de l'application", font=("Arial", 16)).pack()
entry_url = tk.Entry(content_url, width=50, font=("Arial", 14))
entry_url.pack()
content_url.pack(pady=(25, 0))

content_button = tk.Frame(page2)
content_button.pack(pady=(25, 0))
tk.Button(content_button, text="Créer", font=("Arial", 16), command=on_creat).pack(side="left", padx=(0, 10))
tk.Button(content_button, text="Annuler", font=("Arial", 16), command=lambda: show_frame(page1)).pack(padx=(10, 0))

window.mainloop()
