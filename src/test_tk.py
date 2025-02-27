import tkinter as tk
root = tk.Tk()
root.title("Testfenster")
root.geometry("400x300+100+100")
tk.Label(root, text="Fenster-Test").pack(pady=20)
root.mainloop()
