import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk


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
        if isinstance(widget,RoundedButton) and widget not in selected_buttons:
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
canvas.create_image(0, 0, anchor="nw")

# Create a frame for the grid and place it using grid manager
grid_frame = tk.Frame(root, bg="lavender")
grid_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# Configure grid to resize dynamically
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Adjust this scale to control button size changes
button_size = 40

# Custom rounded corner button class
class RoundedButton(Canvas):
    def __init__(self, master=None, text="", radius=20, padding=5, bg="lightblue", fg="black", font=("Arial", 14, "bold"), **kw):
        super().__init__(master, width=radius*2, height=radius*2, bd=0, highlightthickness=0, **kw)
        self.radius = radius
        self.padding = padding
        self.bg = bg
        self.fg = fg
        self.font = font
        self.text = text
        
        self.create_rounded_rectangle(self.padding, self.padding, self.winfo_reqwidth()-self.padding, self.winfo_reqheight()-self.padding, radius=self.radius, fill=self.bg)
        self.create_text((self.winfo_reqwidth())//2, (self.winfo_reqheight())//2, text=self.text, fill=self.fg, font=self.font)
        
        # Bind events to handle the button interactions
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_button_motion)
        self.bind("<ButtonRelease-1>", self.on_button_release)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2-radius, y2-radius,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2-radius,
                  x1, y2-radius,
                  x1+radius, y1+radius]
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_button_press(self, event):
        # Handle button press event
        pass

    def on_button_motion(self, event):
        # Handle motion event
        pass

    def on_button_release(self, event):
        # Handle button release event
        pass

# Example usage of RoundedButton
root = tk.Tk()
root.title("Rounded Button Example")

grid_frame = tk.Frame(root, bg="lavender")
grid_frame.grid(padx=20, pady=20)

# Create a grid of rounded buttons
button_grid = []
crossword = [
    list("HELLO"),
    list("WORLD")
]

for i in range(len(crossword)):
    row = []
    for j in range(len(crossword[i])):
        letter = crossword[i][j]
        btn = RoundedButton(grid_frame, text=letter)
        btn.grid(row=i, column=j, padx=5, pady=5)
        row.append(btn)
    button_grid.append(row)

# Label to display the image, placed using grid
image_label = tk.Label(root, bg="lavender")
image_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")


# Function to resize the grid when the window size changes
def resize_buttons(event):
    global button_size
    grid_width = min(event.width, event.height)
    button_size = grid_width // len(crossword)

    for i in range(len(button_grid)):
        for j in range(len(button_grid[i])):
            btn = button_grid[i][j]
            btn.config(width=button_size//14, height=button_size//23)

# Bind the resize function to the grid_frame resize event
grid_frame.bind("<Configure>", resize_buttons)

# Run the main loop
root.mainloop()
