import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
conn = mysql.connector.connect(host='localhost', user='root', password='Mydhili@27', database='registration')
my_cursor = conn.cursor()

def Login():
    global root
    username = entry_username.get().lower()
    password = entry_password.get()
    try:
        sql = "SELECT * FROM registereddata WHERE Username = %s  AND Password = %s"
        val = (username,password)
        my_cursor.execute(sql, val)
        user = my_cursor.fetchone()

        if user and user[4]==password and user[2]==username:
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            open_homepage()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Login Failed", "An error occurred while logging in. Please try again.")

def open_idea_dialog():
    idea_window = tk.Toplevel(root)
    idea_window.title("Share an Idea")

    bg_frame = tk.Frame(idea_window, bg="light blue")
    bg_frame.place(relwidth=1, relheight=1)


    title_label = tk.Label(idea_window, text="Share Your Idea", font=("Arial", 25))
    title_label.place(relx=0.5,rely=0.15,anchor="center")

    entry_idea = tk.Entry(bg_frame, font=("Arial", 14), width=30,bd=3, relief="sunken", insertborderwidth=3, insertwidth=4, highlightthickness=2, highlightcolor="black", highlightbackground="lightblue")  # Adding borders
    entry_idea.place(relx=0.5,rely=0.4,anchor="center")

    category_combobox = ttk.Combobox(bg_frame, values=["softwareideas", "hardwareideas"], font=("Arial", 15))
    category_combobox.place(relx=0.5,rely=0.27,anchor="center")
    category_combobox.set("Select Category") 


    def submit_idea():
        idea = entry_idea.get().strip()
        category = category_combobox.get()
        if idea and category in ["softwareideas", "hardwareideas"]:
            try:
                table_name = category.lower().replace(" ", "")
                sql1 = f"INSERT INTO {table_name} (Idea) VALUES (%s)"
                val1=(idea,)
                my_cursor.execute(sql1, val1)
                conn.commit()
                reply_text.config(state=tk.NORMAL) 
                reply_text.insert(tk.END, "User's Idea: " + idea + "\n")
                reply_text.insert(tk.END, "Thank you for submitting\n") 
                reply_text.config(state=tk.DISABLED)
            except mysql.connector.Error as e:  # Catching mysql.connector.Error
                print("Error:", e)
                messagebox.showerror("Submitting idea failed", "An error occurred while submitting the idea.")
        elif not idea:
            messagebox.showwarning("Empty Idea", "Please enter your idea before submitting.")
        else:
            messagebox.showwarning("Empty Idea", "Please enter your idea before submitting.")

    
    submit_button = tk.Button(idea_window, text="Submit Idea", command=submit_idea, font=("Arial", 14), bg="yellow", fg="black")
    submit_button.place(relx=0.5,rely=0.48,anchor="center")


    reply_text = tk.Text(idea_window, height=6, width=40)
    reply_text.place(relx=0.5,rely=0.6,anchor="center")

    
    reply_text.config(state=tk.DISABLED) 
def retrieve_ideas_from_mysql():
    idea_window = tk.Toplevel(root)
    idea_window.title("View Ideas")

    window_width = 800
    window_height = 600
    screen_width = idea_window.winfo_screenwidth()
    screen_height = idea_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    idea_window.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))

    bg_frame = tk.Frame(idea_window, bg="violet")
    bg_frame.pack(fill=tk.BOTH, expand=True)

    dropdown_var = tk.StringVar()
    dropdown = ttk.Combobox(bg_frame, textvariable=dropdown_var, values=["softwareideas", "hardwareideas"],font=("Arial", 20))
    dropdown.pack(pady=(20, 10))
    dropdown.set("Select an option") 

    

    text_widget = tk.Text(bg_frame, height=25, width=100)
    text_widget.pack(padx=20, pady=20)

    def fetch_ideas():
        category = dropdown_var.get()
        try:
            query = f"SELECT Idea FROM {category.replace(' ', '').lower()}"
            my_cursor.execute(query)
            stored_ideas = my_cursor.fetchall()
            if stored_ideas:
                for idea in stored_ideas:
                    text_widget.insert(tk.END, idea[0] + "\n")
            else:
                text_widget.insert(tk.END, "No ideas found")
        except mysql.connector.Error as e:
            print("Error connecting to MySQL database:", e)

    dropdown.bind("<<ComboboxSelected>>", lambda event: fetch_ideas())


