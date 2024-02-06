import wx
from ProductFrame import ProductFrame
from GestionClient import GestionClient
from GestionCommande import Gestioncommande 
class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Main Window", size=(400, 300))
        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        button_1 = wx.Button(panel, label="Open Gestion Produit")
        button_1.Bind(wx.EVT_BUTTON, self.open_gestion_produit)
        sizer.Add(button_1, 0, wx.ALL | wx.EXPAND, 10)

        button_2 = wx.Button(panel, label="Open Gestion Commande")
        button_2.Bind(wx.EVT_BUTTON, self.open_gestion_commande)
        sizer.Add(button_2, 0, wx.ALL | wx.EXPAND, 10)

        button_3 = wx.Button(panel, label="Open Gestion Client")
        button_3.Bind(wx.EVT_BUTTON, self.open_window_3)
        sizer.Add(button_3, 0, wx.ALL | wx.EXPAND, 10)

        panel.SetSizer(sizer)
        self.Show()

    def open_gestion_produit(self, event):
        window = ProductFrame()
        window.Show()

    def open_gestion_commande(self, event):
        window =Gestioncommande()
        window.Show()

    def open_window_3(self, event):
        window = GestionClient()
        window.Show()

class SubWindow(wx.Frame):
    def __init__(self, title):
        super().__init__(None, title=title, size=(300, 200))
        self.Show()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow()
    app.MainLoop()
