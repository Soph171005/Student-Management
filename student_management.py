import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


#Data base connection

con = sqlite3.connect("school.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS student(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    marks REAL
) 
""")

con.commit()

#Main Window

root = tk.Tk()
root.title("Student Management System")
root.geometry("850x600")
root.configure(bg ="#f0f4f8")

#Title

title = tk.Label(
    root,
    text = "STUDENT MANAGEMENT SYSTEM",
    font = ("Arial", 22, "bold"),
    bg = "#1e3a5f",
    fg = "white",
    pady=15

)
title.pack(fill = "x")

#Input Frame

input_frame = tk.LabelFrame(
    root,
    text="Student Details",
    font = ("Arial", 12, "bold"),
    padx=20,
    pady=15,
    bg="#f0f4f8"
)

input_frame.pack(fill="x") 

#Student ID
tk.Label(input_frame, text="Student ID", bg= "#f0f4f8",
         font=("Arial",11)).grid(row=0, column=0, padx=10,pady=8)
id_entry = tk.Entry(input_frame, font=("Arial",11))
id_entry.grid(row=0, column=1, padx=10,pady=8)

#Student Name
tk.Label(input_frame, text="Student Name:", bg="#f0f4f8",
         font=("Arial",11)).grid(row=0, column=2, padx=10,pady=8)
name_entry = tk.Entry(input_frame, font=("Arial",11))
name_entry.grid(row=0, column=3,padx=10,pady=8)

#Age
tk.Label(input_frame, text = "Age:", bg= "#f0f4f8", 
         font = ("Arial",11)).grid(row=1, column=0,padx=10,pady=8)
age_entry = tk.Entry(input_frame, font=("Arial",11))
age_entry.grid(row=1,column=1,padx=10,pady=8)

#Marks 
tk.Label(input_frame, text = "Marks:", bg = "#f0f4f8",
         font = ("Arial",11)).grid(row=1, column=2,padx=10,pady=8)
marks_entry = tk.Entry(input_frame, font=("Arial",11))
marks_entry.grid(row=1, column=3, padx=10,pady=8)

#Clear Function

def clear_feilds():
    id_entry.delete(0,tk.END)
    name_entry.delete(0,tk.END)
    age_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

#Add student
def add_student():
    name = name_entry.get().strip() #.strip removes 
    age = age_entry.get()
    marks = marks_entry.get()

    if name == "" or age == "" or marks == "":
        messagebox.showerror("Error", "Please enter all details")
        return
    try:
        age = int(age)
        marks = float(marks)
        if age <=0 or marks < 0 or marks > 100:
            messagebox.showerror("Error", "Enter Valid age and marks (0-100)")
            return
        cur.execute("""
        INSERT INTO students(name,age,marks)
        VALUES(?,?,?)
        """, (name,age,marks))

        con.commit()

        messagebox.showinfo("Success", "Student added successfully!")

        clear_feilds()
        display_students()

    except ValueError:
        messagebox.showerror("Error", "Age must be an integer and marks must be numeric")
    except sqlite3.Error as e:
        con.rollback() #create feedback for system so it can update all the values 
        messagebox.showerror("Database Error", str(e))

#Display Students

def display_students():
    for item in tree.get_children():
        tree.delete(item)
    try:
        cur.execute("SELECT * FROM students")
        records = cur.fetchall()

        for row in records:
            tree.insert("", tk.END, values=row)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))

#Search Student
def search_student():
    student_id = id_entry.get().strip()
    if student_id == "":
        messagebox.showerror("Error", "Enter Student ID")
        return
    try:
        cur.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id)
        )

        record = cur.fetchone()
        if record:
             clear_feilds()
             id_entry.insert(0,record[0])
             name_entry.insert(0,record[1])
             age_entry.insert(0,record[2])
             marks_entry.insert(0,record[3])

             messagebox.showinfo("Success", "Student found!")
        else:
            messagebox.showwarning("Not found", "Student does not exist")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))

#update marks

def update_marks():
    student_id = id_entry.get().strip()
    marks = marks_entry.get().strip()

    if student_id == "" or marks == "":
        messagebox.showerror("Error", "Enter Student ID and new marks")
        return
    try:
        student_id = int(student_id)
        marks = float(marks)

        if marks < 0 or marks > 100:
            messagebox.showerror("Error", "Marks must be between 0 and 100")
            return

        cur.execute("""
        UPDATE students
        SET marks = ?
        WHERE id = ?
        """, (marks, student_id))

        if cur.rowcount == 0:
            con.rollback()
            messagebox.showwarning("Not Found", "Student ID not found")
        else:
            con.commit()
            messagebox.showinfo("Success", "Marks updated successfully")
            clear_feilds()
            display_students()
    except ValueError:
        messagebox.showerror("Error", "Enter a valid ID and marks")
    except sqlite3.Error as e:
        con.rollback()
        messagebox.showerror("Database Error", str(e))

#Delete Student

def delete_student():
    student_id = id_entry.get().strip()

    if student_id == "":
        messagebox.showerror("Error", "Enter Student ID")
        return
    try:
        student_id = int(student_id)
        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this student?"

        )

        if answer:
            cur.execute(
                "DELETE FROM students WHERE id = ?",
                (student_id,)
            )

            if cur.rowcount == 0:
                con.rollback()
                messagebox.showwarning("Not Found", "Student ID not found")
            else:
                con.commit()
                messagebox.showinfo("Success", "Student deleted successfully!")
                clear_feilds()
                display_students()
    except ValueError:
        messagebox.showerror("Error", "Enter a valid Student ID")
    except sqlite3.Error as e:
        con.rollback()
        messagebox.showerror("Database Error", str(e))

#Button Frame

button_frame = tk.Frame(root, bg = "#f0f4f8")
button_frame.pack(pady=10)

tk.Button(
    button_frame, text = "Add Student",
    command = add_student, width = 15,
    bg = "#198754", fg="white",
    font=("Arial",10,"bold")
).grid(row=0,column=0,padx=0,pady=5)

tk.Button(
    button_frame, text = "Display Students",
    command=display_students, width=15,
    bg="#0d6efd", fg = "white",
    font=("Arial",10,"bold")
).grid(row=0, column=1,padx=8,pady=5)

tk.Button(
    button_frame, text = "Search Student",
    command = search_student, width=15,
    bg="#6f42c1", fg="white",
    font=("Arial",10,"bold")
).grid(row=0, column=2,padx=8,pady=5)

tk.Button(
    button_frame, text = "Update Marks",
    command = update_marks, width=15,
    bg="#fd7e14", fg="white",
    font=("Arial", 10, "bold")
).grid(row=1, column=0, padx=8,pady=5)

tk.Button(
    button_frame, text="Delete Student",
    command = delete_student, width =15,
    bg = "#dc3545", fg="white",
    font=("Arial", 10, "bold")
).grid(row=1,column=1,padx=8,pady=5)

tk.Button(
    button_frame, text = "Clear Feilds",
    command=clear_feilds, width=15,
    bg="#6c757d", fg="white",
    font=("Arial",10,"bold")
).grid(row=1,column=2,padx=8,pady=5)

#Student Tabel

table_frame = tk.LabelFrame( #
    root,
    text="Student Records",
    font = ("Arial",12,"bold"),
    bg="#f0f4f8",
    padx=10,
    pady=10
)

table_frame.pack(padx=20,pady=15,fill="both", expand=True)

columns= ("ID", "Name", "Age", "Marks")

tree= ttk.Treeview( #
    table_frame,
    columns = columns,
    show="headings"
)

tree.heading("ID", text="Student ID")
tree.heading("Name", text = "Student Name")
tree.heading("Age", text = "Age")
tree.heading("Marks", text = "Marks")

tree.column("ID", width=100,anchor="center") #
tree.column("Name", width=250, anchor = "center") 
tree.column("Age", width =100, anchor ="center")
tree.column("Marks", width=150, anchor="center")

tree.pack(fill="both", expand=True)

#Select Record From Table

def select_student(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0],"values")

        clear_feilds()

        id_entry.insert(0,values[0]) #
        name_entry.insert(0,values[1])
        age_entry.insert(0, values[2])
        marks_entry.insert(0,values[3])
tree.bind("<<<TreeviewSelect>>", select_student)

#Exit application

def exit_application():
    answer = messagebox.askyesno(
        "Exit",
        "Do you want to exit the application?"
    )
    if answer:
        con.close()
        root.destroy()

exit_button = tk.Button(
    root,
    text="EXIT",
    command = exit_application, 
    bg="#212529",
    fg="white",
    width=15,
    font=("Arial", 11, "bold")
)

exit_button.pack(pady=10)
root.mainloop()