def open_homepage():
    homepage = tk.Toplevel(root)
    homepage.title("Home Page")
    homepage.geometry("1000x1100")
    homepage.configure(bg="light green")


    background_image = tk.PhotoImage(file='C:/Users/spapa/Downloads/h1.png')
    background_label = tk.Label(homepage, image=background_image, borderwidth=0)
    background_label.place(relwidth=1, relheight=1)

    home_button1 = tk.Button(homepage, text="Login", command=Login, width=55, height=2,bg="red",fg="black")
    home_button2 = tk.Button(homepage, text="Share idea", command=open_idea_dialog, width=55, height=2,bg="green",fg="black")
    home_button3 = tk.Button(homepage, text="View ideas", command= retrieve_ideas_from_mysql,width=55, height=2,bg="yellow",fg="black")
    home_button4 = tk.Button(homepage, text="Liked ideas",command=liked_ideas,width=55, height=2,bg="blue",fg="black")

    home_button1.grid(row=0, column=0)
    home_button2.grid(row=0, column=1)
    home_button3.grid(row=0, column=2)
    home_button4.grid(row=0, column=3) 
    root.mainloop()
def liked_ideas():

    liked_window = tk.Toplevel(root)
    liked_window.title("Liked Ideas")

    bg_frame = tk.Frame(liked_window, bg="purple")
    bg_frame.place(relwidth=1, relheight=1)

    title_label = tk.Label(liked_window, text="Popular Ideas", font=("Arial", 25))
    title_label.place(relx=0.5,rely=0.1,anchor="center")


    copied_ideas_entry = tk.Text(liked_window, height=10, width=50, font=("Arial", 14))
    copied_ideas_entry.place(relx=0.5,rely=0.3,anchor="center")

    def fetch_liked_ideas():
        try:
            copied_ideas_entry.delete(1.0, tk.END) 
            my_cursor.execute("SELECT Idea FROM likedideas")
            liked_ideas = my_cursor.fetchall()
            if liked_ideas:
                for idea in liked_ideas:
                    copied_ideas_entry.insert(tk.END, idea[0] + "\n")
            else:
                copied_ideas_entry.insert(tk.END, "No liked ideas found")
        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Fetch Error", "Failed to fetch liked ideas. Please try again.")

    fetch_liked_ideas() 

    def paste_ideas():
        copied_ideas_text = root.clipboard_get()
        copied_ideas_entry.insert(tk.END, copied_ideas_text="\n")

    paste_button = tk.Button(liked_window, text="Paste", command=paste_ideas, font=("Arial", 14), bg="blue", fg="white")
    paste_button.place(relx=0.5,rely=0.6,anchor="center")

    def submit_liked_ideas():
        ideas = copied_ideas_entry.get("1.0", "end-1c").split("\n")
        if ideas:
            try:
                sql = "INSERT INTO likedideas (Idea) VALUES (%s)"
                for idea in ideas:
                    if idea.strip():  
                        val = (idea,)
                        my_cursor.execute(sql, val)
                conn.commit()
                messagebox.showinfo("Liked Ideas Submitted", "Liked ideas submitted successfully!")
            except Exception as e:
                print("Error:", e)
                messagebox.showerror("Submission Error", "Failed to submit liked ideas. Please try again.")

    submit_button = tk.Button(liked_window, text="Submit", command=submit_liked_ideas, font=("Arial", 14), bg="green", fg="white")
    submit_button.place(relx=0.5,rely=0.7,anchor="center")

