import tkinter as tk
from select import select
from tkinter import messagebox
from PIL import Image, ImageTk

current_state = 'S'
selected_item = None

valid_items = ["apple", "banana", "carrot", "milk", "bread"]

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 500


def state_machine(input_action):
    global current_state, selected_item

    match current_state:
        case 'S':
            if input_action == "select_item":
                selected_item = item_input.get().lower()
                if selected_item in valid_items:
                    current_state = 'I'
                    label.config(text=f"Item '{selected_item}' selected, waiting for payment.")
                else:
                    show_error_and_reset(f"'{selected_item}' is not a valid item.")
            else:
                messagebox.showerror("Invalid Action", "Cannot perform action in the current state.")

        case 'I':
            if input_action == "enter_payment":
                entered_code = card_code_input.get()
                if len(entered_code) == 4 and entered_code.isdigit():
                    current_state = 'P'
                    label.config(text="Payment Accepted, waiting for confirmation.")
                else:
                    current_state = 'S'
                    show_error("Invalid payment code entered.")
            else:
                messagebox.showerror("Invalid Action", "You need to select an item first.")

        case 'P':
            if input_action == "confirm_transaction":
                label.config(text="Transaction Confirmed!")
                messagebox.showinfo("Transaction", "Transaction completed successfully!")
                reset_machine()
            else:
                messagebox.showerror("Invalid Action", "Cannot confirm the transaction.")


def show_error_and_reset(error_message):
    messagebox.showerror("Error", error_message)
    reset_machine()

def show_error(error_message):
    global current_state, selected_item
    messagebox.showerror("Error", error_message)
    current_state = 'I'
    selected_item = item_input.get().lower()
    card_code_input.delete(0, tk.END)
    label.config(text="POS Machine Ready. Please enter PIN again.")


def reset_machine():
    global current_state, selected_item
    current_state = 'S'
    selected_item = None
    item_input.delete(0, tk.END)
    card_code_input.delete(0, tk.END)
    label.config(text="POS Machine Ready. Please select an item.")


def load_dfa_image():
    image = Image.open("states.png")
    image = image.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.image = photo


root = tk.Tk()
root.title("POS Machine")

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.pack(side=tk.LEFT)

load_dfa_image()

input_frame = tk.Frame(root)
input_frame.pack(side=tk.RIGHT, padx=10, pady=10)

item_label = tk.Label(input_frame, text="Enter Item:")
item_label.pack()
item_input = tk.Entry(input_frame)
item_input.pack()

card_code_label = tk.Label(input_frame, text="Enter 4-digit Card Code:")
card_code_label.pack()
card_code_input = tk.Entry(input_frame)
card_code_input.pack()

available_items_label = tk.Label(input_frame, text="Available Items:")
available_items_label.pack(pady=10)
item_listbox = tk.Listbox(input_frame)
item_listbox.pack()

for item in valid_items:
    item_listbox.insert(tk.END, item)

select_item_button = tk.Button(input_frame, text="Select Item", command=lambda: state_machine("select_item"))
enter_payment_button = tk.Button(input_frame, text="Enter Payment", command=lambda: state_machine("enter_payment"))
confirm_button = tk.Button(input_frame, text="Confirm Transaction",
                           command=lambda: state_machine("confirm_transaction"))
reset_button = tk.Button(input_frame, text="Reset Machine", command=reset_machine)

select_item_button.pack(pady=10)
enter_payment_button.pack(pady=10)
confirm_button.pack(pady=10)
reset_button.pack(pady=10)

label = tk.Label(input_frame, text="POS Machine Ready. Please select an item.")
label.pack(pady=20)

root.mainloop()
