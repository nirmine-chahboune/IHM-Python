import tkinter as tk
import sqlite3
from tkinter import ttk
import xml.etree.ElementTree as ET




# Création de la fenêtre principale
window = tk.Tk()
window.title("Gestion Client")

# Function to delete the selected client
def delete_selected_client():
    selected_item = tree.selection()
    if selected_item:
        id_to_delete = tree.item(selected_item, 'values')[0]

        # Delete from SQLite database
        cursor.execute("DELETE FROM client WHERE id=?", (id_to_delete,))
        conn.commit()

        # Delete from XML file (if exists)
        try:
            tree_xml = ET.parse('clients.xml')
            clients = tree_xml.getroot()
            for client in clients.findall('client'):
                existing_id = client.find('ID').text
                if existing_id == id_to_delete:
                    clients.remove(client)

            # Save the updated XML file
            tree_xml.write('clients.xml')
        except FileNotFoundError:
            pass

        # Remove the selected item from the Treeview
        tree.delete(selected_item)




# Connexion à la base de données SQLite
conn = sqlite3.connect('gestion.db')
cursor = conn.cursor()

# Exécution d'une requête pour récupérer les données de la table (ex. nom de la table : "client")
cursor.execute("CREATE TABLE IF NOT EXISTS client (id INTEGER PRIMARY KEY, nom TEXT, email TEXT)")
conn.commit()

# Création du tableau
tree = ttk.Treeview(window, columns=('ID', 'Nom', 'email'))

# Configuration des colonnes
tree.heading('#1', text='ID')
tree.column('#1', anchor='w', width=50)
tree.heading('#2', text='Nom')
tree.column('#2', anchor='w', width=100)
tree.heading('#3', text='Email')
tree.column('#3', anchor='w', width=80)

# Fonction pour ajouter une nouvelle client à la base de données SQLite
def add_client_to_db():
    id = id_entry.get()
    nom = nom_entry.get()
    email = email_entry.get()

    cursor.execute("INSERT INTO client (id, nom, email) VALUES (?, ?, ?)", (id, nom, email))
    conn.commit()

    id_entry.delete(0, 'end')
    nom_entry.delete(0, 'end')
    email_entry.delete(0, 'end')

    # Fetch the updated data from the database
    cursor.execute("SELECT * FROM client")
    data = cursor.fetchall()

    # Clear the existing table
    for row in tree.get_children():
        tree.delete(row)

    # Update the table with the new data
    for row in data:
        tree.insert('', 'end', values=row)

# Fonction pour sauvegarder les données en format XML
def save_to_xml():
    # Charger les données existantes à partir du fichier XML
    try:
        tree_xml = ET.parse('clients.xml')
        clients = tree_xml.getroot()
    except FileNotFoundError:
        # Si le fichier n'existe pas, créer un nouvel élément racine
        clients = ET.Element('clients')

    # Récupérer les données à partir des champs de saisie
    id = id_entry.get()
    nom = nom_entry.get()
    email = email_entry.get()

    # Vérifier si l'ID est déjà présent dans le fichier XML
    existing_ids = set()
    for client in clients.findall('client'):
        existing_id = client.find('ID').text
        existing_ids.add(existing_id)

    if id not in existing_ids:
        # L'ID est unique, créer un nouvel élément client avec les données saisies
        client = ET.Element('client')
        id_element = ET.Element('ID')
        id_element.text = id
        nom_element = ET.Element('Nom')
        nom_element.text = nom
        email_element = ET.Element('email')
        email_element.text = email

        client.append(id_element)
        client.append(nom_element)
        client.append(email_element)

        clients.append(client)

        # Enregistrer le fichier XML avec les nouvelles données
        tree_xml = ET.ElementTree(clients)
        tree_xml.write('clients.xml')
    else:
        print("ID déjà existant, veuillez utiliser un ID unique.")



# Remplissage du tableau avec les données de la base de données
cursor.execute("SELECT * FROM client")
data = cursor.fetchall()
for row in data:
    tree.insert('', 'end', values=row)

# Placement du tableau dans la fenêtre
tree.pack()

# Fonction pour fermer la connexion à la base de données
def close_db():
    conn.close()
    window.destroy()

# Entry fields for ID, nom, and email
id_label = tk.Label(window, text="ID:")
id_label.pack()
id_entry = tk.Entry(window)
id_entry.pack()

nom_label = tk.Label(window, text="Nom:")
nom_label.pack()
nom_entry = tk.Entry(window)
nom_entry.pack()

email_label = tk.Label(window, text="email:")
email_label.pack()
email_entry = tk.Entry(window)
email_entry.pack()

# Button to add the client to the database
add_button = tk.Button(window, text="Ajouter au DB (SQLite3)", command=add_client_to_db)
add_button.pack(side="left")

# Bouton pour sauvegarder les données en format XML
save_xml_button = tk.Button(window, text="Sauvegarder en XML", command=save_to_xml)
save_xml_button.pack(side="left")

# Create a "Delete" button
delete_button = tk.Button(window, text="Supprimer de db", command=delete_selected_client)
delete_button.pack(side="left")





# ... (existing code) ...

# Function to delete a client from the database and XML file using the ID from id_entry
def delete_client_by_id():
    id_to_delete = id_entry.get()

    # Delete from SQLite database
    cursor.execute("DELETE FROM client WHERE id=?", (id_to_delete,))
    conn.commit()

    # Delete from XML file (if exists)
    try:
        # Delete from XML file (if exists)
        tree_xml = ET.parse('clients.xml')
        clients = tree_xml.getroot()
        client_to_delete = None

        for client in clients.findall('client'):
            existing_id = client.find('ID').text
            if existing_id == id_to_delete:
                client_to_delete = client
                break

        if client_to_delete:
            clients.remove(client_to_delete)

            # Save the updated XML file
            tree_xml.write('clients.xml')
    except FileNotFoundError:
        pass

    # Clear the input field and update the Treeview widget
    id_entry.delete(0, 'end')

    # Re-populate the Treeview with updated data
    cursor.execute("SELECT * FROM client")
    data = cursor.fetchall()

    # Clear the existing table
    for row in tree.get_children():
        tree.delete(row)

    # Update the table with the new data
    for row in data:
        tree.insert('', 'end', values=row)

# ... (existing code) ...
# Create a "Delete" button
delete_button = tk.Button(window, text="Supprimer de XML", command=delete_client_by_id)
delete_button.pack(side="left")

# Bouton pour fermer la fenêtre
close_button = tk.Button(window, text="Fermer", command=close_db)
close_button.pack(side="left")

# Lancement de la boucle principale de l'interface graphique
window.mainloop()
