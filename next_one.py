import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
import sys

if len(sys.argv) > 1:
    received_variable = sys.argv[1]
    received_variable2 = sys.argv[2]
    received_variable3 = sys.argv[3]
    received_variable4 = sys.argv[4]
    print("Received variable:", received_variable,received_variable2,received_variable3,received_variable4)
else:
    print("No variable received.")

def compare_csv_files():
    file_path1 = file1_entry.get()  # Use the value from the Entry widget
    file_path2 = file2_entry.get()  # Use the value from the Entry widget

    try:
        with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
            df1 = pd.read_csv(file_path1)
            df2 = pd.read_csv(file_path2)

            # Sort the columns of both DataFrames
            df1_sorted = df1.reindex(sorted(df1.columns), axis=1)
            df2_sorted = df2.reindex(sorted(df2.columns), axis=1)

            print(df1_sorted)
            print(df2_sorted)

            unique_column = "filter"
            # Merge the DataFrames on the unique column
            merged_df = pd.merge(df1_sorted, df2_sorted, on=unique_column, how="outer")

            print(merged_df)

            # Find differences and create a list of tuples
            differences = []
            for index, row in merged_df.iterrows():
                for col in df1.columns:  # Use the original column names without suffixes
                    if col != unique_column:
                        value1 = row[col + "_x"]
                        value2 = row[col + "_y"]

                        # Compare values while handling NaN
                        if pd.isna(value1) and pd.isna(value2):
                            difference = False  # Both NaN, consider them equal
                        elif isinstance(value1, str) and isinstance(value2, str):
                            difference = value1.strip() != value2.strip()  # String comparison
                        else:
                            difference = value1 != value2  # Other types comparison

                        if difference:
                            differences.append((row[unique_column], col, value1, value2))

            # Display Mismatch field values in a tabular form
            if len(differences) > 0:

                if (received_variable3 < received_variable4):
                    table_window = tk.Toplevel()
                    table_window.title(f"Mismatch Fields of {received_variable2} and Dublicates")

                    tree = ttk.Treeview(table_window)
                    tree["columns"] = ("row", "field_name1", "source_value", "datawarehouse_value")
                    tree.heading("row", text=f"Primary Key = {received_variable}")
                    tree.heading("field_name1", text="Mismatch Field Name")
                    tree.heading("source_value", text=f"Source Value and Count = {received_variable3}")
                    tree.heading("datawarehouse_value", text=f"DWH Count= {received_variable4},Dublicate")

                    for i, (row, field_name1, source_value, datawarehouse_value) in enumerate(differences):
                        tree.insert("", tk.END, values=(row, field_name1, source_value, datawarehouse_value))

                    tree.pack()

                    style = ttk.Style(table_window)
                    style.theme_use("clam")  # set theam to clam
                    style.configure("Treeview", background="mediumvioletred",
                                    fieldbackground="white", foreground="white")
                    style.configure('Treeview.Heading', background="PowderBlue")

                    table_window.mainloop()

                else:
                    table_window = tk.Toplevel()
                    table_window.title(f"Mismatch Fields of {received_variable2}")

                    tree = ttk.Treeview(table_window)
                    tree["columns"] = ("row", "field_name1", "source_value", "datawarehouse_value")
                    tree.heading("row", text=f"Primary Key = {received_variable}")
                    tree.heading("field_name1", text="Mismatch Field Name")
                    tree.heading("source_value", text=f"Source Value and Count = {received_variable3}")
                    tree.heading("datawarehouse_value", text=f"DWH Value and Count = {received_variable4}")

                    for i, (row, field_name1, source_value, datawarehouse_value) in enumerate(differences):
                        tree.insert("", tk.END, values=(row, field_name1, source_value, datawarehouse_value))

                    tree.pack()

                    style = ttk.Style(table_window)
                    style.theme_use("clam")  # set theam to clam
                    style.configure("Treeview", background="mediumvioletred",
                                    fieldbackground="white", foreground="white")
                    style.configure('Treeview.Heading', background="PowderBlue")
                    table_window.mainloop()

            else:
                if(received_variable3 < received_variable4):
                    table_window = tk.Toplevel()
                    table_window.title(f"No Mismatch fields found in {received_variable2} but DWH Dublicates")

                    tree = ttk.Treeview(table_window)
                    tree["columns"] = ("row", "field_name1", "source_value", "datawarehouse_value")
                    tree.heading("row", text=f"Primary Key = {received_variable}")
                    tree.heading("field_name1", text="No Mismatch Field")
                    tree.heading("source_value", text=f"Source Count = {received_variable3}")
                    tree.heading("datawarehouse_value", text=f"DWH Count Dublicate = {received_variable4}")

                    for i, (row, field_name1, source_value, datawarehouse_value) in enumerate(differences):
                        tree.insert("", tk.END, values=(row, "field_name1", "source_value", "datawarehouse_value"))

                    tree.pack()

                    style = ttk.Style(table_window)
                    style.theme_use("clam")  # set theam to clam
                    style.configure("Treeview", background="mediumvioletred",
                                    fieldbackground="white", foreground="white")
                    style.configure('Treeview.Heading', background="PowderBlue")
                    table_window.mainloop()

                else:
                    table_window = tk.Toplevel()
                    table_window.title(f"No Mismatch fields found in {received_variable2}")
                    tree = ttk.Treeview(table_window)
                    tree["columns"] = ("row", "field_name1", "source_value", "datawarehouse_value")
                    tree.heading("row", text=f"Primary Key = {received_variable}")
                    tree.heading("field_name1", text="No Mismatch Field")
                    tree.heading("source_value", text=f"Source Count = {received_variable3}")
                    tree.heading("datawarehouse_value", text=f"DWH Count = {received_variable4}")

                    for i, (row, field_name1, source_value, datawarehouse_value) in enumerate(differences):
                        tree.insert("", tk.END, values=(row, "field_name1", "source_value", "datawarehouse_value"))

                    tree.heading("#0", text="No Mismatch Found", anchor='c')
                    tree.insert("", tk.END, values=("", "                No Mismatch"))

                    tree.pack()

                    style = ttk.Style(table_window)
                    style.theme_use("clam")  # set theam to clam
                    style.configure("Treeview", background="green",
                                    fieldbackground="white", foreground="white")
                    style.configure('Treeview.Heading', background="PowderBlue")
                    table_window.mainloop()


    except IOError as e:
        messagebox.showerror("Error", f"Error occurwhite while comparing CSV files: {e}")

