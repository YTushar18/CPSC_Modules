import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog, messagebox, Tk, Button, Label, Frame
from tkinter.ttk import Treeview

class BucketSortApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Bucket Sort Temperature Data")

        self.frame = Frame(self.root)
        self.frame.pack(pady=20)

        self.upload_label = Label(self.frame, text="No file selected")
        self.upload_label.pack(side='top', fill='x', pady=5)

        self.upload_button = Button(self.frame, text="Upload Data", command=self.load_data)
        self.upload_button.pack(side='top', fill='x', pady=5)

        self.sort_button = Button(self.frame, text="Sort Data", command=self.sort_data, state='disabled')
        self.sort_button.pack(side='top', fill='x', pady=5)

        self.visualize_button = Button(self.frame, text="Visualize Data", command=self.visualize_data, state='disabled')
        self.visualize_button.pack(side='top', fill='x', pady=5)

        self.table_frame = Frame(self.root)
        self.table_frame.pack(pady=20)
        self.tree = None

        self.sorted_data = None

    def load_data(self):
        file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            self.upload_label.config(text="File loaded successfully")
            self.sort_button.config(state='normal')
        else:
            messagebox.showwarning("Warning", "No file was selected.")

    def sort_data(self):
        if self.data is not None:
            try:
                self.sorted_data = self.data.sort_values(by='Sensor_ID', ascending=True).reset_index(drop=True)
                self.show_table(self.sorted_data)
                self.visualize_button.config(state='normal')
            except KeyError:
                messagebox.showerror("Error", "'Sensor_ID' column not found in the file.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def create_table(self, columns):
        if self.tree:
            self.tree.destroy()
        self.tree = Treeview(self.table_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        self.tree.pack(side='left', fill='both', expand=True)

    def show_table(self, data):
        self.create_table(list(data.columns))
        for _, row in data.iterrows():
            self.tree.insert('', 'end', values=list(row))

    def visualize_data(self):
        if self.sorted_data is not None:
            plt.figure(figsize=(10, 5))
            plt.plot(self.sorted_data['Sensor_ID'], marker='o')
            plt.title('Sorted Temperature Data')
            plt.xlabel('Index')
            plt.ylabel('Temperature (C)')
            plt.grid(True)
            plt.show()
        else:
            messagebox.showerror("Error", "No sorted data to visualize.")

if __name__ == "__main__":
    root = Tk()
    app = BucketSortApplication(root)
    root.mainloop()
