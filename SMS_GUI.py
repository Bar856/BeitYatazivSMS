import tkinter as tk
from tkinter import *
from functions import *
from tkinter import font as tkFont
import tkinter.scrolledtext as scrolledtext


# GUI
class App:
    # create GUI
    def __init__(self, parent):
        self.parent = parent
        myfont = tkFont.Font(family='arial', size=15, weight="bold")

        self.label2 = tk.Label(self.parent, text="שליחת SMS", font=('david', 30, 'bold'), fg='green')
        self.label2.pack(padx=3, pady=3)
        # options menu departments
        self.options = departments
        self.om_variable = tk.StringVar(self.parent)
        self.om_variable.set("בחר מחלקה")
        self.om = tk.OptionMenu(self.parent, self.om_variable, *self.options, command=self.add_to_listbox)
        self.om.config(font=myfont)  # set the button font
        self.om.pack(padx=3, pady=3)

        self.label1 = tk.Label(self.parent, text="הודעה:", font=('david', 15, 'bold'))
        self.label1.pack(padx=3, pady=3)

        self.entry = tk.Entry(self.parent, font=('david', 15, 'bold'), insertborderwidth=2)
        self.entry.pack(padx=3, pady=3)

        self.radio_var = IntVar()
        self.check_btn1 = tk.Radiobutton(master=self.parent, text="שלח לעובד/עובדים נבחרים",
                                         variable=self.radio_var, value=1, font=myfont,
                                         command=self.clearFieldsForRadio1)
        self.check_btn1.pack(ipady=3)
        self.check_btn2 = tk.Radiobutton(master=self.parent, text="שלח לכל המחלקה",
                                         variable=self.radio_var, value=2, font=myfont,
                                         command=self.selectItemsForDepart)
        self.check_btn2.pack(ipady=3)
        self.check_btn3 = tk.Radiobutton(master=self.parent, text="שלח הודעה לכל העובדים",
                                         variable=self.radio_var, value=3, font=myfont, command=self.showAllContacts)
        self.check_btn3.pack(ipady=3)
        self.check_btn1.select()

        self.btn2 = tk.Button(self.parent, text="שלח SMS", command=self.send_msg_gui, state='normal', width=10,
                              height=2, fg='green', font=('david', 15, 'bold'))
        self.btn2.pack(padx=3, pady=3)

        self.btn_exit = Button(self.parent, text="Exit", command=quit, state='normal', width=6, height=1,
                               fg='red', font=('david', 20, 'bold'))
        self.btn_exit.pack(padx=3, pady=3)

        self.list_contacts = Listbox(self.parent, selectmode="multiple", width=1, height=8, font=myfont)
        self.list_contacts.pack(padx=3, pady=3, expand=NO, fill="both")

        self.txt = scrolledtext.ScrolledText(self.parent, font=('david', 15, 'bold'), highlightthickness=5, height=8)
        self.txt['font'] = myfont
        self.txt.configure(state="disable")
        self.txt.tag_configure('tag-right', justify='center')
        self.txt.pack(expand=True, fill='both')

        self.parent.title('SMS Beit Yatziv')
        self.parent.geometry("400x600")
        self.parent.resizable(True, True)
        self.parent.mainloop()

    # add to listbox by depart
    def add_to_listbox(self, depart):
        self.list_contacts.delete(0, END)
        x = get_contacts_by_depart(depart)
        counter = 1
        for each_item in range(len(x)):
            self.list_contacts.insert(END, "   {:>}                                {:>8}"
                                      .format(x[each_item], counter))
            self.list_contacts.itemconfig(each_item)
            counter += 1

    # get the selected contacts from textbox
    def get_selected_contacts(self):
        li = []
        for i in self.list_contacts.curselection():
            li.append(self.list_contacts.get(i))
        return li

    # clear ent after sending msg
    def clear_fields(self):
        self.entry.delete(0, END)
        self.list_contacts.delete(0, END)
        self.om_variable.set("בחר מחלקה")

    # clear and add contacts to listbox
    def clearFieldsForRadio1(self):
        self.list_contacts.delete(0, END)
        self.add_to_listbox(self.om_variable.get())

    # radio btn 3
    def showAllContacts(self):
        self.list_contacts.delete(0, END)
        counter = 1
        for i in departments:
            x = get_contacts_by_depart(i)
            for each_item in range(len(x)):
                self.list_contacts.insert(END, "   {:>}                                {:>8}".format(x[each_item],
                                                                                                     counter))
                self.list_contacts.itemconfig(each_item)
                counter += 1
        for i in range(0, self.list_contacts.size()):
            self.list_contacts.select_set(i)

    # radio btn 2
    def selectItemsForDepart(self):
        self.add_to_listbox(self.om_variable.get())
        for i in range(0, self.list_contacts.size()):
            self.list_contacts.select_set(i)

    # send sms gui helper function
    def send_sms_help1(self, to_names):
        data = self.entry.get()
        for i in to_names:
            i2 = removeSpaces(i)
            to_num = get_contact_num(i2)
            sms = send_sms(to_num, data, True)
            if sms is True:
                self.send_msg_to_tk("הודעה נשלחה אל:{0} תוכן ההודעה: {1}".format(get_cantact_name(to_num), data))
                self.clear_fields()
            elif sms == "ex1":
                self.send_msg_to_tk("הודעה לא נשלחה - שגיאת רשת")
            else:
                self.send_msg_to_tk("הודעה לא נשלחה - שגיאה")

    # send msg thru GUI app
    def send_msg_gui(self):
        try:
            if self.entry.get() == "":
                self.send_msg_to_tk("אנא רשום הודעה")
                return False
            rad_var = self.radio_var.get()
            if rad_var == 1:
                to_names = self.get_selected_contacts()
                if not to_names:
                    self.send_msg_to_tk("אנא בחר עובד/עובדים")
                    return False
                self.send_sms_help1(to_names)
            elif rad_var == 2:
                to_names = get_contacts_by_depart(self.om_variable.get())
                self.send_sms_help1(to_names)
            elif rad_var == 3:
                to_names = []
                for i in contacts:
                    to_names.append(i.name)
                self.send_sms_help1(to_names)
            self.txt.see(tk.END)
        except Exception as e:
            print(str(e))

    #  Send messages to txt_box in GUI
    def send_msg_to_tk(self, string):
        self.txt.configure(state="normal")
        self.txt.insert(END, str("\n" + string), 'tag-right')
        self.txt.configure(state="disabled")


# Run the design
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
