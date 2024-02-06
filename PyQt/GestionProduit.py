import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QFont
import sqlite3
import xml.etree.ElementTree as ET

class ProductWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gestion Produit")
        self.setGeometry(100, 100, 800, 400)

        layout = QVBoxLayout()

        id_label = QLabel('ID:')
        self.id_input = QLineEdit()
        nom_label = QLabel('Nom:')
        self.nom_input = QLineEdit()
        prix_label = QLabel('Prix:')
        self.prix_input = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(nom_label)
        layout.addWidget(self.nom_input)
        layout.addWidget(prix_label)
        layout.addWidget(self.prix_input)

        add_button_db = QPushButton('Ajouter au DB (SQLite3)')
        add_button_xml = QPushButton('Sauvegarder en XML')
        delete_button_db = QPushButton('Supprimer de DB')
        delete_button_xml = QPushButton('Supprimer de XML')

        add_button_db.clicked.connect(self.add_product_to_db)
        add_button_xml.clicked.connect(self.save_to_xml)
        delete_button_db.clicked.connect(self.delete_selected_product_db)
        delete_button_xml.clicked.connect(self.delete_product_by_id_xml)

        layout.addWidget(add_button_db)
        layout.addWidget(add_button_xml)
        layout.addWidget(delete_button_db)
        layout.addWidget(delete_button_xml)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(['ID', 'Nom', 'Prix'])
        layout.addWidget(self.tree)

        self.conn = sqlite3.connect('gestion.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS produits (id INTEGER PRIMARY KEY, nom TEXT, prix REAL)")
        self.conn.commit()

        self.update_tree_from_db()

        self.setLayout(layout)

    def add_product_to_db(self):
        id = self.id_input.text()
        nom = self.nom_input.text()
        prix = self.prix_input.text()

        self.cursor.execute("INSERT INTO produits (id, nom, prix) VALUES (?, ?, ?)", (id, nom, prix))
        self.conn.commit()

        self.clear_input_fields()
        self.update_tree_from_db()

    def clear_input_fields(self):
        self.id_input.clear()
        self.nom_input.clear()
        self.prix_input.clear()

    def update_tree_from_db(self):
        self.tree.clear()
        self.cursor.execute("SELECT * FROM produits")
        data = self.cursor.fetchall()

        for row in data:
            item = QTreeWidgetItem(self.tree)
            item.setText(0, str(row[0]))
            item.setText(1, row[1])
            item.setText(2, str(row[2]))

    def save_to_xml(self):
        id = self.id_input.text()
        nom = self.nom_input.text()
        prix = self.prix_input.text()

        existing_ids = set()

        try:
            tree_xml = ET.parse('products.xml')
            products = tree_xml.getroot()
            for product in products.findall('product'):
                existing_id = product.find('ID').text
                existing_ids.add(existing_id)
        except FileNotFoundError:
            products = ET.Element('Products')

        if id not in existing_ids:
            product = ET.Element('product')
            id_element = ET.Element('ID')
            id_element.text = id
            nom_element = ET.Element('Nom')
            nom_element.text = nom
            prix_element = ET.Element('Prix')
            prix_element.text = prix

            product.append(id_element)
            product.append(nom_element)
            product.append(prix_element)

            products.append(product)

            tree_xml = ET.ElementTree(products)
            tree_xml.write('products.xml')
        else:
            print("ID déjà existant, veuillez utiliser un ID unique.")

    def delete_selected_product_db(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            id_to_delete = int(selected_item.text(0))
            self.cursor.execute("DELETE FROM produits WHERE id=?", (id_to_delete,))
            self.conn.commit()
            self.update_tree_from_db()

    def delete_product_by_id_xml(self):
        id_to_delete = self.id_input.text()

        try:
            tree_xml = ET.parse('products.xml')
            products = tree_xml.getroot()
            product_to_delete = None

            for product in products.findall('product'):
                existing_id = product.find('ID').text
                if existing_id == id_to_delete:
                    product_to_delete = product
                    break

            if product_to_delete:
                products.remove(product_to_delete)
                tree_xml.write('products.xml')
        except FileNotFoundError:
            pass

        self.clear_input_fields()

        self.update_tree_from_db()       

    def closeEvent(self, event):
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProductWidget()
    window.show()
    sys.exit(app.exec_())
