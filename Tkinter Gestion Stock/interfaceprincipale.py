import tkinter as tk
import subprocess

def open_interface_1():
    subprocess.Popen(["python", "GestionClient.py"])

def open_interface_2():
    subprocess.Popen(["python", "GestionCommande.py"])


def perform_action_3():
    subprocess.Popen(["python", "GestionProduit.py"])

window = tk.Tk()
window.title("Open Interfaces and Actions")

# Set the size of the window in pixels
window.geometry("500x300")

# Create a frame to organize the buttons
button_frame = tk.Frame(window)
button_frame.pack(padx=20, pady=10)

# Create buttons for opening interfaces with larger fonts and size
button_font = ("Arial", 12)

# Create buttons with spacing
button_1 = tk.Button(button_frame, text="Gestion Client", command=open_interface_1, font=button_font, width=20, height=2)
button_1.pack(pady=10)  # Add vertical spacing

button_2 = tk.Button(window, text="Gestion Commande", command=open_interface_2,font=button_font, width=20, height=2)
button_2.pack(pady=10)


button_3 = tk.Button(window, text="Gestion Produit", command=perform_action_3,font=button_font, width=20, height=2)
button_3.pack(pady=10)

window.mainloop()
