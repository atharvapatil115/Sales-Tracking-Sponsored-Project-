import tkinter as tk
from tkinter import Frame, Label, Button, Scrollbar, Canvas, simpledialog,messagebox
import pandas as pd
from Database.database_handler import Fetch_all_items, update_sales, add_stock, initialize_daily_balance,Fetch_today,add_product,update_price
from PIL import Image , ImageTk
from Utils.Activate import main
import os
from Reports.Report_generator import Combine


global buttons 
global curr_op 
global data
today = False
buttons = []
def open_main():
    
    bool = main()
    if bool:
        def display_login():
            global main_content
            main_content = Frame(root,bg="#cbe6d3")
            main_content.pack(fill="both", expand=True)
            users = {'atharva': 'atharva123'}
            def Validation():
                username = username_entry.get()
                password = password_entry.get()
                if username in users and users[username] == password:
                    messagebox.showinfo("Login Successful", f"Welcome {username}!")
                    # login_window.destroy()
                    left_frame.destroy()
                    right_frame.destroy()
                    show_categories("Update Sales")

                    for btn in buttons:
                        btn.config(state=tk.NORMAL)
                    btn_today.config(state=tk.NORMAL)
                    btn_combine.config(state=tk.NORMAL)
                    # open_main()
                else:
                    messagebox.showerror("Login Failed", "Invalid username or password.")
            left_frame = tk.Frame(main_content, width=430, height=480, bg="#cbe6d3")
            left_frame.pack(side="left", fill="both", expand=True)
            right_frame = tk.Frame(main_content, width=480, height=500, bg="#cbe6d3")
            right_frame.pack(side="right", fill="both", expand=True)
            image_path = "download.jpeg"  # Ensure this path is correct
            try:
                image = Image.open(image_path).resize((480,530))  # Resize to fit half window
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



            ###################################################
        initialize_daily_balance()

        def clear_placeholder(event):
            if search_entry.get() == "Search":
                search_entry.delete(0, tk.END)

        def add_placeholder(event):
            if not search_entry.get():
                search_entry.insert(0, "Search")

        def search_action():
            search_query = search_entry.get()
            if search_query and search_query != "Search":
                filter_table(search_query,headers_default)

        def logout(category):
            confirm  = messagebox.askyesnocancel("Logout","Are you sure you want to logout?")
            if confirm:
                    
                main_content.destroy()
                display_login()
                # display_login()

        def reload(selected_category):
            show_table(selected_category)

        def show_categories(action):
            global current_action, selected_category
            current_action = action
            selected_category = None
            main_content.pack_forget()
            main_content.pack(fill="both", expand=True)
            for widget in main_content.winfo_children():
                widget.destroy()

            Label(main_content, bg = "#cbe6d3",text=f"Select Category to {action}", font=("Arial", 16)).pack(pady=20)
            categories = ["Liquor", "Snacks", "ColdDrinks"]

            for category in categories:
                Button(main_content, text=category, font=("Arial", 12), width=50,
                    height=3,bg="White",
                    command=lambda c=category: show_table(c)).pack(pady=10)

        def show_table(category):
            global selected_category, data
            selected_category = category
            
            for widget in main_content.winfo_children():
                widget.destroy()

            Label(main_content,bg="#cbe6d3", text=f"{current_action} - {category}", font=("Arial", 16)).pack(pady=10)
            Label(main_content, bg="#cbe6d3",text="Enter Product ID:", font=("Arial", 12)).pack()

            product_id_entry = tk.Entry(main_content, font=("Arial", 12))
            product_id_entry.pack(pady=5, fill="x")
            product_id_entry.bind("<KeyRelease>", lambda event: filter_table(product_id_entry.get()))

            data = Fetch_all_items(category)
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data, columns=["ID", "Brand", "Price", "OB", "Added", "Total", "CB", "Total Sales"])

            table_container = Frame(main_content)
            table_container.pack(fill="both", expand=True)

            canvas = Canvas(table_container)
            scrollbar = Scrollbar(table_container, orient="vertical", command=canvas.yview)
            table_frame = Frame(canvas)
            
            canvas_window = canvas.create_window((0, 0), window=table_frame, anchor="nw")

            table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            table_container.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
            global headers_default
            headers_default = ["ID", "Brand", "Price", "OB", "Added", "Total", "CB", "Total Sales"]
            display_table(table_frame, data,headers_default)

        def show_today_sales():
            today = True
            global selected_category, data
            # selected_category = category
            
            for widget in main_content.winfo_children():
                widget.destroy()

            # Label(main_content,bg="#cbe6d3", text=f"{current_action} - {category}", font=("Arial", 16)).pack(pady=10)
            Label(main_content, bg="#cbe6d3",text="Enter Product ID:", font=("Arial", 12)).pack()

            product_id_entry = tk.Entry(main_content, font=("Arial", 12))
            product_id_entry.pack(pady=5, fill="x")
            product_id_entry.bind("<KeyRelease>", lambda event: filter_table(product_id_entry.get()))

            data = Fetch_today()
            print(f"front end data :{data}")
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data, columns=["Date", "ID", "Category", "Brand Name", "OB", "Added", "Total", "Total Sales","CB","Price","Total"])

            table_container = Frame(main_content)
            table_container.pack(fill="both", expand=True)

            canvas = Canvas(table_container)
            scrollbar = Scrollbar(table_container, orient="vertical", command=canvas.yview)
            table_frame = Frame(canvas)
            
            canvas_window = canvas.create_window((0, 0), window=table_frame, anchor="nw")

            table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            table_container.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
            headers_today = ["Date", "ID", "Category", "Brand Name", "OB", "Added", "Total", "Total Sales","CB","Price","Total"]
            display_table(table_frame, data,headers_today)
       
       
       
        def show_combined():
            global Start_date,End_date
            prompt_text = "Enter the Start Date"
            Start_date = simpledialog.askstring("Start Date",f"{prompt_text}")
            prompt_text = "Enter the End Date"
            End_date = simpledialog.askstring("End Date", f"{prompt_text}")
            today = True
            global selected_category, data
            # selected_category = category
            
            for widget in main_content.winfo_children():
                widget.destroy()

            # Label(main_content,bg="#cbe6d3", text=f"{current_action} - {category}", font=("Arial", 16)).pack(pady=10)
            Label(main_content, bg="#cbe6d3",text="Enter Product ID:", font=("Arial", 12)).pack()

            product_id_entry = tk.Entry(main_content, font=("Arial", 12))
            product_id_entry.pack(pady=5, fill="x")
            product_id_entry.bind("<KeyRelease>", lambda event: filter_table(product_id_entry.get()))

            data = Combine(Start_date,End_date)
            print(f"front end data :{data}")
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data, columns=["Date", "ID", "Category", "Brand Name", "OB", "Added", "Total", "Total Sales","CB","Price","Total"])

            table_container = Frame(main_content)
            table_container.pack(fill="both", expand=True)

            canvas = Canvas(table_container)
            scrollbar = Scrollbar(table_container, orient="vertical", command=canvas.yview)
            table_frame = Frame(canvas)
            
            canvas_window = canvas.create_window((0, 0), window=table_frame, anchor="nw")

            table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            table_container.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
            headers_combined = ["Date", "Category", "Product ID", "Brand Name", "OB", "Rec", "CB", "Price","Sold","Total","Total sale"]
            display_table(table_frame, data,headers_combined)

        def display_table(table_frame, table_data, headers):
            for widget in table_frame.winfo_children():
                widget.destroy()
        
            for col, header in enumerate(headers):
                label = tk.Label(table_frame, text=header, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, borderwidth=1, relief="solid")
                label.grid(row=0, column=col, sticky="nsew")

            for row_index, row in enumerate(table_data.itertuples(index=False), start=1):
                for col_index, value in enumerate(row):
                    cell = tk.Label(table_frame, text=value, font=("Arial", 10), padx=10, pady=5, borderwidth=1, relief="solid")
                    cell.grid(row=row_index, column=col_index, sticky="nsew")
                    cell.bind("<Button-1>", lambda event, r=row: get_user_input(r))
            
            for i in range(len(headers)):
                table_frame.grid_columnconfigure(i, weight=1)
        def filter_table(product_id):
            filtered_data = data[data['ID'].astype(str).str.startswith(product_id)] if product_id else data
            display_table(main_content.winfo_children()[-1], filtered_data,headers_default)
        
        def get_user_input(row):
            product_id, product_name = row.ID, row.Brand
            if current_action == "Update Sales":
                prompt_text = "Enter the number of items sold" 
                user_value = simpledialog.askinteger("Input", f"{prompt_text} for {product_name} (ID: {product_id}):", minvalue=0)
            elif current_action == "Add Stock":
                prompt_text = "Enter the number of items to be added"
                user_value = simpledialog.askinteger("Input", f"{prompt_text} for {product_name} (ID: {product_id}):", minvalue=0)
            elif current_action == "Update Price":
                prompt_text = "Enter the price"
                user_value = simpledialog.askinteger("Input", f"{prompt_text} for {product_name} (ID: {product_id}):", minvalue=0)
            elif current_action == "Add Product":
                prompt_text = "Enter the Product_id"
                user_value = simpledialog.askstring("Input", f"{prompt_text}")
                prompt_text = "Enter the Brand Name"
                Name_new = simpledialog.askstring("Input", f"{prompt_text}")
                prompt_text = "Enter the Price"
                price_new = simpledialog.askinteger("Input", f"{prompt_text}",minvalue=0)
                prompt_text = "Enter the Opening Balance"
                OB_new = simpledialog.askinteger("Input", f"{prompt_text}",minvalue=0)
               


                
                for widget in main_content.winfo_children():
                    widget.destroy()

                # Label(main_content, text=f"{current_action} - {category}", font=("Arial", 16)).pack(pady=10)
                Label(main_content, text="Enter Product ID:", font=("Arial", 12)).pack()

                product_id_entry = tk.Entry(main_content, font=("Arial", 12))
                product_id_entry.pack(pady=5, fill="x")
                product_id_entry.bind("<KeyRelease>", lambda event: filter_table(product_id_entry.get()))
                data=Fetch_all_items(selected_category)
                if not isinstance(data, pd.DataFrame):
                    data = pd.DataFrame(data, columns=["ID", "Brand", "Price", "OB", "Added", "Total", "CB", "Total Sales"])

                table_container = Frame(main_content)
                table_container.pack(fill="both", expand=True)

                canvas = Canvas(table_container)
                scrollbar = Scrollbar(table_container, orient="vertical", command=canvas.yview)
                table_frame = Frame(canvas)
            
                canvas_window = canvas.create_window((0, 0), window=table_frame, anchor="nw")

                table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                canvas.configure(yscrollcommand=scrollbar.set)
            
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
            
                table_container.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
                display_table(table_frame, data,headers_default)
                
            if user_value is not None:
                if current_action == "Update Sales":
                    update_sales(selected_category, product_id, user_value)
                    reload(selected_category)
                elif current_action == "Add Stock":
                    add_stock(product_id, selected_category, user_value)
                    reload(selected_category)
                elif current_action == "Update Price":
                    update_price(product_id,user_value,selected_category)
                    reload(selected_category)
                elif current_action == "View todays sales":
                    show_today_sales()
                    reload(selected_category)
                elif current_action == "Add Product":
                    # Combine(Start_date,End_date)
                    add_product(selected_category,user_value,Name_new,price_new,OB_new)
                    reload(selected_category)


        root = tk.Tk()
        root.title("Sales Tracking System")
        # w, h = 850, 580
        # ws = root.winfo_screenwidth()
        # hs = root.winfo_screenheight()
        # x = (ws // 2) - (w // 2)
        # y = (hs // 2) - (h // 2)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}")
        # root.geometry("850x580")
        root.minsize(800, 500)
        root.config(bg="#cbe6d3")

        top_frame = Frame(root, bg="#124163", height=50)
        top_frame.pack(fill="x")
        top_frame.place()
        global background

        

        Button(top_frame, bg="#cbe6d3",text="Logout", command=lambda: logout(selected_category)).pack(side="right", padx=10, pady=10)

        search_entry = tk.Entry(top_frame, width=50, font=("Arial", 12))
        search_entry.insert(0, "Search")
        search_entry.bind("<FocusIn>", clear_placeholder)
        search_entry.bind("<FocusOut>", add_placeholder)
        search_entry.pack(side="left", ipady=4, padx=5)

        Button(top_frame, text="GO", command=search_action).pack(side="left", padx=5)#green button

        sidebar = Frame(root, bg="#124163", width=200)
        sidebar.pack(side="left", fill="y")

        for btn_text in ["Add Product", "Update Sales", "Add Stock", "Update Price",  "Analysis", "Upcoming Stock"]:
            btn=Button(sidebar,bg = "#cbe6d3",text=btn_text, height=3, state=tk.DISABLED, command=lambda t=btn_text: show_categories(t))
            btn.pack(pady=5, padx=10, fill="x")
            buttons.append(btn)
        global btn_today,btn_combine
        btn_today=Button(sidebar,bg = "#cbe6d3",text="View todays sales", height=3, state=tk.DISABLED, command=lambda : show_today_sales())
        btn_today.pack(pady=5, padx=10, fill="x")
        btn_combine=Button(sidebar,bg = "#cbe6d3",text="Combine Reports", height=3, state=tk.DISABLED, command=lambda : show_combined())
        btn_combine.pack(pady=5, padx=10, fill="x")
    

        Todays_sales = Button(sidebar, text=btn_text, bg="white", height=3, command = lambda:Fetch_today()) 

        
    #     try:
    #         image_path = "download.jpeg"
        
    #         if not os.path.exists(image_path):
    #             raise FileNotFoundError(f"Image file not found: {image_path}")

    #         image = Image.open(image_path)
    #         image = image.resize((900, 400))  # Resize for better fitting
    #         global background  # Make it global to avoid garbage collection
    #         background = ImageTk.PhotoImage(image)  # Convert to Tkinter image

    #     # Apply image as a background label on main_content frame
    #         bg_label = Label(main_content, image=background)
    #         bg_label.place(relwidth=1, relheight=1)  # Cover entire frame

    #     except FileNotFoundError as e:
    #         messagebox.showerror("Error", str(e))
    #     except PermissionError:
    #         messagebox.showerror("Error", f"Permission denied for the image file: {image_path}")

    # # Set background image
    #     bg_label = Label(main_content, image=background)
    #     bg_label.place(relwidth=1, relheight=1)  # Cover the whole frame
    #     print("Image Path Exists:", os.path.exists(image_path))
    #     image = Image.open("Royal_park.jpeg")
        # image.show()


        display_login()
        root.mainloop()
# open_main()



    # issues