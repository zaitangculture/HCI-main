import tkinter as tk

def on_button_click():
    label.config(text="Hello, Tkinter!")

root = tk.Tk()
root.title("Tkinter Example")

label = tk.Label(root, text="Hello, World!")
label.pack()

button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack()

root.mainloop()
