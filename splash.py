import tkinter as tk
from tkinter import PhotoImage

# Typing animation function
def type_text(label, text, delay=100):
    def animate(i=0):
        if i <= len(text):
            label.config(text=text[:i])
            splash.after(delay, animate, i + 1)
            
    animate()
    label.config(text="")
    animate()

# Function to launch main app
def show_main():
    splash.destroy()
    import Frontend
    Frontend.open_main()

# Create splash window
splash = tk.Tk()
splash.overrideredirect(True)
splash.config(bg="white")

# Center it on screen
w, h = 400, 350
ws = splash.winfo_screenwidth()
hs = splash.winfo_screenheight()
x = (ws // 2) - (w // 2)
y = (hs // 2) - (h // 2)
splash.geometry(f"{w}x{h}+{x}+{y}")

# Load the logo
try:
    logo_img = PhotoImage(file="download.png")  # Ensure it's a PNG
    logo = tk.Label(splash, image=logo_img, bg="white")
    logo.pack(pady=(30, 10))
except Exception as e:
    print(f"Couldn't load image: {e}")

# Label for typing effect
label = tk.Label(splash, text="", font=("Arial", 16), bg="white")
label.pack()

# Footer
tk.Label(splash, text="© Atharva Patil, Sakshi Pawar, Neeraj Sharma. All rights reserved.", font=("Arial", 10), bg="white").pack(side="bottom", pady=10)

# Start the typing animation
type_text(label, "Loading Stocks Manager...")

# Launch main app after 3 sec
splash.after(8000, show_main)

splash.mainloop()
