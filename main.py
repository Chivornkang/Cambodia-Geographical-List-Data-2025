
import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

DATA_FILE = Path(__file__).parent / "src" / "CambodiaGeographicalList2025.json"

with open(DATA_FILE, encoding="utf-8") as file:
    data = json.load(file)

root = tk.Tk()
root.title("Cambodia Address Selector")
root.geometry("600x550")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Arial", 11))
style.configure("TCombobox", font=("Arial", 11), padding=8)
style.configure("TButton", font=("Arial", 11), padding=8)

translations = {
    "English": {
        "title": "Cambodia Address",
        "language": "Language",
        "Province": "Province",
        "District": "District",
        "Commune": "Commune",
        "Village": "Village",
        "address": "Selected Address",
        "copy": "Copy Address",
        "clear": "Clear",
        "warning": "Please select all locations."
    },
    "ខ្មែរ": {
        "title": "ជ្រើសរើសអាសយដ្ឋាន",
        "language": "ភាសា",
        "Province": "រាជធានី / ខេត្ត",
        "District": "ក្រុង / ស្រុក / ខណ្ឌ",
        "Commune": "ឃុំ / សង្កាត់",
        "Village": "ភូមិ",
        "address": "អាសយដ្ឋានដែលបានជ្រើសរើស",
        "copy": "ចម្លងអាសយដ្ឋាន",
        "clear": "សម្អាត",
        "warning": "សូមជ្រើសរើសទីតាំងទាំងអស់។"
    }
}

language = tk.StringVar(value="ខ្មែរ")

levels = {
    "Province": "districts",
    "District": "communes",
    "Commune": "villages",
    "Village": None
}

selected = {}
options = {}
comboboxes = {}
labels = {}

header = ttk.Frame(root, padding=25)
header.pack(fill="x")

title_label = ttk.Label(header, font=("Arial", 18, "bold"))
title_label.pack(side="left")

language_combo = ttk.Combobox(
    header,
    textvariable=language,
    values=["English", "ខ្មែរ"],
    state="readonly",
    width=12
)
language_combo.pack(side="right")

main = ttk.Frame(root, padding=(25, 5, 25, 20))
main.pack(fill="both", expand=True)

for level in levels:
    frame = ttk.Frame(main)
    frame.pack(fill="x", pady=9)

    label = ttk.Label(frame, width=18)
    label.pack(side="left")

    combo = ttk.Combobox(frame, state="readonly", width=48)
    combo.pack(side="left", fill="x", expand=True)

    labels[level] = label
    comboboxes[level] = combo

address_label = ttk.Label(main)
address_label.pack(anchor="w", pady=(25, 8))

address_box = tk.Text(
    main,
    height=4,
    font=("Arial", 13),
    wrap="word",
    padx=10,
    pady=10
)
address_box.pack(fill="x")

buttons = ttk.Frame(main)
buttons.pack(fill="x", pady=15)

def display_name(item):
    return f"{item['name_kh']} "

def clear_levels(start):
    names = list(levels)
    index = names.index(start)

    for level in names[index:]:
        comboboxes[level].set("")
        comboboxes[level]["values"] = ()
        selected.pop(level, None)
        options.pop(level, None)

    update_address()

def load_level(level, items):
    options[level] = {
        display_name(item): item for item in items
    }

    comboboxes[level]["values"] = list(options[level].keys())
    comboboxes[level].set("")

def on_select(level):
    item = options[level].get(comboboxes[level].get())

    if not item:
        return

    selected[level] = item

    names = list(levels)
    index = names.index(level)

    if index + 1 < len(names):
        next_level = names[index + 1]
        clear_levels(next_level)
        load_level(next_level, item.get(levels[level], []))

    update_address()

def get_address():
    if len(selected) != 4:
        return ""

    return ", ".join(
        selected[level]["name_kh"]
        for level in reversed(levels)
    )

def update_address():
    address_box.delete("1.0", "end")
    address_box.insert("1.0", get_address())

def copy_address():
    address = address_box.get("1.0", "end").strip()

    if not address:
        messagebox.showwarning(
            translations[language.get()]["title"],
            translations[language.get()]["warning"]
        )
        return

    root.clipboard_clear()
    root.clipboard_append(address)
    root.update()

def clear_all():
    selected.clear()
    options.clear()

    for level in levels:
        comboboxes[level].set("")
        comboboxes[level]["values"] = ()

    load_level("Province", data)
    update_address()

def update_language(*args):
    lang = translations[language.get()]

    root.title(lang["title"])
    title_label.config(text=lang["title"])
    address_label.config(text=lang["address"])

    for level in levels:
        labels[level].config(text=lang[level])

    copy_button.config(text=lang["copy"])
    clear_button.config(text=lang["clear"])

for level in levels:
    comboboxes[level].bind(
        "<<ComboboxSelected>>",
        lambda event, name=level: on_select(name)
    )

copy_button = ttk.Button(buttons, command=copy_address)
copy_button.pack(side="left")

clear_button = ttk.Button(buttons, command=clear_all)
clear_button.pack(side="right")

language.trace_add("write", update_language)

load_level("Province", data)
update_language()

root.mainloop()
