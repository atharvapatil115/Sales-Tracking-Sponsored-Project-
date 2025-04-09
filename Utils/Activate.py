import json
import os
import uuid
from tkinter import simpledialog, messagebox
from Utils.data_logger import log_info, log_error, log_warning
from datetime import datetime

# Paths for storing activation details
ACTIVATION_FILE = "activation_data.json"

# Load activation data from file
def load_activation_data():
    if os.path.exists(ACTIVATION_FILE):
        with open(ACTIVATION_FILE, "r") as file:
            return json.load(file)
    return {
        "activated_systems": [],
        "valid_keys": [
            "AB12-CD34-EF56-GH78",
            "IJ90-KL12-MN34-OP56",
            "QR78-ST90-UV12-WX34",
            "YZ56-AB78-CD90-EF12",
            "GH34-IJ56-KL78-MN90"
        ]
    }

# Save activation data to file
def save_activation_data(data):
    with open(ACTIVATION_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Get unique system identifier (MAC Address)
def get_system_id():
    mac_address = ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 48, 8))
    return mac_address

# Perform activation process
def activate_software():
    data = load_activation_data()
    system_id = get_system_id()

    if system_id in data["activated_systems"]:
        messagebox.showinfo("Activation Status", "Software is already activated!")
        log_info("Software is already activated!")
        return True

    key = simpledialog.askstring("Activation Required", "Enter your activation key:")
    
    if not key:
        log_warning("User did not enter an activation key.")
        messagebox.showerror("Activation Failed", "No activation key entered.")
        return False

    key = key.strip()
    
    if key in data["valid_keys"]:
        # Remove the key from the valid list and activate the system
        data["valid_keys"].remove(key)
        data["activated_systems"].append(system_id)
        save_activation_data(data)

        messagebox.showinfo("Activation Successful", "Your software is now activated.")
        log_info(f"Software activated for system {system_id} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return True
    else:
        messagebox.showerror("Activation Failed", "Invalid activation key entered.")
        log_error("Invalid activation key attempt.")
        return False

# Main function to check and activate
def main():
    data = load_activation_data()
    system_id = get_system_id()

    if system_id not in data["activated_systems"]:
        messagebox.showwarning("Activation Needed", "Software is not activated on this system!")
        
        if not activate_software():
            return False  # Stop execution if activation fails

    # messagebox.showinfo("Welcome", "Welcome to the Stock Management System!")
    return True  # Continue to application

if __name__ == "__main__":
    main()
