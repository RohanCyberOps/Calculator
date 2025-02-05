import tkinter as tk
from tkinter import messagebox
import os
import pygame  # For sound effects

# Initialize Pygame for sound
pygame.mixer.init()

# Load sound effects
click_sound = "click.wav"
error_sound = ("error.mp3")

def play_sound(sound_file):
    pygame.mixer.Sound(sound_file).play()

# Function to perform calculations
def calculate(num1, num2, operator):
    try:
        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            if num2 == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            return num1 / num2
        elif operator == '**':
            return num1 ** num2
        elif operator == '%':
            if num2 == 0:
                raise ZeroDivisionError("Cannot perform modulus by zero.")
            return num1 % num2
        else:
            raise ValueError("Invalid operator.")
    except Exception as e:
        play_sound(error_sound)
        return f"Error: {e}"

# Function to handle calculation
def on_calculate(event=None):
    play_sound(click_sound)
    try:
        num1_text = entry_num1.get().strip()
        num2_text = entry_num2.get().strip()

        if not num1_text or not num2_text:
            raise ValueError("Both fields must be filled.")

        num1 = float(num1_text)
        num2 = float(num2_text)
        operator = operator_var.get()

        result = calculate(num1, num2, operator)

        if isinstance(result, str) and result.startswith("Error"):
            messagebox.showerror("Error", result)
        else:
            result_label.config(text=f"Result: {result}", fg="blue")
            history_listbox.insert(tk.END, f"{num1} {operator} {num2} = {result}")
    except ValueError as e:
        play_sound(error_sound)
        messagebox.showerror("Input Error", str(e))

# Function to clear history
def clear_history():
    play_sound(click_sound)
    history_listbox.delete(0, tk.END)
    result_label.config(text="Result: ", fg="black")

# Function to save history
def save_history():
    play_sound(click_sound)
    try:
        with open("calculator_history.txt", "w") as file:
            for item in history_listbox.get(0, tk.END):
                file.write(item + "\n")
        messagebox.showinfo("Success", "History saved successfully.")
    except Exception as e:
        messagebox.showerror("File Error", f"Error saving history: {e}")

# Function to load history
def load_history():
    play_sound(click_sound)
    try:
        if os.path.exists("calculator_history.txt"):
            with open("calculator_history.txt", "r") as file:
                history = file.readlines()
            history_listbox.delete(0, tk.END)
            for line in history:
                if line.strip():
                    history_listbox.insert(tk.END, line.strip())
        else:
            messagebox.showinfo("Info", "No history file found.")
    except Exception as e:
        messagebox.showerror("File Error", f"Error loading history: {e}")

# Function to toggle theme
def toggle_theme():
    play_sound(click_sound)
    global dark_mode
    if dark_mode:
        root.config(bg="#f0f0f0")
        for widget in root.winfo_children():
            widget.config(bg="#f0f0f0", fg="#333")
        dark_mode = False
        theme_button.config(text="🌞 Light Mode", bg="#007BFF", fg="white")
    else:
        root.config(bg="#1e1e1e")
        for widget in root.winfo_children():
            widget.config(bg="#1e1e1e", fg="white")
        dark_mode = True
        theme_button.config(text="🌙 Dark Mode", bg="#FF8C00", fg="black")

# GUI Setup
root = tk.Tk()
root.title("Calculator")
root.geometry("350x500")

# Default theme
dark_mode = False
root.config(bg="#f0f0f0")

# Fonts and Colors
FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 10, "bold")
BUTTON_COLOR = "#007BFF"
TEXT_COLOR = "#333"

# Input fields
tk.Label(root, text="Number 1:", font=FONT, bg=root["bg"], fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_num1 = tk.Entry(root, font=FONT)
entry_num1.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Number 2:", font=FONT, bg=root["bg"], fg=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_num2 = tk.Entry(root, font=FONT)
entry_num2.grid(row=1, column=1, padx=10, pady=10)

# Operator selection
tk.Label(root, text="Operator:", font=FONT, bg=root["bg"], fg=TEXT_COLOR).grid(row=2, column=0, padx=10, pady=10, sticky="w")
operator_var = tk.StringVar(value="+")
operator_menu = tk.OptionMenu(root, operator_var, "+", "-", "*", "/", "**", "%")
operator_menu.config(font=FONT, bg="white", fg=TEXT_COLOR)
operator_menu.grid(row=2, column=1, padx=10, pady=10)

# Buttons
calculate_button = tk.Button(root, text="Calculate", font=BUTTON_FONT, bg=BUTTON_COLOR, fg="white", command=on_calculate)
calculate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="we")

clear_button = tk.Button(root, text="Clear History", font=BUTTON_FONT, bg="red", fg="white", command=clear_history)
clear_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="we")

# Result display
result_label = tk.Label(root, text="Result: ", font=FONT, fg="black", bg=root["bg"])
result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# History section
tk.Label(root, text="History:", font=FONT, bg=root["bg"], fg=TEXT_COLOR).grid(row=6, column=0, padx=10, pady=5, sticky="w")
history_listbox = tk.Listbox(root, width=40, height=5, font=("Arial", 10))
history_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

# Save and Load buttons
save_button = tk.Button(root, text="Save History", font=BUTTON_FONT, bg=BUTTON_COLOR, fg="white", command=save_history)
save_button.grid(row=8, column=0, padx=10, pady=10, sticky="we")

load_button = tk.Button(root, text="Load History", font=BUTTON_FONT, bg=BUTTON_COLOR, fg="white", command=load_history)
load_button.grid(row=8, column=1, padx=10, pady=10, sticky="we")

# Theme Toggle Button
theme_button = tk.Button(root, text="🌞 Light Mode", font=BUTTON_FONT, bg=BUTTON_COLOR, fg="white", command=toggle_theme)
theme_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="we")

# Bind Enter key to trigger calculation
root.bind("<Return>", on_calculate)

# Run the GUI
root.mainloop()