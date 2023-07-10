from tkinter import *
from tkinter import messagebox
from random import shuffle, randint, choice
import pyperclip
import json


# ---------------------------- DEFAULT BUTTON ------------------------------- #
def show_all():
    try:
        with open("data.json") as data_file:
            json_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error!", message="No data found.")
    else:
        data = ""
        for web in json_data:
            data += f"Website :              {web}\nEmail/Username : {json_data[web]['email']}\nPassword :            {json_data[web]['password']}\n\n"
        messagebox.showinfo(title="Login credentials", message=data)


# ---------------------------- DEFAULT BUTTON ------------------------------- #
def default_email():
    email_entry.delete(0, END)
    email_entry.insert(0, "shrivardhanc1234@gmail.com")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    is_ok = messagebox.askokcancel(title="Generated Password", message=f"Do you want to copy {password}\n"
                                                                       f" to your clipboard?")
    if is_ok:
        pyperclip.copy(password)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_pass():
    website = website_entry.get().lower()
    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
            email = data[website]["email"]
            password = data[website]["password"]
            website_entry.delete(0, END)
    except KeyError:
        messagebox.showinfo(title="Error!", message=f"NO details for {website} found.")
    except FileNotFoundError:
        messagebox.showinfo(title="Error!", message="File Not Found.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"Email: {email}\nPassword: {password}\n\n"
                                                              f"Do you want to copy the password?")
        if is_ok:
            pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().lower()
    email = email_entry.get().lower()
    password = password_entry.get()
    new_data = {website: {
        "email": email,
        "password": password,
    }}
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="You have left some fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n"
                                                              f"Email/Username: {email}\n"
                                                              f"Password: {password}\n")
        if is_ok:
            try:
                with open("data.json", 'r') as data_file:
                    data = json.load(data_file)
                    data.update(new_data)
            except FileNotFoundError:
                with open("data.json", 'w') as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                with open("data.json", 'w') as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

# Canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Label
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=36)
website_entry.focus()
website_entry.grid(row=1, column=1)

email_entry = Entry(width=36)
email_entry.grid(row=2, column=1)

password_entry = Entry(width=36)
password_entry.grid(row=3, column=1)

# Buttons
pass_gen_button = Button(text="Generate Password", width=15, command=generate_pass)
pass_gen_button.grid(row=3, column=2)

add_button = Button(text="Add", width=47, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=15, command=find_pass)
search_button.grid(row=1, column=2)

default_button = Button(text="Default", width=15, command=default_email)
default_button.grid(row=2, column=2)

show_all_button = Button(text="Show all", width=47, command=show_all)
show_all_button.grid(row=5, column=1, columnspan=2)

window.mainloop()
