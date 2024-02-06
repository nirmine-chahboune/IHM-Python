import wx
import sqlite3

class ProductFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="produit", size=(400, 300))
        
        panel = wx.Panel(self)

        self.id_input = wx.TextCtrl(panel)
        self.nom_input = wx.TextCtrl(panel)
        self.prix_input = wx.TextCtrl(panel)

        btn_add = wx.Button(panel, label='Add')
        btn_delete = wx.Button(panel, label='Delete')
        btn_update = wx.Button(panel, label='Update')

        self.product_list = wx.ListBox(panel)

        btn_add.Bind(wx.EVT_BUTTON, self.add_product)
        btn_delete.Bind(wx.EVT_BUTTON, self.delete_product)
        btn_update.Bind(wx.EVT_BUTTON, self.update_product)
        self.product_list.Bind(wx.EVT_LISTBOX, self.select_product)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label='ID:'), 0, wx.ALL, 5)
        sizer.Add(self.id_input, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(wx.StaticText(panel, label='Nom:'), 0, wx.ALL, 5)
        sizer.Add(self.nom_input, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(wx.StaticText(panel, label='Prix:'), 0, wx.ALL, 5)
        sizer.Add(self.prix_input, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn_add, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn_delete, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn_update, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.product_list, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(sizer)
        self.Center()
        self.Show()

        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS produits (id INTEGER PRIMARY KEY, nom TEXT, prix REAL)")
        self.conn.commit()
        self.refresh_product_list()

    def add_product(self, event):
        id_value = self.id_input.GetValue()
        nom_value = self.nom_input.GetValue()
        prix_value = self.prix_input.GetValue()

        self.cursor.execute("INSERT INTO produits (id, nom, prix) VALUES (?, ?, ?)", (id_value, nom_value, prix_value))
        self.conn.commit()
        self.refresh_product_list()

    def delete_product(self, event):
        selected_index = self.product_list.GetSelection()
        if selected_index != -1:
            product_id = self.product_list.GetString(selected_index).split(':')[0]
            self.cursor.execute("DELETE FROM produits WHERE id=?", (product_id,))
            self.conn.commit()
            self.refresh_product_list()

    def update_product(self, event):
        selected_index = self.product_list.GetSelection()
        if selected_index != -1:
            product_id = self.product_list.GetString(selected_index).split(':')[0]
            nom_value = self.nom_input.GetValue()
            prix_value = self.prix_input.GetValue()
            self.cursor.execute("UPDATE produits SET nom=?, prix=? WHERE id=?", (nom_value, prix_value, product_id))
            self.conn.commit()
            self.refresh_product_list()

    def select_product(self, event):
        selected_index = self.product_list.GetSelection()
        if selected_index != -1:
            product_id, nom, prix = self.product_list.GetString(selected_index).split(':')
            self.id_input.SetValue(product_id)
            self.nom_input.SetValue(nom)
            self.prix_input.SetValue(prix)

    def refresh_product_list(self):
        self.product_list.Clear()
        self.cursor.execute("SELECT * FROM produits")
        products = self.cursor.fetchall()
        for product in products:
            self.product_list.Append(f"{product[0]}: {product[1]} - {product[2]}")


if __name__ == '__main__':
    app = wx.App()
    ProductFrame(None, title='Product CRUD')
    app.MainLoop()
