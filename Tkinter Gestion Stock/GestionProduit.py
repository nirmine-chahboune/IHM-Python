import tkinter as tk
import sqlite3
from tkinter import ttk
import xml.etree.ElementTree as ET

# Création de la fenêtre principale
window = tk.Tk()
window.title("Gestion Produit")

# Connexion à la base de données SQLite
conn = sqlite3.connect('gestion.db')
cursor = conn.cursor()

# Exécution d'une requête pour récupérer les données de la table (ex. nom de la table : "produits")
cursor.execute("CREATE TABLE IF NOT EXISTS produits (id INTEGER PRIMARY KEY, nom TEXT, prix REAL)")
conn.commit()

# Création du tableau
tree = ttk.Treeview(window, columns=('ID', 'Nom', 'Prix'))

# Configuration des colonnes
tree.heading('#1', text='ID')
tree.column('#1', anchor='w', width=50)
tree.heading('#2', text='Nom')
tree.column('#2', anchor='w', width=100)
tree.heading('#3', text='Prix')
tree.column('#3', anchor='w', width=80)

# Fonction pour ajouter un nouveau produit à la base de données SQLite
def add_product_to_db():
    id = id_entry.get()
    nom = nom_entry.get()
    prix = prix_entry.get()

    cursor.execute("INSERT INTO produits (id, nom, prix) VALUES (?, ?, ?)", (id, nom, prix))
    conn.commit()

    id_entry.delete(0, 'end')
    nom_entry.delete(0, 'end')
    prix_entry.delete(0, 'end')

    # Fetch the updated data from the database
    cursor.execute("SELECT * FROM produits")
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
        tree_xml = ET.parse('products.xml')
        products = tree_xml.getroot()
    except FileNotFoundError:
        # Si le fichier n'existe pas, créer un nouvel élément racine
        products = ET.Element('Products')
        

    # Récupérer les données à partir des champs de saisie
    id = id_entry.get()
    nom = nom_entry.get()
    prix = prix_entry.get()
  # Vérifier si l'ID est déjà présent dans le fichier XML
    existing_ids = set()
    for product in products.findall('product'):
        existing_id = product.find('ID').text
        existing_ids.add(existing_id)

    if id not in existing_ids:
        # L'ID est unique, créer un nouvel élément product avec les données saisies
        product = ET.Element('product')
        id_element = ET.Element('ID')
        id_element.text = id
        nom_element = ET.Element('Nom')
        nom_element.text = nom
        prix_element = ET.Element('prix')
        prix_element.text =prix

        product.append(id_element)
        product.append(nom_element)
        product.append(prix_element)

        products.append(product)

        # Enregistrer le fichier XML avec les nouvelles données
        tree_xml = ET.ElementTree(products)
        tree_xml.write('products.xml')
    else:
        print("ID déjà existant, veuillez utiliser un ID unique.")



# Remplissage du tableau avec les données de la base de données
cursor.execute("SELECT * FROM produits")
data = cursor.fetchall()
for row in data:
    tree.insert('', 'end', values=row)

# Placement du tableau dans la fenêtre
tree.pack()

# Fonction pour fermer la connexion à la base de données
def close_db():
    conn.close()
    window.destroy()

# Entry fields for ID, nom, and prix
id_label = tk.Label(window, text="ID:")
id_label.pack()
id_entry = tk.Entry(window)
id_entry.pack()

nom_label = tk.Label(window, text="Nom:")
nom_label.pack()
nom_entry = tk.Entry(window)
nom_entry.pack()

prix_label = tk.Label(window, text="Prix:")
prix_label.pack()
prix_entry = tk.Entry(window)
prix_entry.pack()

# Button to add the product to the database
add_button = tk.Button(window, text="Ajouter au DB (SQLite3)", command=add_product_to_db)
add_button.pack()

# Bouton pour sauvegarder les données en format XML
save_xml_button = tk.Button(window, text="Sauvegarder en XML", command=save_to_xml)
save_xml_button.pack()

# Bouton pour fermer la fenêtre
close_button = tk.Button(window, text="Fermer", command=close_db)
close_button.pack()

# Lancement de la boucle principale de l'interface graphique
window.mainloop()
