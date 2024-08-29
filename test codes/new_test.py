import tkinter as tk
from tkinter import Canvas, font
from PIL import Image, ImageTk

# Function to create rounded buttons
def create_rounded_button(canvas, x, y, width, height, radius, text, command=None, font=None):
    canvas.create_oval(x, y, x + 2*radius, y + 2*radius, fill="lightblue", outline="")
    canvas.create_oval(x + width - 2*radius, y, x + width, y + 2*radius, fill="lightblue", outline="")
    canvas.create_oval(x, y + height - 2*radius, x + 2*radius, y + height, fill="lightblue", outline="")
    canvas.create_oval(x + width - 2*radius, y + height - 2*radius, x + width, y + height, fill="lightblue", outline="")
    canvas.create_rectangle(x + radius, y, x + width - radius, y + height, fill="lightblue", outline="")
    canvas.create_rectangle(x, y + radius, x + width, y + height - radius, fill="lightblue", outline="")
    button = tk.Button(canvas, text=text, font=font, width=1, height=1, relief="flat", bg="lightblue", command=command)
    button_window = canvas.create_window(x + width//2, y + height//2, window=button)
    return button, button_window

# Function to check if the selected word is correct
def check_word(selected_buttons, correct_words, word_labels, image_label):
    selected_word = ''.join([btn['text'] for btn in selected_buttons]).lower()
    correct_words_lower = [word.lower() for word in correct_words]

    if selected_word in correct_words_lower:
        for btn in selected_buttons:
            btn.config(bg="pink", state="disabled")  # Correct word: change color to pink and disable the buttons
        correct_word_index = correct_words_lower.index(selected_word)
        update_word_list(correct_words[correct_word_index], word_labels, image_label)
        correct_words.pop(correct_word_index)
    else:
        reset_selection(selected_buttons)

# Function to reset selection (for incorrect words)
def reset_selection(selected_buttons):
    for btn in selected_buttons:
        if btn['state'] != 'disabled':  # Only reset buttons that are not disabled
            btn.config(bg="lightblue")

# Function to handle button press
def handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels, image_label):
    if event.type == tk.EventType.ButtonPress:
        reset_selection(selected_buttons)
        selected_buttons.clear()
        select_button(event.widget, selected_buttons)
    elif event.type == tk.EventType.Motion:
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button) and widget not in selected_buttons:
            select_button(widget, selected_buttons)
    elif event.type == tk.EventType.ButtonRelease:
        check_word(selected_buttons, correct_words, word_labels, image_label)

# Function to handle button selection
def select_button(button, selected_buttons):
    selected_buttons.append(button)
    button.config(bg="lavender")

# Function to update the word list (crossing out the correct word) and display the image
def update_word_list(found_word, word_labels, image_label):
    for lbl in word_labels:
        if lbl['text'].lower() == found_word.lower():
            lbl.config(fg="gray", font="Arial 10 overstrike")
            break
    show_image(found_word, image_label)

# Function to set the image paths
def get_image_path(word):
    images = {
        "AdamSmith": "images/adam_smith.jpg",
        "CharlesBabbage": "images/charles_babbage.jpg",
        "EdwardsDeming": "images/edwards_deming.jpg",
        "EliWhitney": "images/eli_whitney.jpg",
        "EltonMayo": "images/elton_mayo.jpg",
        "FrederickWTaylor": "images/frederick_taylor.jpg",
        "HenryFord": "C:/Users/vivek/Desktop/new/henryFord.png",
        "HenryGantt": "C:/Users/vivek/Desktop/new/henryFord.png",
        "JamesPWomack": "images/james_womack.jpg",
        "JohnPKotter": "images/john_kotter.jpg",
        "JoshepMJuran": "images/joshep_juran.jpg",
        "KaoruIshikawa": "images/kaoru_ishikawa.jpg",
        "KurtLewin": "images/kurt_lewin.jpg",
        "MorrisCooke": "C:/Users/vivek/Desktop/new/moorisCokke.png",
        "PeterSenge": "images/peter_senge.jpg",
        "ShigeoShingo": "images/shigeo_shingo.jpg",
        "TaiichiOhno": "images/taiichi_ohno.jpg",
        "WalterAShewhart": "images/walter_shewhart.jpg"
    }
    return images.get(word, None)