def registraion():
    root = tk.Tk()
    root.title("Registration Page")

    window_width = 600
    window_height = 600
    screen_width = root.winfo_screenwidth() 
    screen_height = root.winfo_screenheight() 
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))
    root.configure(bg="light blue")

    heading_label = tk.Label(root, text="REGISTRATION   PAGE", font=("Helvetica", 25),fg="dark blue",bg="light blue")
    heading_label.pack(pady=(50, 10))
    form_frame = tk.Frame(root)
    form_frame.pack(pady=(100, 10))

    label_first_name = tk.Label(form_frame, text="Firstname :",font=("Arial", 20))
    label_first_name.grid(row=0,column=0, pady=10)
    entry_first_name = tk.Entry(form_frame,font=("Arial", 14), width=20)
    entry_first_name.grid(row=0,column=1, pady=10)

    label_last_name = tk.Label(form_frame, text="Lastname :",font=("Arial", 20))
    label_last_name.grid(row=1,column=0, pady=10)
    entry_last_name = tk.Entry(form_frame,font=("Arial", 14), width=20)
    entry_last_name.grid(row=1,column=1, pady=10)

    label_username = tk.Label(form_frame, text="Username :",font=("Arial", 20))
    label_username.grid(row=2,column=0, pady=10)
    entry_username = tk.Entry(form_frame,font=("Arial", 14), width=20)
    entry_username.grid(row=2,column=1, pady=10)

    label_email = tk.Label(form_frame, text="Email :",font=("Arial", 20))
    label_email.grid(row=3,column=0, pady=10)
    entry_email = tk.Entry(form_frame,font=("Arial", 14), width=20)
    entry_email.grid(row=3,column=1, pady=10)

    label_password = tk.Label(form_frame, text="Password :",font=("Arial", 20))
    label_password.grid(row=4,column=0, pady=10)
    entry_password = tk.Entry(form_frame, show="*",font=("Arial", 14), width=20)
    entry_password.grid(row=4,column=1, pady=10)

    label_phone_number = tk.Label(form_frame, text="Phonenumber :",font=("Arial", 20))
    label_phone_number.grid(row=5,column=0, pady=10)
    entry_phone_number = tk.Entry(form_frame,font=("Arial", 14), width=20)
    entry_phone_number.grid(row=5,column=1, pady=10)


    def submit():
        Firstname = entry_first_name.get()
        Lastname = entry_last_name.get()
        Username = entry_username.get()
        Email = entry_email.get()
        Password = entry_password.get()
        phonenumber = entry_phone_number.get() 
       
    
        try:
            sql = "INSERT INTO registereddata (Firstname, Lastname, Username, Email, Password, Phonenumber) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (Firstname, Lastname, Username, Email, Password, phonenumber)
            my_cursor.execute(sql, val)
            conn.commit()
            messagebox.showinfo("Registration successful.", "Thank you for registering!")
        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Registration failed", "Failed to register. Please try again.")
    submit_button1 = tk.Button(form_frame, text="Submit", command=submit,font=("Arial", 20))
    submit_button1.grid(row=6,column=1, pady=1)
    root.mainloop()


root = tk.Tk()
root.title("Login Page")
window_width = 600
window_height = 600
screen_width = root.winfo_screenwidth() 
screen_height = root.winfo_screenheight() 
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))

heading_label = tk.Label(root, text="SHARING IDEAS", font=("Helvetica", 25))
heading_label.pack(pady=(50, 10))
form_frame = tk.Frame(root)
form_frame.pack(pady=(100, 10))

label_username = tk.Label(form_frame, text="Username:", font=("Arial", 16))
label_username.grid(row=0, column=0, pady=5, sticky="e", padx=10)

entry_username = tk.Entry(form_frame, font=("Arial", 14))
entry_username.grid(row=0, column=1, pady=5, sticky="w", padx=10)

label_password = tk.Label(form_frame, text="Password:", font=("Arial", 16))
label_password.grid(row=1, column=0, pady=5, sticky="e", padx=10)

entry_password = tk.Entry(form_frame, show="*", font=("Arial", 14))  
entry_password.grid(row=1, column=1, pady=5, sticky="w", padx=10)

login_button = tk.Button(form_frame, text="Login", command=Login, font=("Arial", 14), bg="green", fg="white", width=10)
login_button.grid(row=2, column=0, pady=20, padx=(10, 15), sticky="e")

register_button = tk.Button(form_frame, text="Register", command=registraion,font=("Arial", 14), bg="blue", fg="white", width=15)
register_button.grid(row=2, column=1, pady=20, padx=(5, 10), sticky="w")

root.mainloop()


