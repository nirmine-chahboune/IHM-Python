import sqlite3

conn = sqlite3.connect('gestion.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS client (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prix INTEGER
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fournisseur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS commande(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prix TEXT
    )
''')