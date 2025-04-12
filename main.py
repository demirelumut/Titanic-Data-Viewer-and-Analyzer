import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the Titanic dataset
titanic_data = pd.read_csv('titanic_data.csv')

# Create the main application window
root = tk.Tk()
root.title("Titanic Data Viewer and Analyzer")
root.geometry("1000x750")
root.configure(bg="light gray")  # Light blue background

# Global variables
canvas_widget = None
info_label = None

# Function to display passenger details by name
def search_by_name():
    name = name_entry.get()
    result = titanic_data[titanic_data['Name'].str.contains(name, case=False, na=False)]
    if result.empty:
        messagebox.showinfo("Not Found", f"No passenger found with name containing '{name}'.")
    else:
        details_text.delete("1.0", tk.END)
        details_text.insert("1.0", result.to_string(index=False))

# Function to plot survival analysis
def plot_survival():
    global canvas_widget, info_label

    category = category_var.get()
    value = value_entry.get()

    if not category or not value:
        messagebox.showerror("Input Error", "Please select a category and enter a value.")
        return

    try:
        filtered_data = titanic_data[titanic_data[category].astype(str).str.contains(value, case=False, na=False)]
        if filtered_data.empty:
            messagebox.showinfo("No Data", f"No data found for {category} = {value}.")
            return

        survival_counts = filtered_data['Survived'].value_counts(normalize=True) * 100

        # Plot the data
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.set_facecolor('gray')
        survival_counts.plot(kind='barh', color=['salmon', 'green'], ax=ax)  # Softer colors, horizontal bar
        ax.set_title(f"Survival Rates by {category} = {value}", fontsize=14)
        ax.set_xlabel("Percentage", fontsize=12)
        ax.set_ylabel("Survived", fontsize=12)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['Died', 'Survived'], fontsize=10)

        # Clear previous canvas and info label if exist
        if canvas_widget:
            canvas_widget.pack_forget()
        if info_label:
            info_label.destroy()

        # Embed the plot in the GUI
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=10)
        canvas.draw()

        # Display percentages below the graph
        info_text = (f"Percentage Not Survived: {survival_counts.get(0, 0):.2f}%\n"
                     f"Percentage Survived: {survival_counts.get(1, 0):.2f}%")
        info_label = tk.Label(root, text=info_text, bg="Light Gray", font=("Arial", 12), justify="center")
        info_label.pack(pady=5)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to reset the plot
def reset_plot():
    global canvas_widget, info_label
    if canvas_widget:
        canvas_widget.pack_forget()
        canvas_widget = None
    if info_label:
        info_label.destroy()
        info_label = None

# GUI Elements




frame = tk.Frame(root, bg="Silver")
frame.pack(fill=tk.BOTH, expand=True, pady=10)

# Search by Name Section
tk.Label(frame, text="Enter Passenger Name:", bg="#F5F5DC", font=("Arial", 15)).grid(row=0, column=0, padx=15, pady=5, sticky="w")
name_entry = tk.Entry(frame, width=50, font=("Arial", 14))
name_entry.grid(row=0, column=1, padx=5, pady=5)
search_button = tk.Button(frame, text="Search", command=search_by_name, bg="gray", fg="black", font=("Arial", 13))
search_button.grid(row=0, column=2, padx=5, pady=5)

# Text box to display details
details_text = tk.Text(frame, height=10, width=120, bg='Gray', fg='Black' , font=("Courier", 10))
details_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# Survival Analysis Section
tk.Label(frame, text="Select Category:", bg="#F5F5DC", font=("Arial", 12)).grid(row=2, column=0, padx=20, pady=5, sticky="w")
category_var = tk.StringVar()


category_menu = ttk.Combobox(frame, textvariable=category_var,  values=['Sex', 'Age', 'Pclass', 'Embarked'], state="readonly", font=("Arial", 12))
category_menu.grid(row=2, column=1, padx=5, pady=5)



tk.Label(frame, text="Enter Value:", bg="#F5F5DC", font=("Arial", 12)).grid(row=3, column=0, padx=20, pady=5, sticky="w")
value_entry = tk.Entry(frame, width=30, font=("Arial", 12))
value_entry.grid(row=3, column=1, padx=5, pady=5)

plot_button = tk.Button(frame, text="Plot Survival", command=plot_survival, bg="Gray", fg="gold", font=("Arial", 12))
plot_button.grid(row=3, column=2, padx=5, pady=5)

reset_button = tk.Button(frame, text="Reset Plot", command=reset_plot, bg="gray", fg="orange", font=("Arial", 12))
reset_button.grid(row=4, column=2, padx=5, pady=5)

# Run the application
root.mainloop()
