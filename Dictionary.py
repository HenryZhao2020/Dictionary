# Import all the libraries
from tkinter import *
from tkinter import ttk
from translate import Translator

dictionary_count = 0  # Store the number of dictionaries created
grid_thickness = 2
grid_height = 32  # The height of each row of the dictionary
grid_color = "gray"  # The color of the grids
animation_speed = 15  # The speed of slide-in/out animate effect


class Dictionary:
    """Create a Empty Dictionary"""

    def __init__(self):
        global dictionary_count, grid_color
        # Setup a window
        self.root = Tk()
        self.root.title("Henry's Dictionary")
        self.root.geometry("{}x{}+{}+{}".format(456, 600, int(self.root.winfo_screenwidth() / 2 - 228),
                                                int(self.root.winfo_screenheight() / 2 - 300)))
        self.root.minsize(456, 300)
        self.root.iconbitmap("Logo.ico")
        self.root["bd"] = 8  # The border width around the inner window

        self.max_hold = 0  # The maximum number of rows that the window can display
        self.row_count = 0  # The total number of rows of the dictionary
        self.topmost_row = 0  # The top row of the displayed page of the dictionary
        self.is_typing, self.is_first_time_typing = True, True
        self.words = []  # Store all the Entry boxes (not the str) in the "Word" column
        self.remove_row_buts = []  # Store all the "Remove Row" buttons
        self.word_rows = []  # Store all the rows of the "Word" column
        self.translations = []  # Store all the Entry boxes (not the str) in the "Translation" column.
        self.sort_row_buts = []  # Store all the "Sort Row" buttons
        self.translation_rows = []  # Store all the rows of the "Translation" column
        self.remove_row_but_icon = PhotoImage(file="RemoveBut.png")
        self.sort_row_but_icon = PhotoImage(file="SortBut.png")
        self.x = 0  # The horizontal position of the "Remove Row"/"Sort Row" buttons for animate effects
        self.y = 0  # The vertical position of the rows for animate effect
        self.width = 0  # The horizontal position of the "Word"/"Translation" entries for animate effects
        self.id = None
        self.to_be_removed_row = 0
        self.temp_removed_rows = []  # Store all the rows pending to be removed

        # Guide users to enter a word
        enter_word_pane = Frame(self.root, height=27)
        enter_word_pane.pack(side=TOP, fill=X, pady=2)
        enter_word_pane.pack_propagate(False)
        Label(enter_word_pane, text="Enter a word here:", font=("Segoe UI", 9), width=16, anchor=W, bd=0,
              highlightthickness=0).pack(side=LEFT, pady=1)
        self.entered_word = ttk.Entry(enter_word_pane)  # Contain the word that the users entered
        self.entered_word.bind("<Key>", lambda e: self.break_before_msg())
        self.entered_word.pack(side=LEFT, fill=BOTH, expand=True, pady=0.5)
        # Translate the word on click (optional)
        self.translate_but = ttk.Button(enter_word_pane, text="Get Translation", width=19,
                                        takefocus=0, command=lambda: self.translate())
        self.translate_but.pack(side=RIGHT, fill=BOTH, padx=(8, 0))

        # Guide users to enter the translation of the word
        self.enter_translation_pane = Frame(self.root, height=27)
        self.enter_translation_pane.pack(side=TOP, fill=X, pady=3)
        self.enter_translation_pane.pack_propagate(False)
        Label(self.enter_translation_pane, text="Enter its translation:", font=("Segoe UI", 9), width=16, anchor=W,
              bd=0, highlightthickness=0).pack(side=LEFT, pady=1)
        self.entered_translation = ttk.Entry(self.enter_translation_pane)  # Contain the translation of the word
        self.entered_translation.bind("<Key>", lambda e: self.break_before_msg())
        self.entered_translation.pack(side=LEFT, fill=BOTH, expand=True, pady=0.5)
        # Add the word and its meaning to the dictionary
        self.add_dict_but = ttk.Button(self.enter_translation_pane, text="Add to Dictionary", width=19,
                                       takefocus=0, command=lambda: self.add_to_dict())
        self.add_dict_but.pack(side=RIGHT, fill=BOTH, padx=(8, 0))

        # Display Error Message
        self.error_msg = Label(self.root, font=("Segoe UI", 9), fg="#D03E3A", bd=0, highlightthickness=0)

        # Display the dictionary in a grid with two columns
        self.dict = Frame(self.root)
        self.dict.pack(fill=BOTH, expand=True, pady=(30, 8))

        # The Word column
        self.word_col = Frame(self.dict)
        self.word_col.pack(side=LEFT, expand=True, fill=BOTH)
        self.word_col.pack_propagate(False)
        self.word_col_header = Entry(self.word_col, bd=2, relief=FLAT, bg=self.root["bg"], fg="gray",
                                     justify=CENTER, font=("Segoe UI", 18, "bold"), highlightthickness=1)
        self.word_col_header.pack(fill=X)
        Frame(self.word_col, height=2, bg=grid_color).pack(fill=X, padx=(1, 0))

        # A vertical line that separates the two columns
        separation_line = Frame(self.dict, width=2)
        Frame(separation_line, bg=self.root["bg"], width=2, height=9).pack(side=TOP)
        Frame(separation_line, bg="gray", width=2).pack(fill=BOTH, expand=True)
        separation_line.pack(side=LEFT, fill=Y)

        # The Translation column
        self.translation_col = Frame(self.dict)
        self.translation_col.pack(side=RIGHT, expand=True, fill=BOTH)
        self.translation_col.pack_propagate(False)
        self.translation_col_header = Entry(self.translation_col, bd=2, relief=FLAT, bg=self.root["bg"], justify=CENTER,
                                            font=("Segoe UI", 18, "bold"), fg="gray", highlightthickness=1)
        self.translation_col_header.pack(fill=X)
        Frame(self.translation_col, height=2, bg=grid_color).pack(fill=X, padx=(0, 1))

        # Special Characters Insertion Pane
        special_char_pane = Frame(self.root, width=self.root.winfo_width() - self.root["bd"] * 2, height=26)
        special_char_pane.pack(side=BOTTOM, fill=X, pady=(8, 0))
        special_char_pane.pack_propagate(False)
        Label(special_char_pane, text="Insert Special Characters:  ", font=("Segoe UI", 9)).pack(side=LEFT, fill=Y)
        ttk.Button(special_char_pane, text="á", width=3, takefocus=0,
                   command=lambda: self.insert_special_char("á")).pack(side=LEFT, fill=Y, padx=(5, 0))
        ttk.Button(special_char_pane, text="é", width=3, takefocus=0,
                   command=lambda: self.insert_special_char("é")).pack(side=LEFT, fill=Y, padx=(5, 0))
        ttk.Button(special_char_pane, text="í", width=3, takefocus=0,
                   command=lambda: self.insert_special_char("í")).pack(side=LEFT, fill=Y, padx=(5, 0))
        ttk.Button(special_char_pane, text="ñ", width=3, takefocus=0,
                   command=lambda: self.insert_special_char("ñ")).pack(side=LEFT, fill=Y, padx=(5, 0))
        ttk.Button(special_char_pane, text="ó", width=3, takefocus=0,
                   command=lambda: self.insert_special_char("ó")).pack(side=LEFT, fill=Y, padx=(5, 0))
        ttk.Button(special_char_pane, text="ú", width=3, takefocus=0,
                   command=lambda: self.insert_special_char("ú")).pack(side=LEFT, fill=Y, padx=(5, 0))
        ttk.Button(special_char_pane, text="ü", width=3, takefocus=0,
                   command=lambda: self.insert_special_char("ü")).pack(side=LEFT, fill=Y, padx=(5, 0))
        ttk.Button(special_char_pane, text="¿", width=3, takefocus=0,
                   command=lambda: self.insert_special_char("¿")).pack(side=LEFT, fill=Y, padx=(5, 0))
        ttk.Button(special_char_pane, text="¡", width=3, takefocus=0,
                   command=lambda: self.insert_special_char("¡")).pack(side=LEFT, fill=Y, padx=(5, 0))

        # Find a word from the dictionary
        find_pane = Frame(self.root, height=27)
        find_pane.pack(side=BOTTOM, fill=X)
        find_pane.pack_propagate(False)
        Label(find_pane, text="Find a word:  ", font=("Segoe UI", 9)).pack(side=LEFT, pady=1)
        self.find_word = ttk.Entry(find_pane)
        self.find_word.pack(side=LEFT, fill=BOTH, expand=True, pady=0.5)
        find_word_but = ttk.Button(find_pane, text="   Find Word   ", takefocus=0)
        find_word_but.pack(side=RIGHT, fill=BOTH, padx=(8, 0))
        Frame(self.root, bg="light gray", height=1).pack(side=BOTTOM, fill=X, pady=10)

        # A Frame for displaying info and options
        operation_pane = Frame(self.root, height=27)
        operation_pane.pack(side=BOTTOM, fill=X)
        operation_pane.pack_propagate(False)

        # Remove or rearrange the rows of the dictionaries on click
        self.edit_row_but = ttk.Button(operation_pane, text="Edit", takefocus=0, width=9,
                                       command=lambda: self.show_edit_buts())
        if self.row_count == 0:
            self.edit_row_but["state"] = DISABLED
        self.edit_row_but.pack(side=LEFT, fill=Y)

        # Recover the removed rows
        self.cancel_remove_but = ttk.Button(operation_pane, text="Cancel", takefocus=0, width=10,
                                            command=lambda: self.recover_removed_rows())

        # If the window cannot fit all the rows of the dictionary, click this to view more rows on the next page
        self.next_page = Button(operation_pane, text=">", bd=0, font=("Calibri", 18), relief=SUNKEN,
                                command=lambda: self.go_to_next_page())
        self.next_page.pack(side=RIGHT, fill=Y)

        # Click this to view the previous few rows on the previous page
        self.previous_page = Button(operation_pane, text="<", font=("Calibri", 18), bd=0, relief=SUNKEN,
                                    command=lambda: self.go_to_previous_page())
        self.previous_page.pack(side=RIGHT, fill=Y)

        dictionary_count += 1
        self.root.bind("<Configure>", lambda e: self.set_moving_pages_enabled())
        self.root.bind("<Key>", lambda e: self.set_buts_enabled())
        self.set_languages_dialog()
        self.root.mainloop()

    def set_languages_dialog(self):
        """Ask for users' preferences of languages before the program launches."""
        self.root.attributes("-disabled", True)
        dialog = Toplevel(self.root)
        dialog.transient(self.root)
        dialog.title("Set Your Preference of Languages")
        dialog.geometry("{}x{}+{}+{}".format(360, 144, int(dialog.winfo_screenwidth() / 2 - 180),
                                             int(dialog.winfo_screenheight() / 2 - 72)))
        dialog.resizable(False, False)
        dialog.iconbitmap("Logo.ico")
        dialog["bd"] = 8

        enter_setting_pane = Frame(dialog)
        enter_setting_pane.pack(side=TOP, fill=X)

        # Guide users to enter the language that they want to translate from
        from_pane = Frame(enter_setting_pane)
        from_pane.pack(side=TOP, fill=X, pady=2)
        Label(from_pane, text="Translate From:", font=("Segoe UI", 9), width=13, anchor=W).pack(side=LEFT, pady=2)
        lang_from = ttk.Combobox(from_pane, values=languages)
        lang_from.current(0)
        lang_from.pack(fill=BOTH, expand=True, padx=(0, 0.5))

        # Guide users to enter the language that they want to translate to
        to_pane = Frame(enter_setting_pane)
        to_pane.pack(fill=X, pady=3)
        Label(to_pane, text="To:", font=("Segoe UI", 9), width=13, anchor=W).pack(side=LEFT, pady=2)
        lang_to = ttk.Combobox(to_pane, values=languages)
        lang_to.current(0)
        lang_to.pack(fill=BOTH, expand=True, padx=(0, 0.5))

        Label(dialog, text="You could change them later by editing the column headers.", font=("Segoe UI", 9),
              fg="gray").pack(anchor=W, pady=8)

        save_but = ttk.Button(dialog, text="  Save your Preferences  ", takefocus=0, command=lambda: set_languages())
        save_but.pack(side=BOTTOM, anchor=E)

        def set_languages():
            if lang_from.get() != "<Configure Later>":
                self.word_col_header.insert(END, lang_from.get())
            if lang_to.get() != "<Configure Later>":
                self.translation_col_header.insert(END, lang_to.get())
            close_dialog()

        def close_dialog():
            self.root.attributes("-disabled", False)
            self.root.deiconify()
            dialog.destroy()
            self.entered_word.focus_set()
            self.root.update()
            self.error_msg.place(x=self.entered_translation.winfo_x(), y=self.enter_translation_pane.winfo_y() + 19)

        dialog.focus_force()
        dialog.protocol("WM_DELETE_WINDOW", lambda: close_dialog())
        dialog.bind("<Escape>", lambda e: close_dialog())
        dialog.mainloop()

    def break_before_msg(self):
        self.is_typing = True

    def insert_special_char(self, char):
        if isinstance(self.root.focus_get(), Entry):
            self.root.focus_get().insert(self.root.focus_get().index(INSERT), char)

    def translate(self):
        """Translate a word from one language to the other.
        Change the original and translation languages by editing the column headers."""
        translator = Translator(from_lang=self.word_col_header.get(), to_lang=self.translation_col_header.get())
        translation = translator.translate(self.entered_word.get())
        # Append the translated word to the translation Entry box
        self.entered_translation.delete(0, END)
        self.entered_translation.insert(0, translation)
        self.translate_but["state"] = DISABLED
        self.set_buts_enabled()

    def set_buts_enabled(self):
        """Set "Translate" and "Add to Dictionary" Button Enabled/Disabled."""
        if self.entered_word.get() == "":
            self.translate_but["state"] = DISABLED  # Cannot translate it if the word is empty
        else:
            self.translate_but["state"] = NORMAL

        word_col = self.word_col_header.get()
        self.word_col_header.delete(0, END)
        self.word_col_header.insert(END, word_col.upper())

        translation_col = self.translation_col_header.get()
        self.translation_col_header.delete(0, END)
        self.translation_col_header.insert(END, translation_col.upper())

        # Must have a word and its translation that are not empty before we add them to the dictionary
        if self.entered_word.get() != "" and self.entered_translation.get() != "":
            row = self.get_contained_row()
            self.is_first_time_typing = False
            # If the dictionary is not empty and contains the word but not its other translation,
            if self.row_count > 0 and row != -1 and not self.check_meaning_contained():
                self.add_dict_but["state"] = NORMAL  # Allow users to add the word and its other translation
                # Create an "Enter" keyboard shortcut to add the word and its translations to the dictionary
                self.entered_word.bind("<Return>", lambda e: self.add_to_dict())
                self.entered_translation.bind("<Return>", lambda e: self.add_to_dict())
                self.error_msg["text"] = ""
            else:
                if self.row_count == 0 or row == -1:  # If the dictionary is empty or does not contain the word,
                    self.add_dict_but["state"] = NORMAL  # Can add the word and its other translation
                    self.entered_word.bind("<Return>", lambda e: self.add_to_dict())
                    self.entered_translation.bind("<Return>", lambda e: self.add_to_dict())
                    self.error_msg["text"] = ""
                else:
                    self.add_dict_but["state"] = DISABLED  # Cannot otherwise
                    self.entered_word.unbind("<Return>")
                    self.entered_translation.unbind("<Return>")
                    if self.is_typing:
                        self.error_msg["text"] = "*This word and its translation are already in the dictionary"
        else:
            self.add_dict_but["state"] = DISABLED  # Cannot add them to the dictionary otherwise
            # Remove the "Enter" keyboard shortcut if the "Add to Dictionary" button is disabled
            self.entered_word.unbind("<Return>")
            self.entered_translation.unbind("<Return>")
            if not self.is_first_time_typing:  # No need to show these messages when the program first opens
                # Show these error messages when the word and/or translation are empty
                if self.entered_word.get() == "" and self.entered_translation.get() == "":
                    self.error_msg["text"] = "*Enter a word and its translation"
                elif self.entered_word.get() == "":
                    self.error_msg["text"] = "*Enter a word"
                elif self.entered_translation.get() == "":
                    self.error_msg["text"] = "*Enter the translation of the word you entered"

    def show_edit_buts(self):
        """Show the "Remove Row"/"Sort Row" buttons with animate effects."""
        self.root.after(animation_speed, self.slide_in)
        for i in range(self.row_count):
            self.sort_row_buts[i].pack(side=RIGHT, fill=BOTH, padx=(6, 1), pady=(0, 1.5))

        self.edit_row_but.config(text="Done", command=lambda: self.remove_rows())

    def hide_edit_buts(self):
        """Hide the "Remove Row"/"Sort Row" buttons with animate effects."""
        self.root.after(animation_speed, self.slide_out)
        for i in range(self.row_count):
            self.sort_row_buts[i].pack_forget()

        self.edit_row_but.config(text="Edit", command=lambda: self.show_edit_buts())

    def slide_in(self):
        """Slide-in effects when editing the dictionary."""
        if self.x < 33:
            self.x += 1  # Stop moving once the entries have moved 33 units horizontally
            # Store the ID of this events for cancellation when calling the method slide_out()
            self.root.after(animation_speed, self.slide_in)
        if self.width < 21:
            self.width += 1  # Stop moving once the buttons have moved 21 units horizontally
            self.root.after(animation_speed, self.slide_in)

        for i in range(self.row_count):
            # Change the position of components on screen
            self.remove_row_buts[i].place(x=0, y=0, width=self.width, height=grid_height - grid_thickness)
            self.words[i].pack(padx=(self.x, 0))

    def slide_out(self):
        """Slide-out effects when editing the dictionary."""
        if self.x > 0:
            self.x -= 1  # Stop moving once the buttons have gone back to their original positions
            self.root.after(animation_speed, self.slide_out)
        if self.width > 0:
            self.width -= 1  # Stop moving once the entries have gone back to their original positions
            self.root.after(animation_speed, self.slide_out)

        for i in range(self.row_count):
            # Change the position of components on screen
            self.remove_row_buts[i].place(x=0, y=0, width=self.width, height=grid_height - grid_thickness)
            self.words[i].pack(padx=(self.x, 0))

    def push_in(self):
        """Slide-in effects when editing the dictionary."""
        if self.y < grid_height - 2:
            self.y += 2  # Stop getting smashed once the entries has been completely hidden
            self.id = self.root.after(animation_speed, self.push_in)
        else:
            self.root.after_cancel(self.id)
            self.y = 0
            return

        self.word_rows[self.to_be_removed_row]["height"] = grid_height - self.y
        self.translation_rows[self.to_be_removed_row]["height"] = grid_height - self.y

    def push_out(self):
        """Slide-in effects when editing the dictionary."""
        if self.y < grid_height - 2:
            self.y += 2  # Stop getting smashed once the entries has been completely hidden
            self.id = self.root.after(animation_speed, self.push_out)
        else:
            self.root.after_cancel(self.id)
            self.y = 0
            return

        for i in range(self.row_count):
            if self.word_rows[i]["height"] != grid_height:
                self.word_rows[i]["height"] = self.y + 2
                self.translation_rows[i]["height"] = self.y + 2

    def temp_store_removed_rows(self, but):
        """Temporarily store the rows pending to be removed.
        The rows are hidden but still stored in the lists."""
        self.cancel_remove_but.pack(side=LEFT, padx=(6, 0), fill=Y)
        self.to_be_removed_row = self.remove_row_buts.index(but)
        # Store the removed rows in a list for recovery if needed
        self.temp_removed_rows.append([but, self.word_rows[self.to_be_removed_row], self.words[self.to_be_removed_row],
                                       self.translations[self.to_be_removed_row],
                                       self.translation_rows[self.to_be_removed_row],
                                       self.sort_row_buts[self.to_be_removed_row]])

        self.id = self.root.after(animation_speed, self.push_in)

    def recover_removed_rows(self):
        """Recover all the removed rows when pressed the "Cancel" button."""
        self.hide_edit_buts()
        self.root.after(animation_speed, self.push_out)
        self.cancel_remove_but.pack_forget()
        self.temp_removed_rows.clear()
        self.x, self.width = 0, 0

    def remove_rows(self):
        """Remove all the rows pending to be removed.
        Cannot be recovered later."""
        self.cancel_remove_but.pack_forget()
        self.hide_edit_buts()

        for i in range(len(self.temp_removed_rows)):
            index = self.temp_removed_rows[i]
            self.remove_row_buts.remove(index[0])
            self.word_rows.remove(index[1])
            index[1].pack_forget()
            self.words.remove(index[2])
            self.translations.remove(index[3])
            self.translation_rows.remove(index[4])
            index[4].pack_forget()
            self.sort_row_buts.remove(index[5])
            self.row_count -= 1

        self.temp_removed_rows.clear()
        if self.row_count == 0:
            self.edit_row_but["state"] = DISABLED

    def add_to_dict(self):
        """Add a word and its translation to the dictionary."""
        row = self.get_contained_row()  # Whether the entered word is already in the dictionary
        # Tne translation of the entered word
        translation = self.entered_translation.get()[0].upper() + self.entered_translation.get()[1:].lower()

        if row != -1:  # If it is in the dictionary
            self.translations[row].insert(END, "; " + translation)  # Add the translation on the same row that it is on
        else:
            # Otherwise, create a new row. Word in the first column, translation on the second column.
            word_col_pane = Frame(self.word_col, height=grid_height)
            self.word_rows.append(word_col_pane)
            word_col_pane.pack(fill=X)
            word_col_pane.pack_propagate(False)
            word_control_pane = Frame(word_col_pane)
            word_control_pane.pack(fill=BOTH, expand=True)
            remove_row_but = Button(word_control_pane, image=self.remove_row_but_icon, bd=0, relief=SUNKEN, anchor=E)
            remove_row_but["command"] = lambda: self.temp_store_removed_rows(remove_row_but)
            self.remove_row_buts.append(remove_row_but)
            remove_row_but.place(x=0, y=0, width=0, height=grid_height - grid_thickness)
            word_col = Entry(word_control_pane, font=("Segoe UI", 13), justify=CENTER, relief=FLAT,
                             highlightthickness=1, highlightcolor="gray")
            word_col.insert(END, self.entered_word.get()[0].upper() + self.entered_word.get()[1:].lower())
            word_col.pack(fill=BOTH, expand=True)
            self.words.append(word_col)
            Frame(word_col_pane, height=grid_thickness, bg=grid_color).pack(fill=X, padx=(1, 0), side=BOTTOM)

            translation_col_pane = Frame(self.translation_col, height=grid_height)
            self.translation_rows.append(translation_col_pane)
            translation_col_pane.pack(fill=X)
            translation_col_pane.pack_propagate(False)
            translation_control_pane = Frame(translation_col_pane)
            translation_control_pane.pack(fill=BOTH, expand=True)
            sort_row_but = Button(translation_control_pane, image=self.sort_row_but_icon, bd=0, relief=SUNKEN)
            self.sort_row_buts.append(sort_row_but)

            translation_col = Entry(translation_control_pane, font=("Segoe UI", 13), justify=CENTER,
                                    relief=FLAT, highlightthickness=1, highlightcolor="gray")
            translation_col.insert(END, translation)
            translation_col.pack(side=LEFT, fill=BOTH, expand=True)
            Frame(translation_col_pane, height=grid_thickness, bg=grid_color).pack(fill=X, padx=(0, 1), side=BOTTOM)
            self.translations.append(translation_col)

            self.slide_out()
            self.row_count += 1

        self.is_typing = False
        self.edit_row_but["state"] = NORMAL
        self.set_buts_enabled()

    def get_contained_row(self):
        """Return the row that contains the entered word.
        Return -1 if the dictionary does not contain it."""
        for i in range(self.row_count):
            if self.words[i].get().lower() == self.entered_word.get().lower():
                return i
        return -1

    def check_meaning_contained(self):
        """Return True if the dictionary already contains the word and its translation.
        Return False otherwise."""
        for i in range(self.row_count):
            if self.words[i].get().lower() == self.entered_word.get().lower():
                if self.translations[i].get().__contains__(";"):
                    for word in self.translations[i].get().split("; "):
                        if word.lower() == self.entered_translation.get().lower():
                            return True
                else:
                    if self.translations[i].get().lower() == self.entered_translation.get().lower():
                        return True
        return False

    def set_moving_pages_enabled(self):
        self.max_hold = int((self.dict.winfo_height() - self.word_col_header.winfo_height()) / grid_height)
        if self.topmost_row + self.max_hold >= self.row_count:  # If the window CAN fit all the rows of the dictionary,
            self.next_page["state"] = DISABLED  # "Next" button will be disabled
        else:  # Or if the window CANNOT fit all the rows of the dictionary
            self.next_page["state"] = NORMAL  # "Next" button will be enabled

        if self.topmost_row <= 0:  # If we are already on the first page
            self.previous_page["state"] = DISABLED  # "Previous" button will be disabled
        else:
            self.previous_page["state"] = NORMAL  # "Previous" button will be enabled otherwise

        self.set_buts_enabled()

    def go_to_previous_page(self):
        # When the window is resized, the maximize rows (max_hold) that it can display changes.
        # The topmost row decreases if max_hold increases and increases if max_hold decreases
        self.topmost_row -= self.max_hold

        if self.topmost_row >= 0:  # If the topmost is >= 0, then the window still cannot fit the entire dictionary
            for j in range(self.row_count):
                # Only the part of the rows that can be fit in the window is visible.
                if self.topmost_row <= j < self.topmost_row + self.max_hold:
                    self.word_rows[j].pack(fill=X)
                    self.translation_rows[j].pack(fill=X)
                else:
                    self.word_rows[j].pack_forget()
                    self.translation_rows[j].pack_forget()

            for j in range(self.row_count):
                # The other parts can also be seen if the height of the window increases
                if j >= self.topmost_row + self.max_hold:
                    self.word_rows[j].pack(fill=X)
                    self.translation_rows[j].pack(fill=X)

            self.set_moving_pages_enabled()
        else:  # Otherwise, the window can fit the entire dictionary
            for j in range(self.row_count):
                self.word_rows[j].pack_forget()
                self.translation_rows[j].pack_forget()

            for j in range(self.row_count):
                self.word_rows[j].pack(fill=X)
                self.translation_rows[j].pack(fill=X)

            self.topmost_row = 0

    def go_to_next_page(self):
        self.topmost_row += self.max_hold

        if self.topmost_row <= self.row_count:
            for j in range(self.row_count):
                # All the rows before the bottommost row of the previous page of the dictionary (inclusive) are hidden
                if j < self.topmost_row:
                    self.word_rows[j].pack_forget()
                    self.translation_rows[j].pack_forget()
                # The rest (if not empty) are shown
                else:
                    self.word_rows[j].pack(fill=X)
                    self.translation_rows[j].pack(fill=X)

            self.set_moving_pages_enabled()


