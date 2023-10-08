import customtkinter
from functions.proxy import Proxy


class App(customtkinter.CTk):

    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)

        titletext = "BRAVOSIX"

        self.title(titletext)
        self.geometry('300x250')
        self.resizable(False, False)
        self.proxy = Proxy()

        self.after(201, lambda : self.iconbitmap("icon.ico"))


        self.default_font = customtkinter.CTkFont(family="consolas")

        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        title = customtkinter.CTkLabel(master=self, text=titletext, font=customtkinter.CTkFont(size=20,
                                                                                               weight="bold",
                                                                                               family="consolas"))

        title.grid(row=0, column=0, columnspan=3, rowspan=2, sticky='we', pady=15)

        self.statusSwitch = customtkinter.CTkSwitch(master=self, text="GOINGDARK", command=lambda: self.selfVPN(),
                                                   font=self.default_font)
        
        if self.proxy.current_value:
            self.statusSwitch.select()

        self.statusSwitch.grid(row=2, column=0, columnspan=1, sticky='we', pady=15, padx=15)

        self.cityLabel = customtkinter.CTkLabel(master=self, text="CITY: ", font=self.default_font)
        self.cityLabel.grid(row=3, column=0, columnspan=3, sticky='we', padx=40, pady=3)

        self.countryLabel = customtkinter.CTkLabel(master=self, text="COUNTRY: ", font=self.default_font)
        self.countryLabel.grid(row=4, column=0, columnspan=3, sticky='we', padx=40, pady=3)

        self.ipAddressLabel = customtkinter.CTkLabel(master=self, text="IP: ", font=self.default_font)
        self.ipAddressLabel.grid(row=5, column=0, columnspan=3, sticky='we', padx=40, pady=3)

        self.updateIdentity(self.proxy.get_identity())

        self.changeIdentity = customtkinter.CTkButton(master=self, text="CHANGE", command=lambda: self.newIdentity(),
                                                      font=self.default_font)
        self.changeIdentity.grid(row=2, column=2, pady=15, padx=10)

    def selfVPN(self):
        """
        Flip the state of the VPN
        :return: 
        """
        newIdentity = self.proxy.change_proxy_state()
        self.updateIdentity(newIdentity)

    def newIdentity(self):
        """
        Generate another identity to use (another IP, Country and City)
        :return: 
        """

        self.proxy.new_location()
        newIdentity = self.proxy.get_identity()

        self.updateIdentity(newIdentity)

    def updateIdentity(self, newIdentity):
        """
        Update the labels giving information of the current identity
        :param newIdentity: 
        :return: 
        """
        self.ipAddressLabel.configure(text=f"IP: {newIdentity['query']}")
        self.cityLabel.configure(text=f"CITY: {newIdentity['city']}")
        self.countryLabel.configure(text=f"COUNTRY: {newIdentity['country']}")

    def on_close(self):
        self.iconify()  # Minimize a janela ao invés de fechá-la
        self.protocol('WM_DELETE_WINDOW', self.on_close)

    def run(self):
        """
        Runs the application
        :return: 
        """
        self.mainloop()
