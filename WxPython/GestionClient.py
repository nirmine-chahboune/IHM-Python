import wx
import sqlite3

class GestionClient(wx.Frame):
    def __init__(self):
        super().__init__(None, title="client", size=(400, 300))
        
        panel = wx.Panel(self)

        self.id_input = wx.TextCtrl(panel)
        self.nom_input = wx.TextCtrl(panel)
        self.email_input = wx.TextCtrl(panel)

        btn_add = wx.Button(panel, label='Add')
        btn_delete = wx.Button(panel, label='Delete')
        btn_update = wx.Button(panel, label='Update')

        self.client_list = wx.ListBox(panel)

        btn_add.Bind(wx.EVT_BUTTON, self.add_client)
        btn_delete.Bind(wx.EVT_BUTTON, self.delete_client)
        btn_update.Bind(wx.EVT_BUTTON, self.update_client)
        self.client_list.Bind(wx.EVT_LISTBOX, self.select_client)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(panel, label='ID:'), 0, wx.ALL, 5)
        sizer.Add(self.id_input, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(wx.StaticText(panel, label='Nom:'), 0, wx.ALL, 5)
        sizer.Add(self.nom_input, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(wx.StaticText(panel, label='Email:'), 0, wx.ALL, 5)
        sizer.Add(self.email_input, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn_add, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn_delete, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn_update, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.client_list, 1, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(sizer)
        self.Center()
        self.Show()

        self.conn = sqlite3.connect('client.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS client (id INTEGER PRIMARY KEY, nom TEXT, email TEXT)")
        self.conn.commit()
        self.refresh_client_list()

    def add_client(self, event):
        id_value = self.id_input.GetValue()
        nom_value = self.nom_input.GetValue()
        email_value = self.email_input.GetValue()

        self.cursor.execute("INSERT INTO client (id, nom, email) VALUES (?, ?, ?)", (id_value, nom_value, email_value))
        self.conn.commit()
        self.refresh_client_list()

    def delete_client(self, event):
        selected_index = self.client_list.GetSelection()
        if selected_index != -1:
            client_id = self.client_list.GetString(selected_index).split(':')[0]
            self.cursor.execute("DELETE FROM client WHERE id=?", (client_id,))
            self.conn.commit()
            self.refresh_client_list()

    def update_client(self, event):
        selected_index = self.client_list.GetSelection()
        if selected_index != -1:
            client_id = self.client_list.GetString(selected_index).split(':')[0]
            nom_value = self.nom_input.GetValue()
            email_value = self.email_input.GetValue()
            self.cursor.execute("UPDATE client SET nom=?, email=? WHERE id=?", (nom_value, email_value, client_id))
            self.conn.commit()
            self.refresh_client_list()

    def select_client(self, event):
        selected_index = self.client_list.GetSelection()
        if selected_index != -1:
            client_id, nom, email = self.client_list.GetString(selected_index).split(':')
            self.id_input.SetValue(client_id)
            self.nom_input.SetValue(nom)
            self.email_input.SetValue(email)

    def refresh_client_list(self):
        self.client_list.Clear()
        self.cursor.execute("SELECT * FROM client")
        client = self.cursor.fetchall()
        for cl in client:
            self.client_list.Append(f"{cl[0]}: {cl[1]} - {cl[2]}")


if __name__ == '__main__':
    app = wx.App()
    GestionClient(None, title='Client CRUD')
    app.MainLoop()
