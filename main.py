import subprocess
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import time
from tkinter import messagebox, PhotoImage, Listbox, END, ACTIVE, BOTH
import pyodbc
import pandas as pd
import csv

def main():
    def fetch_tables1():
        url = entry_url1.get()
        user = entry_user1.get()
        password = entry_password1.get()
        database = entry_database1.get()

        connection_string1 = f"DRIVER={{SQL Server}};SERVER={url};DATABASE={database};UID={user};PWD={password}"

        # Add table names to the listbox
        table_names = fetch_tables(connection_string1)
        for table_name in table_names:
            listbox_table.insert(END, table_name)

    def fetch_tables2():
        url = entry_url2.get()
        user = entry_user2.get()
        password = entry_password2.get()
        database = entry_database2.get()

        connection_string1 = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={url};DATABASE={database};UID={user};PWD={password}"

        # Add table names to the listbox
        table_names = fetch_tables(connection_string1)
        for table_name in table_names:
            listbox_table2.insert(END, table_name)

        # Add table names to the listbox
        table_names = fetch_tables_tenant()
        for table_name in table_names:
            listbox_table3.insert(END, table_name)

    def fetch_tables(connection_string):
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("select CONCAT(TABLE_SCHEMA,'.',TABLE_NAME) as table_name from information_schema.tables where table_type = 'BASE TABLE' order by table_name")

        tables = cursor.fetchall()

        list = []
        for table in tables:
            list.append(table.table_name)

        return list

    def fetch_tables_tenant():
        url2 = entry_url2.get()
        user2 = entry_user2.get()
        password2 = entry_password2.get()
        database2 = entry_database2.get()

        connection_string2 = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={url2};DATABASE={database2};UID={user2};PWD={password2}"
        conn = pyodbc.connect(connection_string2)
        cursor = conn.cursor()
        cursor.execute("select TenantID as table_name from [config].[tblTenantInformation] where CustomerOnboardingFlag = 1 order by table_name")

        tables = cursor.fetchall()

        list = []
        for table in tables:
            list.append(table.table_name)

        return list

    def export_query_to_csv(connection_string, query, file_path):
        try:
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
            cursor.execute(query)

            with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([col[0] for col in cursor.description])
                writer.writerows((str(item) for item in row) for row in cursor.fetchall())

            print("Data written to CSV file successfully!")

            cursor.close()
            conn.close()

        except pyodbc.Error as e:
            print("Error occurred while executing query:", e)

    def filter_common_headers(file_path1, file_path2):
        try:
            # Step 1: Read CSV files into DataFrames
            df1 = pd.read_csv(file_path1)
            df2 = pd.read_csv(file_path2)

            # Step 2: Identify the common headers (columns)
            common_headers = list(set(df1.columns) & set(df2.columns))

            # Step 3: Keep only the common headers in both DataFrames
            df1_common = df1[common_headers]
            df2_common = df2[common_headers]

            # Step 4: Move the 'filter' column to the front of the DataFrame
            if 'filter' in df1_common.columns:
                filter_col = df1_common.pop('filter')
                df1_common.insert(0, 'filter', filter_col)

            if 'filter' in df2_common.columns:
                filter_col = df2_common.pop('filter')
                df2_common.insert(0, 'filter', filter_col)

            # Step 5: Save DataFrames to new CSV files separately
            output_file1 = "D:/Datatesting/sourceEE.csv"
            output_file2 = "D:/Datatesting/destinationEE.csv"

            df1_common.to_csv(output_file1, index=False)
            df2_common.to_csv(output_file2, index=False)

        except IOError as e:
            print("Error occurred while filtering common headers:", e)

    def export_and_filter():
        url1 = entry_url1.get()
        database1 = entry_database1.get()
        user1 = entry_user1.get()
        password1 = entry_password1.get()

        url2 = entry_url2.get()
        database2 = entry_database2.get()
        user2 = entry_user2.get()
        password2 = entry_password2.get()

        # Retrieve the selected table name from the first listbox
        selected_table_index = listbox_table.curselection()
        if not selected_table_index:
            messagebox.showerror("Error", "Please select a table name from the first listbox.")
            return
        selected_table_name = listbox_table.get(selected_table_index)

        # Retrieve the selected table name from the second listbox
        selected_table_index2 = listbox_table2.curselection()
        if not selected_table_index2:
            messagebox.showerror("Error", "Please select a table name from the second listbox.")
            return
        selected_table_name2 = listbox_table2.get(selected_table_index2)

        # Retrieve the selected table name from the second listbox
        selected_table_index3 = listbox_table3.curselection()
        if not selected_table_index3:
            messagebox.showerror("Error", "Please select a Tenant name from the third listbox.")
            return
        selected_table_name3 = listbox_table3.get(selected_table_index3)

        connection_string1 = f"DRIVER={{SQL Server}};SERVER={url1};DATABASE={database1};UID={user1};PWD={password1}"
        connection_string2 = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={url2};DATABASE={database2};UID={user2};PWD={password2}"

        # Extract the table name and remove the schema name
        selected_table_name_order = selected_table_name.split('.')[-1]

        print(selected_table_name_order)

        selectQueryOrder = f"SELECT C.COLUMN_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS T JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE C ON C.CONSTRAINT_NAME=T.CONSTRAINT_NAME WHERE C.TABLE_NAME='{selected_table_name_order}' and T.CONSTRAINT_TYPE='PRIMARY KEY'"
        conn = pyodbc.connect(connection_string1)
        cursor = conn.cursor()
        cursor.execute(selectQueryOrder)

        orderby_var = cursor.fetchall()
        # Extract the values and join them with ', ' to remove brackets and commas
        orderby_columns = ', '.join(row[0] for row in orderby_var)
        print(orderby_columns)

        selectQuery1 = f"SELECT {orderby_columns} as filter,* FROM {selected_table_name} order by {orderby_columns}"
        selectQuery2 = f"SELECT {orderby_columns} as filter,* FROM {selected_table_name2} where tenantid = '{selected_table_name3}' order by {orderby_columns}"

        count_source = f"SELECT count(*) as count_source FROM {selected_table_name}"
        conn = pyodbc.connect(connection_string1)
        cursor = conn.cursor()
        cursor.execute(count_source)

        count_source1 = cursor.fetchval()
        count_source2 = str(count_source1)
        print(count_source2)

        count_dwh = f"SELECT count(*) as count_dwh FROM {selected_table_name2} where tenantid = '{selected_table_name3}'"
        conn = pyodbc.connect(connection_string2)
        cursor = conn.cursor()
        cursor.execute(count_dwh)

        count_dwh1 = cursor.fetchval()
        count_dwh2 = str(count_dwh1)
        print(count_dwh2)

        file_path1 = "D:/Datatesting/source3.csv"
        file_path2 = "D:/Datatesting/destination3.csv"

        export_query_to_csv(connection_string1,selectQuery1,file_path1)
        export_query_to_csv(connection_string2,selectQuery2,file_path2)
        filter_common_headers(file_path1, file_path2)
        start()
        messagebox.showinfo("Success", "Data exported and filtered successfully!")
        try:
            subprocess.Popen(["D:/Datatesting/dist/next_one/next_one.exe",orderby_columns,selected_table_name_order,count_source2,count_dwh2])
        except FileNotFoundError:
            messagebox.showerror("Error", "Failed to launch the next UI.")

        # Show success message
        messagebox.showinfo("Success", "Data exported and filtered successfully!")

    def start():
        progress = 100
        load = 0
        speed = 1
        while(load<progress):
            time.sleep(0.05)
            bar['value']+=(speed/progress)*100
            load+=speed
            percent.set(str(int((load/progress)*100)))
            window.update_idletasks()

        bar.stop()
    # Create the Tkinter window
    window = tk.Tk()
    window.title("Database Export and Filter")
    window.geometry("950x500")

    img = PhotoImage(file='D:/Datatesting/Backimg.png')
    tk.Label(window, image=img, bg='white').place(x=0.001, y=0.001)

    # Create the URL1 input label and entry field
    label_url1 = tk.Label(window, text="Source DB URL:")
    label_url1.place(x=50, y=200)
    entry_url1 = tk.Entry(window)
    entry_url1.place(x=50, y=220)

    # Create the Database1 input label and entry field
    label_database1 = tk.Label(window, text="Source DB Name:")
    label_database1.place(x=50, y=240)
    entry_database1 = tk.Entry(window)
    entry_database1.place(x=50, y=260)

    # Create the User1 input label and entry field
    label_user1 = tk.Label(window, text="Source DB User:")
    label_user1.place(x=50, y=280)
    entry_user1 = tk.Entry(window)
    entry_user1.place(x=50, y=300)

    # Create the Password1 input label and entry field
    label_password1 = tk.Label(window, text="Source DB Password:")
    label_password1.place(x=50, y=320)
    entry_password1 = tk.Entry(window, show="*")
    entry_password1.place(x=50, y=340)

    # Create the Table Name list label and listbox
    label_table = tk.Label(window, text="Table Name Source:")
    label_table.place(x=220, y=200)
    listbox_table = Listbox(window, width=30)
    listbox_table.place(x=220, y=220)

    export_button = tk.Button(window, text="connect src", command=fetch_tables1, width=20)
    export_button.place(x=50, y=380)

    # Create the URL2 input label and entry field
    label_url2 = tk.Label(window, text="DWH DB URL:")
    label_url2.place(x=650, y=200)
    entry_url2 = tk.Entry(window)
    entry_url2.place(x=650, y=220)

    # Create the Database2 input label and entry field
    label_database2 = tk.Label(window, text="DWH DB Name:")
    label_database2.place(x=650, y=240)
    entry_database2 = tk.Entry(window)
    entry_database2.place(x=650, y=260)

    # Create the User2 input label and entry field
    label_user2 = tk.Label(window, text="DWH DB User:")
    label_user2.place(x=650, y=280)
    entry_user2 = tk.Entry(window)
    entry_user2.place(x=650, y=300)

    # Create the Password2 input label and entry field
    label_password2 = tk.Label(window, text="DWH DB Password:")
    label_password2.place(x=650, y=320)
    entry_password2 = tk.Entry(window, show="*")
    entry_password2.place(x=650, y=340)

    # Create the Table Name list label and listbox
    label_table = tk.Label(window, text="Onboarded Tenant:")
    label_table.place(x=790, y=250)
    listbox_table3 = Listbox(window, selectmode="browse", exportselection=False, width=20,height=5)
    listbox_table3.pack(padx=10, pady=10, fill=BOTH, expand=True)
    listbox_table3.place(x=790, y=270)


    export_button = tk.Button(window, text="connect dwh", command=fetch_tables2, width=20)
    export_button.place(x=650, y=380)

    # Create the Table Name list label and listbox
    label_table = tk.Label(window, text="Table Name DWH:")
    label_table.place(x=440, y=200)
    listbox_table2 = Listbox(window, selectmode="browse",exportselection=False, width=30)
    listbox_table2.pack(padx=10,pady=10,fill=BOTH,expand=True)
    listbox_table2.place(x=440, y=220)

    # Create the Export button
    export_button = tk.Button(window, text="Compare", command=export_and_filter, width=10)
    export_button.place(x=435, y=425)

    percent = StringVar()
    text = StringVar()

    bar = Progressbar(window,orient=HORIZONTAL,length=300)
    bar.place(x=330, y=390)

    percentLabel = Label(window,textvariable=percent)
    percentLabel.place(x=470, y=410)

    # Run the Tkinter event loop
    window.mainloop()

if __name__ == "__main__":
    main()

