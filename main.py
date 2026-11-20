
import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

DATA_FILE = Path(__file__).parent / "src" / "CambodiaGeographicalList2025.json"

with open(DATA_FILE, encoding="utf-8") as file:
    data = json.load(file)

root = tk.Tk()
root.title("Cambodia Address Selector")
root.geometry("600x450")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Arial", 11))
style.configure("TCombobox", font=("Arial", 11), padding=8)
style.configure("TButton", font=("Arial", 11), padding=8)

main = ttk.Frame(root, padding=25)
main.pack(fill="both", expand=True)

ttk.Label(
    main,
    text="Cambodia Address Selector",
    font=("Arial", 19, "bold")
).pack(pady=(0, 25))

levels = {
    "Province": "districts",
    "District": "communes",
    "Commune": "villages",
    "Village": None
}

comboboxes = {}
selected = {}
options = {}

for level in levels:
    frame = ttk.Frame(main)
    frame.pack(fill="x", pady=9)

    ttk.Label(frame, text=level, width=12).pack(side="left")

    combo = ttk.Combobox(frame, state="readonly", width=42)
    combo.pack(side="left", fill="x", expand=True)

    comboboxes[level] = combo

def display_name(item):
    return f"{item['name_kh']} ({item['code']})"

def clear_levels(start):
    names = list(levels)
    index = names.index(start)

    for level in names[index:]:
        comboboxes[level].set("")
        comboboxes[level]["values"] = ()
        selected.pop(level, None)
        options.pop(level, None)

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
        child_key = levels[level]

        clear_levels(next_level)
        load_level(next_level, item.get(child_key, []))

def show_result():
    if len(selected) != 4:
        messagebox.showwarning(
            "Warning",
            "Please select all locations."
        )
        return

    result = "\n".join(
        f"{level}: {selected[level]['name_kh']} "
        f"({selected[level]['code']})"
        for level in levels
    )

    messagebox.showinfo("Selected Address", result)

for level in levels:
    comboboxes[level].bind(
        "<<ComboboxSelected>>",
        lambda event, name=level: on_select(name)
    )

ttk.Button(
    main,
    text="Get Selected Address",
    command=show_result
).pack(fill="x", pady=25)

load_level("Province", data)

root.mainloop()
