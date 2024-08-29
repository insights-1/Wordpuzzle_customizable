import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk, ImageFilter

# Function to display scientist information and image
def display_scientist_info(scientist_name):
    # Clear previous content
    for widget in info_frame.winfo_children():
        widget.destroy()

    # Load and display image
    image = Image.open(f"{scientist_name}.jpg")  # Make sure images are named accordingly and stored in the same directory
    image = image.resize((200, 200), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(info_frame, image=photo)
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.pack(pady=10)

    # Display scientist information
    info_label = tk.Label(info_frame, text=f"Information about {scientist_name}", font=("Arial", 12))
    info_label.pack(pady=10)

# Function to check if the selected word is correct
def check_word(selected_buttons, correct_words, word_labels):
    selected_word = ''.join([btn['text'] for btn in selected_buttons]).lower()
    correct_words_lower = [word.lower() for word in correct_words]

    if selected_word in correct_words_lower:
        for btn in selected_buttons:
            btn.config(bg="pink", state="disabled")  # Correct word: change color to pink and disable the buttons
        correct_word_index = correct_words_lower.index(selected_word)
        update_word_list(correct_words[correct_word_index], word_labels)
        correct_name = correct_words.pop(correct_word_index)
        display_scientist_info(correct_name)  # Display info when correct word is found
    else:
        reset_selection(selected_buttons)

# Function to reset selection (for incorrect words)
def reset_selection(selected_buttons):
    for btn in selected_buttons:
        if btn['state'] != 'disabled':  # Only reset buttons that are not disabled
            btn.config(bg="lightblue")

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
root.geometry("2560x1600")

# Create Canvas for background
canvas = Canvas(root)
canvas.grid(row=0, column=1, sticky="nsew")
canvas.create_image(0, 0, anchor="nw")

# Create a frame for the grid
grid_frame = tk.Frame(canvas, bg="lavender")
canvas.create_window((0, 0), window=grid_frame, anchor="nw")

# Create a frame for the scientist information on the left
info_frame = tk.Frame(root, bg="white", width=200)
info_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

# Configure grid to resize dynamically
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Adjust this scale to control button size changes
button_size = 40

# Create the grid of buttons inside larger frames
button_grid = []
selected_buttons = []

for i in range(len(crossword)):
    row = []
    for j in range(len(crossword[i])):
        letter = crossword[i][j]

        # Create rounded rectangle buttons
        btn = tk.Button(grid_frame, text=letter, width=button_size//10, height=button_size//20, font=("Arial", 14, "bold"),
                        bg="lightblue", relief="flat", bd=0)
        btn.grid(row=i, column=j, padx=6, pady=6, ipadx=2, ipady=2, sticky="nsew")
        btn.bind("<ButtonPress-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels))
        btn.bind("<B1-Motion>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels))
        btn.bind("<ButtonRelease-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels))
        row.append(btn)
    button_grid.append(row)

# Create a list of words outside the grid
word_labels = []
for idx, word in enumerate(correct_words):
    lbl = tk.Label(grid_frame, text=word, font="Arial 10 bold", bg="lightgray")
    lbl.grid(row=idx, column=len(crossword[0]) + 1, padx=10, pady=1, sticky="w")
    word_labels.append(lbl)

# Function to resize the grid when the window size changes
def resize_grid(event):
    global button_size
    grid_width = min(event.width, event.height)
    button_size = grid_width // len(crossword)

    for i in range(len(button_grid)):
        for j in range(len(button_grid[i])):
            btn = button_grid[i][j]
            btn.config(width=button_size//14, height=button_size//23, font=("Arial", button_size//4))

# Bind the resize function to the canvas resize event
canvas.bind("<Configure>", resize_grid)

# Run the main loop
root.mainloop()