# All the available languages
languages = ['<Configure Later>', 'Arabic', 'Armenian', 'Assamese', 'Aymara', 'Azeri', 'Bashkir', 'Basque',
             'Belarusian', 'Bengali', 'Bhutani', 'Bihari', 'Bislama', 'Breton', 'Bulgarian', 'Burmese', 'Cambodian',
             'Catalan', 'Chinese', 'Chinese (China)', 'Chinese (Singapore)',
             'Chinese (Taiwan)', 'Corsican', 'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'Dutch (Belgium)',
             'English', 'English', 'English (Australia)', 'English (Belize)', 'English (Canada)', 'English (Ireland)',
             'English (Jamaica)', 'English (New Zealand)', 'English (Philippines)', 'English (South Africa)',
             'English (Trinidad)', 'English (United Kingdom)', 'English (United States)', 'English (Zimbabwe)',
             'Esperanto', 'Estonian', 'FYRO Macedonian', 'Faeroese', 'Farsi', 'Fiji', 'Finnish', 'French',
             'French (Belgium)', 'French (Canada)', 'French (Luxembourg)', 'French (Monaco)', 'French (Switzerland)',
             'Frisian', 'Gaelic', 'Galician', 'Georgian', 'German', 'German (Austria)', 'German (Liechtenstein)',
             'German (Luxembourg)', 'German (Switzerland)', 'Greek', 'Greenlandic', 'Guarani', 'Gujarati', 'Hausa',
             'Hebrew', 'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Indonesian', 'Indonesian', 'Interlingua',
             'Interlingue', 'Inupiak', 'Irish', 'Italian', 'Italian (Switzerland)', 'Japanese', 'Javanese', 'Kannada',
             'Kashmiri', 'Kazakh', 'Kinyarwanda', 'Kirghiz', 'Kirundi', 'Konkani', 'Korean', 'Kurdish', 'Kyrgyz',
             'Laothian', 'Latin', 'Latvian', 'Lingala', 'Lithuanian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese',
             'Maori', 'Marathi', 'Moldavian', 'Mongolian', 'Nauru', 'Nepali (India)', 'Norwegian', 'Norwegian (Bokmal)',
             'Norwegian (Bokmal)', 'Occitan', 'Oriya', 'Pashto/Pushto', 'Polish', 'Portuguese', 'Portuguese (Brazil)',
             'Punjabi', 'Quechua', 'Rhaeto-Romanic', 'Romanian', 'Romanian (Moldova)', 'Russian', 'Russian (Moldova)',
             'Samoan', 'Sangro', 'Sanskrit', 'Serbian', 'Serbo-Croatian', 'Sesotho', 'Shona', 'Sindhi', 'Singhalese',
             'Siswati', 'Slovak', 'Slovenian', 'Slovenian', 'Somali', 'Sorbian', 'Spanish', 'Spanish (Argentina)',
             'Spanish (Bolivia)', 'Spanish (Chile)', 'Spanish (Colombia)', 'Spanish (Costa Rica)',
             'Spanish (Dominican Republic)', 'Spanish (Ecuador)', 'Spanish (El Salvador)', 'Spanish (España)',
             'Spanish (Guatemala)', 'Spanish (Honduras)', 'Spanish (Mexico)', 'Spanish (Nicaragua)', 'Spanish (Panama)',
             'Spanish (Paraguay)', 'Spanish (Peru)', 'Spanish (Puerto Rico)', 'Spanish (United States)',
             'Spanish (Uruguay)', 'Spanish (Venezuela)', 'Sundanese', 'Sutu', 'Swahili', 'Swedish', 'Swedish (Finland)',
             'Syriac', 'Tagalog', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tibetan', 'Tigrinya', 'Tonga', 'Tsonga',
             'Tswana', 'Turkish', 'Turkmen', 'Twi', 'Ukrainian', 'Urdu', 'Uzbek', 'Vietnamese', 'Volapuk', 'Welsh',
             'Wolof', 'Xhosa', 'Yiddish', 'Yiddish', 'Yoruba', 'Zulu']

Dictionary()  # Create a dictionary