window = tk.Tk()
window.title(f"CSV File Comparison of {received_variable2}")
window.geometry("470x150")

img = tk.PhotoImage(file='D:/Datatesting/Untitled.png')
tk.Label(window, image=img, bg='white').place(x=0.001, y=0.001)

file1_label = tk.Label(window, text="File 1:")
file1_label.grid(row=0, column=0, sticky="e")
file1_label.place(x=80,y=20)

file1_entry = tk.Entry(window, width=39)
file1_entry.grid(row=0, column=1)
file1_entry.insert(tk.END, "D:/Datatesting/sourceEE.csv")
file1_entry.place(x=120,y=20)

file2_label = tk.Label(window, text="File 2:")
file2_label.grid(row=1, column=0, sticky="e")
file2_label.place(x=80,y=110)

file2_entry = tk.Entry(window, width=43)
file2_entry.grid(row=1, column=1)
file2_entry.insert(tk.END, "D:/Datatesting/destinationEE.csv")
file2_entry.place(x=120,y=110)

photo = tk.PhotoImage(file =r"D:/Datatesting/imgBtn.png")

compare_button = tk.Button(window, text="Compare", command=compare_csv_files,image=photo)
compare_button.grid(row=2, column=1, pady=10)
compare_button.place(x=190,y=50,width=60,height=50)

# Start the Tkinter event loop
window.mainloop()