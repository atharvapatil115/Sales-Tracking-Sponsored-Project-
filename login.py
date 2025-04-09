import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Frontend import open_main
# Dictionary for user authentication
users = {'atharva': 'atharva123'}

def show_main():
    def Validation():
        username = username_entry.get()
        password = password_entry.get()
        if username in users and users[username] == password:
            messagebox.showinfo("Login Successful", f"Welcome {username}!")
            login_window.destroy()
            open_main()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    # Create the main login window
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("800x500")

    # Create left and right frames
    left_frame = tk.Frame(login_window, width=500, height=500, bg="white")
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = tk.Frame(login_window, width=400, height=500, bg="#cbe6d3")
    right_frame.pack(side="right", fill="both", expand=True)

    # Load and display the image in the left frame
    image_path = "download.jpeg"  # Ensure this path is correct
    try:
        image = Image.open(image_path).resize((500, 500))  # Resize to fit half window
        bg_image = ImageTk.PhotoImage(image)
        img_label = tk.Label(left_frame, image=bg_image)
        img_label.image = bg_image
        img_label.pack(fill="both", expand=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")
        return

    # Create an inner frame inside right_frame to center content
    inner_frame = tk.Frame(right_frame, bg="#cbe6d3")
    inner_frame.pack(expand=True)  # This makes it center vertically

    # Login form inside inner_frame
    tk.Label(inner_frame, text="Enter your name", font=("Helvetica", 14, "bold"), fg='Black', bg='#cbe6d3').pack(pady=10)
    username_entry = tk.Entry(inner_frame, width=25, font=('Arial', 14))
    username_entry.pack(pady=5)

    tk.Label(inner_frame, text="Enter your password", font=("Helvetica", 14, "bold"), fg='Black', bg='#cbe6d3').pack(pady=10)
    password_entry = tk.Entry(inner_frame, show="*", width=25, font=('Arial', 14))
    password_entry.pack(pady=5)

    login_button = tk.Button(inner_frame, text="Login", command=Validation, bg='#124163', fg='white', font=('Arial', 12, 'bold'))
    login_button.pack(pady=10)

    register_button = tk.Button(inner_frame, text="Register", bg='#32cd32', fg='white', font=('Arial', 12, 'bold'))
    register_button.pack(pady=5)

    login_window.mainloop()

show_main()
