import tkinter as tk

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
root.geometry("2560x1600")  # Set the window size to full screen

# Create a frame for the grid and word list
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")

# Set grid proportions for main_frame
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create the frame for the puzzle grid (40% of the width)
grid_frame = tk.Frame(main_frame, bg="lavender")
grid_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
main_frame.grid_columnconfigure(0, weight=2)  # Set the grid frame to take 40% width

# Create the frame for the word list (60% of the width)
words_frame = tk.Frame(main_frame, bg="lightgray")
words_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
main_frame.grid_columnconfigure(1, weight=3)  # Set the words frame to take 60% width

# Create the grid of buttons
button_grid = []
selected_buttons = []

for i in range(len(crossword)):
    row = []
    for j in range(len(crossword[i])):
        letter = crossword[i][j]

        # Create the buttons for the grid
        btn = tk.Button(grid_frame, text=letter, width=2, height=1, font=("Arial", 18, "bold"),
                        bg="lightblue", relief="flat", bd=0)
        btn.grid(row=i, column=j, padx=2, pady=2, ipadx=5, ipady=5, sticky="nsew")
        btn.bind("<ButtonPress-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels))
        btn.bind("<B1-Motion>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels))
        btn.bind("<ButtonRelease-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels))
        row.append(btn)
    button_grid.append(row)

# Create the word list
word_labels = []
for idx, word in enumerate(correct_words):
    lbl = tk.Label(words_frame, text=word, font=("Arial", 14), bg="lightgray", anchor="w")
    lbl.grid(row=idx, column=0, padx=10, pady=5, sticky="w")
    word_labels.append(lbl)

# Adjust grid_frame to resize dynamically
grid_frame.grid_propagate(False)
grid_frame.update_idletasks()
grid_frame.config(width=root.winfo_width() * 0.4)

# Run the main loop
root.mainloop()