# Check for the correct resampling method
try:
    resampling_method = Image.Resampling.LANCZOS
except AttributeError:
    # Fallback for older Pillow versions
    resampling_method = Image.LANCZOS

# Function to display the image
def show_image(word, image_label):
    image_path = get_image_path(word)
    if image_path:
        image = Image.open(image_path)
        image = image.resize((300, 486), resampling_method)  # Use the correct resampling method
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection

# Define the crossword puzzle as a list of lists
crossword = [
    list("EYPWEYKGXVTEJJOTOICQ"),
    list("LIKQKZWMGTLOFHSLFHIK"),
    list("ICHCMWTRNTHYLLPZACWS"),
    list("WMTZKWZAONIWELTRUKAH"),
    list("HRPXKGGNPBTHNQLEUMLC"),
    list("INOHVYMKQACAKEIXEPTO"),
    list("TQSLRAORIXRCSCJLQGEO"),
    list("NEHNYTCIVUABREVXFNRV"),
    list("EMEOTACGJMAZQENXDIAD"),
    list("YHQENHTMOBKQIKSLXMSR"),
    list("OLRYIIPWBTTNAGYRNEHO"),
    list("AUMOWEPAKKDTBOXDTDEF"),
    list("PDHOHSGSECIQEWHBTSWY"),
    list("RNASEEMORRISCOOKEDHR"),
    list("OEOMFVMOLBRRYPUMURAN"),
    list("FJAOSOGNIHSOEGIHSARE"),
    list("SJIYIMOFQHNIKDVQDWTH"),
    list("MKAORUISHIKAWAEXSDTT"),
    list("PABEZPETERSENGERSEFY"),
    list("OFQOGUNFHGIAFFMLFDGC")
]

# Define correct words
correct_words = [
    "AdamSmith", "CharlesBabbage", "EdwardsDeming",
    "EliWhitney", "EltonMayo", "FrederickWTaylor",
    "HenryFord", "HenryGantt",
    "JamesPWomack", "JohnPKotter", "JoshepMJuran",
    "KaoruIshikawa", "KurtLewin", "MorrisCooke",
    "PeterSenge", "ShigeoShingo", "TaiichiOhno",
    "WalterAShewhart"
]

# Create the main window
root = tk.Tk()
root.title("Interactive Criss-Cross Puzzle")
root.geometry("2560x1600")

# Create Canvas for background
canvas = Canvas(root)
canvas.grid(row=0, column=0, sticky="nsew")

# Create a frame for the grid
grid_frame = tk.Frame(canvas, bg="lavender")
canvas.create_window((0, 0), window=grid_frame, anchor="nw")

# Configure grid to resize dynamically
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Font settings
custom_font = font.Font(family="Arial", size=14, weight="bold")

# Adjust this scale to control button size changes
button_size = 40

# Create the grid of buttons inside larger frames
button_grid = []
selected_buttons = []

for i in range(len(crossword)):
    row = []
    for j in range(len(crossword[i])):
        letter = crossword[i][j]
        btn, btn_window = create_rounded_button(canvas, j * (button_size + 10), i * (button_size + 10), button_size, button_size, 10, text=letter, font=custom_font)
        btn.bind("<ButtonPress-1>", lambda event, btn_list=selected_buttons: handle_button_event(event, btn_list, button_grid, correct_words, word_labels, image_label))
        btn.bind("<B1-Motion>", lambda event, btn_list=selected_buttons: handle_button_event(event, btn_list, button_grid, correct_words, word_labels, image_label))
        btn.bind("<ButtonRelease-1>", lambda event, btn_list=selected_buttons: handle_button_event(event, btn_list, button_grid, correct_words, word_labels, image_label))
        row.append(btn)
    button_grid.append(row)

# Create a vertical list of words on the right
words_frame = tk.Frame(canvas, bg="lavender")
canvas.create_window((1000, 50), window=words_frame, anchor="nw")
word_labels = []
for word in correct_words:
    lbl = tk.Label(words_frame, text=word, font="Arial 12", bg="lavender")
    lbl.pack(anchor="w")
    word_labels.append(lbl)

# Create a label to display the image on the left
image_label = tk.Label(canvas, bg="white")
canvas.create_window((50, 50), window=image_label, anchor="nw")

# Start the Tkinter main loop
root.mainloop()
