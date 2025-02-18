import json
from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import os


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = string.ascii_letters
    numbers = string.digits
    symbols = string.punctuation

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, "end")
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Unacceptable Details", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            data = {}
        except json.decoder.JSONDecodeError:
            data = {}

        # dictionary to store emails and passwords in json format
        data.update({
            website: {
                "email": email,
                "password": password,
            }
        })
        with open("data.json", "w") as data_file:
            # Saving/Writing the data
            json.dump(data, data_file, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)


def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="No File Found", message="No Data File Found")
    except json.JSONDecodeError:
        messagebox.showinfo(title="No Data Found", message="data.json does not contain data")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No Details For {website} Found")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.geometry("500x600")
window.title("Password Manager")
window.config(padx=20, pady=20)

# Logo
canvas = Canvas(window, width=200, height=200)
logo_path = "D:/Python/Secure Tool Expo/password-manager/logo.jpg"
if os.path.exists(logo_path):
    main_image = PhotoImage(file=logo_path)
    canvas.create_image(100, 100, image=main_image)
else:
    messagebox.showerror(title="Error", message="logo.jpg file not found")
canvas.grid(column=1, row=0, pady=20)

# Website Frame
website_frame = Frame(window)
website_frame.grid(column=1, row=1, pady=5)

website_label = Label(website_frame, text="Website:")
website_label.grid(sticky="E", padx=5, pady=5)

website_entry = Entry(website_frame, width=35)
website_entry.grid(sticky="EW", padx=5, pady=5)
website_entry.focus()

# Email Frame
email_frame = Frame(window)
email_frame.grid(column=1, row=2, pady=5)

email_label = Label(email_frame, text="Email/Username:")
email_label.grid(sticky="E", padx=5, pady=5)

email_entry = Entry(email_frame, width=35)
email_entry.grid(sticky="EW", padx=5, pady=5)
email_entry.insert(0, "yourmail@gmail.com")

# Password Frame
passframe = Frame(window)
passframe.grid(column=1, row=3, pady=5)

password_label = Label(passframe, text="Password:")
password_label.grid(sticky="E", padx=5, pady=5)

password_entry = Entry(passframe, width=21, show="*")
password_entry.grid(sticky="EW", padx=5, pady=5)

# Buttons Frame

buttonframe = Frame(window)
buttonframe.grid(column=1, row=4, pady=5)

addbutton = Button(buttonframe, text="Add", width=36, command=save)
addbutton.grid(columnspan=2, sticky="EW", padx=5, pady=20)

gpbutton = Button(buttonframe, text="Generate Password", command=generate_password)
gpbutton.grid(columnspan=2,sticky="EW", padx=5, pady=5)

website_search_btn = Button(buttonframe, text="Search", command=find_password)
website_search_btn.grid(columnspan = 2,sticky="EW", padx=5, pady=5)


window.mainloop()