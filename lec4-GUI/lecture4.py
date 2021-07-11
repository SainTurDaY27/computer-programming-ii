import tkinter as tk


def say_hello():
    print("Hello")


# root window creation
root = tk.Tk()
root.title("My first GUI App")
root.geometry("300x100")
# widget creation
label = tk.Label(root, text="Welcome to my GUI application").pack()
btn_hello = tk.Button(root, text="Hello", command=say_hello).pack()
btn_quit = tk.Button(root, text="Quit", command=root.destroy).pack()
# running loop
root.mainloop()
