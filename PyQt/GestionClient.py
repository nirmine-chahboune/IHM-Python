import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QFont
import sqlite3
import xml.etree.ElementTree as ET

class ClientWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gestion Client")
        self.setGeometry(100, 100, 800, 400)

        # Create a QVBoxLayout to arrange the widgets vertically
        layout = QVBoxLayout()

        # Create labels and input fields for ID, Name, and Email
        id_label = QLabel('ID:')
        self.id_input = QLineEdit()
        nom_label = QLabel('Nom:')
        self.nom_input = QLineEdit()
        email_label = QLabel('Email:')
        self.email_input = QLineEdit()

        layout.addWidget(id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(nom_label)
        layout.addWidget(self.nom_input)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)

        # Create buttons for adding to DB, saving to XML, and deleting from DB and XML
        add_button_db = QPushButton('Ajouter au DB (SQLite3)')
        add_button_xml = QPushButton('Sauvegarder en XML')
        delete_button_db = QPushButton('Supprimer de DB')
        delete_button_xml = QPushButton('Supprimer de XML')

        add_button_db.clicked.connect(self.add_client_to_db)
        add_button_xml.clicked.connect(self.save_to_xml)
        delete_button_db.clicked.connect(self.delete_selected_client_db)
        delete_button_xml.clicked.connect(self.delete_client_by_id_xml)

        layout.addWidget(add_button_db)
        layout.addWidget(add_button_xml)
        layout.addWidget(delete_button_db)
        layout.addWidget(delete_button_xml)

        # Create and configure the QTreeWidget for displaying client data
        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(['ID', 'Nom', 'Email'])
        layout.addWidget(self.tree)

        # Establish a connection to the SQLite database
        self.conn = sqlite3.connect('gestion.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS client (id INTEGER PRIMARY KEY, nom TEXT, email TEXT)")
        self.conn.commit()

        self.update_tree_from_db()

        self.setLayout(layout)

    def add_client_to_db(self):
        id = self.id_input.text()
        nom = self.nom_input.text()
        email = self.email_input.text()

        self.cursor.execute("INSERT INTO client (id, nom, email) VALUES (?, ?, ?)", (id, nom, email))
        self.conn.commit()

        self.clear_input_fields()
        self.update_tree_from_db()

    def clear_input_fields(self):
        self.id_input.clear()
        self.nom_input.clear()
        self.email_input.clear()

    def update_tree_from_db(self):
        self.tree.clear()
        self.cursor.execute("SELECT * FROM client")
        data = self.cursor.fetchall()

        for row in data:
            item = QTreeWidgetItem(self.tree)
            item.setText(0, str(row[0]))
            item.setText(1, row[1])
            item.setText(2, row[2])

    def save_to_xml(self):
        id = self.id_input.text()
        nom = self.nom_input.text()
        email = self.email_input.text()

        existing_ids = set()

        try:
            tree_xml = ET.parse('clients.xml')
            clients = tree_xml.getroot()
            for client in clients.findall('client'):
                existing_id = client.find('ID').text
                existing_ids.add(existing_id)
        except FileNotFoundError:
            clients = ET.Element('clients')

        if id not in existing_ids:
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

            tree_xml = ET.ElementTree(clients)
            tree_xml.write('clients.xml')
        else:
            print("ID déjà existant, veuillez utiliser un ID unique.")

    def delete_selected_client_db(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            id_to_delete = int(selected_item.text(0))
            self.cursor.execute("DELETE FROM client WHERE id=?", (id_to_delete,))
            self.conn.commit()
            self.update_tree_from_db()

    def delete_client_by_id_xml(self):
        id_to_delete = self.id_input.text()

        try:
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
                tree_xml.write('clients.xml')
        except FileNotFoundError:
            pass

        self.clear_input_fields()

        self.update_tree_from_db()

    def closeEvent(self, event):
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientWidget()
    window.show()
    sys.exit(app.exec_())
