import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk, ImageFilter

# Function to check if the selected word is correct
def check_word(selected_buttons, correct_words, word_labels):
    selected_word = ''.join([btn['text'] for btn in selected_buttons]).lower()
    correct_words_lower = [word.lower() for word in correct_words]

    if selected_word in correct_words_lower:
        for btn in selected_buttons:
            btn.config(bg="pink", state="disabled")  # Correct word: change color to pink and disable the buttons
        correct_word_index = correct_words_lower.index(selected_word)
        update_word_list(correct_words[correct_word_index], word_labels)
        correct_words.pop(correct_word_index)
    else:
        reset_selection(selected_buttons)

# Function to reset selection (for incorrect words)
def reset_selection(selected_buttons):
    for btn in selected_buttons:
        if btn['state'] != 'disabled':  # Only reset buttons that are not disabled
            btn.config(bg="SystemButtonFace")

# Function to handle button press
def handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels):
    if event.type == tk.EventType.ButtonPress:
        reset_selection(selected_buttons)
        selected_buttons.clear()
        select_button(event.widget, selected_buttons)
    elif event.type == tk.EventType.Motion:
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button) and widget not in selected_buttons:
            select_button(widget, selected_buttons)
    elif event.type == tk.EventType.ButtonRelease:
        check_word(selected_buttons, correct_words, word_labels)

# Function to handle button selection
def select_button(button, selected_buttons):
    selected_buttons.append(button)
    button.config(bg="lavender")

# Function to update the word list (crossing out the correct word)
def update_word_list(found_word, word_labels):
    for lbl in word_labels:
        if lbl['text'].lower() == found_word.lower():
            lbl.config(fg="gray", font="Arial 10 overstrike")
            break

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

# Configure grid to resize dynamically
for i in range(len(crossword)):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Create the grid of buttons inside larger frames
button_grid = []
selected_buttons = []

for i in range(len(crossword)):
    row = []
    for j in range(len(crossword[i])):
        frame = tk.Frame(root, width=60, height=60)  # Larger frame for spacing
        frame.grid_propagate(False)  # Prevent frame from resizing
        frame.grid(row=i, column=j, sticky="nsew")

        letter = crossword[i][j]
        btn = tk.Button(frame, text=letter, width=2, height=1)  # Smaller button, centered
        btn.pack(expand=True)  # Center the button in the frame
        btn.bind("<ButtonPress-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels))
        btn.bind("<B1-Motion>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels))
        btn.bind("<ButtonRelease-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels))
        row.append(btn)
    button_grid.append(row)


    # Load background image
bg_image = Image.open("background_image.jpg").convert("RGBA")
bg_image = bg_image.filter(ImageFilter.GaussianBlur(5))  # Blur effect
bg_image = Image.blend(bg_image, Image.new("RGBA", bg_image.size, (255, 255, 255, 255)), 0.5)  # Transparency effect
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a list of words outside the grid
word_labels = []
for idx, word in enumerate(correct_words):
    lbl = tk.Label(root, text=word, font="Arial 10 bold")
    lbl.grid(row=idx, column=len(crossword[0]) + 1, padx=10, sticky="w")
    word_labels.append(lbl)

# Run the main loop
root.mainloop()