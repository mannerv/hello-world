# TIE-02101 Ohjelmointi 1: Johdanto
# Name:     CharityGifts

# Author:   Veera Manner
#           240130
#           veera.manner@student.tut.fi

# Description: Pick a charity from a pre-selection. You can save your choice
#              to a list, which will be shown in the user interface (for the
#              main user) as 'Santa' is written in the name inquiry.


from tkinter import *
import csv


class Selection:
    # User interface object

    def __init__(self):
        """
        Constuctor:

        has a window, a title, charities dictionary, giftlist saving the choice,
        widgets to make the choice
        """
        self.__window = Tk()
        self.__window.title("Who needs a gift?")

        self.__charities = read_file('charities.csv')
        self.__gifts = []

        self.__text_field1 = Label(self.__window, text= "You my friend "
        "are getting a gift this year. If you feel like someone else might "
        " need it more, use this selection of charities to redirect your gift "
                                                            "for a cause!")

        self.__text_field2 = Label(self.__window, text="First enter your "
                                                       "name:")

        self.__text_field3 = Label(self.__window, text="Please write your "
                                          "first name with letters only, thx!")

        self.__donor = Entry(self.__window)

        self.__sel1_button = []
        for i in sorted(self.__charities):
            new_button = Button(self.__window, text=i, command=lambda index=i:
                                self.finalize(index))
            self.__sel1_button.append(new_button)

        self.__continue_button = Button(self.__window, text="Continue", command=self.fix_name)

        self.__save_button = Button(self.__window, text="Save", command=self.make_donation)

        self.__stop_button = Button(self.__window, text="Quit",
                                    command=self.stop)

        self.set()

    def start(self):
        # Open user interface
        self.__window.mainloop()

    def set(self):
        # Set home view

        self.__text_field1.grid()
        self.__text_field2.grid()
        self.__donor.grid()
        self.__continue_button.grid()
        self.__stop_button.grid()

    def fix_name(self):
        # Check a proper name fed, will go to Santa's list when called

        donor = self.__donor.get()

        if donor.isalpha():

            donor = donor[0].upper() + donor[1:].lower()
            self.__gifts.append(donor)

            if donor == "Santa":
                self.gift_list()
            else:
                self.set_sel1()
        else:
            self.__text_field1["text"] = "Please write your first name with " \
                                         "letters only, thx!"

    def set_sel1(self):
        # Selection view

        self.__text_field1["text"] = "Choose a cause:"
        self.__text_field2["text"] = ""
        for i in range(len(self.__sel1_button)):
            self.__sel1_button[i].grid()
        self.__donor.destroy()
        self.__continue_button.destroy()

    def finalize(self,i):
        # Save the choice

        self.__save_button.grid()

        self.__text_field1["text"] = "Great choice! Now finalize your " \
                                     "donation by pressing 'Save'."
        self.__text_field2["text"] = "If you want to reconsider, press " \
                                     "'Quit' and start again."
        for x in self.__sel1_button:
            x.destroy()

        organization, target = self.__charities[i].split(sep="/")
        self.__gifts.append(target)
        self.__gifts.append(organization)

    def make_donation(self):
        # Confirmation to the given choice
        self.__save_button.destroy()
        donor = self.__gifts[0]
        self.__text_field1["text"] = f"Thank you {donor}!"
        target = self.__gifts[1]
        org = self.__gifts[2]

        self.__text_field2["text"] = "A donation is given under your name " \
                                     f"towards {target} through {org}."

        write_file(self.__gifts)

    def gift_list(self):
        # Show santa's list
        self.__donor.destroy()
        self.__continue_button.destroy()
        self.__text_field1["text"] = "The Giftlist"
        try:
            with open('giftlist.csv', 'r') as gifts:
                csv_reader = csv.reader(gifts, delimiter=';')
                list_g = []

                for line in csv_reader:
                    list_g.append(line[0]+": "+line[2])

            self.__text_field2["text"] = list_g
        except FileNotFoundError:
            self.__text_field2["text"] = "No wishes made yet!"

    def stop(self):
        # Exit ui
        self.__window.destroy()


def read_file(f):
    # reads charities file
    char = {}
    with open(f, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        next(csv_reader)
        for line in csv_reader:
            if line[0] not in char:
                char[line[0]] = line[1]

    return char


def write_file(donation):
    # make santa's list
    with open('giftlist.csv', 'a', newline='') as gifts:
        csv_writer = csv.writer(gifts, delimiter=';')

        csv_writer.writerow(donation)


def main():

    ui = Selection()
    ui.start()


main()

