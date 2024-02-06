import wx
import sqlite3
import xml.etree.ElementTree as ET

class GestionProduit(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Gestion Produit", size=(800, 400))
        self.init_ui()
        self.conn = sqlite3.connect('gestion.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS produits (id INTEGER PRIMARY KEY, nom TEXT, prix REAL)")
        self.conn.commit()
        self.update_tree_from_db()

    def init_ui(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        id_label = wx.StaticText(panel, label='ID:')
        self.id_input = wx.TextCtrl(panel)
        nom_label = wx.StaticText(panel, label='Nom:')
        self.nom_input = wx.TextCtrl(panel)
        prix_label = wx.StaticText(panel, label='Prix:')
        self.prix_input = wx.TextCtrl(panel)

        sizer.Add(id_label, 0, wx.ALL, 5)
        sizer.Add(self.id_input, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(nom_label, 0, wx.ALL, 5)
        sizer.Add(self.nom_input, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(prix_label, 0, wx.ALL, 5)
        sizer.Add(self.prix_input, 0, wx.ALL | wx.EXPAND, 5)

        add_button_db = wx.Button(panel, label='Ajouter au DB (SQLite3)')
        add_button_xml = wx.Button(panel, label='Sauvegarder en XML')
        delete_button_db = wx.Button(panel, label='Supprimer de DB')
        delete_button_xml = wx.Button(panel, label='Supprimer de XML')

        add_button_db.Bind(wx.EVT_BUTTON, self.add_product_to_db)
        add_button_xml.Bind(wx.EVT_BUTTON, self.save_to_xml)
        delete_button_db.Bind(wx.EVT_BUTTON, self.delete_selected_product_db)
        delete_button_xml.Bind(wx.EVT_BUTTON, self.delete_product_by_id_xml)

        sizer.Add(add_button_db, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(add_button_xml, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(delete_button_db, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(delete_button_xml, 0, wx.ALL | wx.EXPAND, 5)

        self.tree = wx.TreeCtrl(panel)
        # Instead, set up the number of columns and their widths:
        self.tree.SetColumnCount(3)
        self.tree.SetColumnWidth(0, 100)  # Adjust width as needed
        self.tree.SetColumnWidth(1, 150)
        self.tree.SetColumnWidth(2, 100)


        sizer.Add(self.tree, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(sizer)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def add_product_to_db(self, event):
        id_value = self.id_input.GetValue()
        nom_value = self.nom_input.GetValue()
        prix_value = self.prix_input.GetValue()

        self.cursor.execute("INSERT INTO produits (id, nom, prix) VALUES (?, ?, ?)", (id_value, nom_value, prix_value))
        self.conn.commit()

        self.clear_input_fields()
        self.update_tree_from_db()

    def clear_input_fields(self):
        self.id_input.Clear()
        self.nom_input.Clear()
        self.prix_input.Clear()

    def update_tree_from_db(self):
        self.tree.DeleteAllItems()
        self.cursor.execute("SELECT * FROM produits")
        data = self.cursor.fetchall()

        root = self.tree.AddRoot('Products')

        for row in data:
            item = self.tree.AppendItem(root, text=str(row[0]))
            self.tree.SetItemText(item, str(row[1]), 1)
            self.tree.SetItemText(item, str(row[2]), 2)

    def save_to_xml(self, event):
        id_value = self.id_input.GetValue()
        nom_value = self.nom_input.GetValue()
        prix_value = self.prix_input.GetValue()

        existing_ids = set()

        try:
            tree_xml = ET.parse('products.xml')
            products = tree_xml.getroot()
            for product in products.findall('product'):
                existing_id = product.find('ID').text
                existing_ids.add(existing_id)
        except FileNotFoundError:
            products = ET.Element('Products')

        if id_value not in existing_ids:
            product = ET.Element('product')
            id_element = ET.Element('ID')
            id_element.text = id_value
            nom_element = ET.Element('Nom')
            nom_element.text = nom_value
            prix_element = ET.Element('Prix')
            prix_element.text = prix_value

            product.append(id_element)
            product.append(nom_element)
            product.append(prix_element)

            products.append(product)

            tree_xml = ET.ElementTree(products)
            tree_xml.write('products.xml')
        else:
            print("ID déjà existant, veuillez utiliser un ID unique.")

    def delete_selected_product_db(self, event):
        selected_item = self.tree.GetSelection()
        if selected_item:
            id_to_delete = int(self.tree.GetItemText(selected_item))
            self.cursor.execute("DELETE FROM produits WHERE id=?", (id_to_delete,))
            self.conn.commit()
            self.update_tree_from_db()

    def delete_product_by_id_xml(self, event):
        id_to_delete = self.id_input.GetValue()

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

    def on_close(self, event):
        self.conn.close()
        self.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    window = GestionProduit()
    window.Show(True)
    app.MainLoop()
