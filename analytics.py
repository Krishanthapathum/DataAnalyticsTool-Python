import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Button, Label, Frame, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# App window
root = Tk()
root.title("COVID-19 Analytics Dashboard")
root.geometry("1000x750")

# Global dataframe to store cleaned data
df_clean = None

# Title Label
title_label = Label(root, text="COVID-19 Analytics Dashboard", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Plot frame
dashboard_frame = Frame(root)
dashboard_frame.pack(pady=10)

plot_frame = Frame(root)
plot_frame.pack()

# File picker & loader
def load_file():
    global df_clean
    file_path = filedialog.askopenfilename(title="Select CSV or Excel File", filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx *.xls")])

    if not file_path:
        return

    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file_path)
    else:
        messagebox.showerror("Invalid File", "Unsupported file type! Please select CSV or Excel.")
        return

    # Basic Preprocessing
    try:
        df_clean = df.dropna(subset=['Confirmed', 'Deaths', 'Recovered', 'Active', 'Country/Region'])
        df_clean['Fatality Rate (%)'] = (df_clean['Deaths'] / df_clean['Confirmed']) * 100
        df_clean['Recovery Rate (%)'] = (df_clean['Recovered'] / df_clean['Confirmed']) * 100
        messagebox.showinfo("Success", "File loaded and processed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error processing file: {e}")

# Clear previous chart
def clear_plot_frame():
    for widget in plot_frame.winfo_children():
        widget.destroy()
    plt.close('all')

# Individual visualizations
def show_barplot():
    if df_clean is not None:
        clear_plot_frame()
        fig, ax = plt.subplots(figsize=(8, 5))
        top_10 = df_clean.nlargest(10, 'Confirmed')
        sns.barplot(data=top_10, x='Confirmed', y='Country/Region', palette="Blues_d", ax=ax)
        ax.set_title('Top 10 Countries by Confirmed Cases')
        render_plot(fig)

def show_scatter():
    if df_clean is not None:
        clear_plot_frame()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=df_clean, x='Confirmed', y='Deaths', hue='WHO Region', ax=ax)
        ax.set_title('Confirmed Cases vs Deaths')
        render_plot(fig)

def show_heatmap():
    if df_clean is not None:
        clear_plot_frame()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(df_clean[['Confirmed', 'Deaths', 'Recovered', 'Active']].corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Correlation Heatmap')
        render_plot(fig)

def show_piechart():
    if df_clean is not None:
        clear_plot_frame()
        fig, ax = plt.subplots(figsize=(6,6))
        top_5 = df_clean.nlargest(5, 'Confirmed')
        ax.pie(top_5['Confirmed'], labels=top_5['Country/Region'], autopct='%1.1f%%', startangle=140)
        ax.set_title('Top 5 Countries Share of Confirmed Cases')
        render_plot(fig)

# Render matplotlib figure inside Tkinter
def render_plot(fig):
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# GUI Buttons
Button(dashboard_frame, text="Load CSV or Excel File", command=load_file, width=25, bg='#4CAF50', fg='white').grid(row=0, column=0, padx=10, pady=5)
Button(dashboard_frame, text="Bar Plot", command=show_barplot, width=15).grid(row=0, column=1, padx=5)
Button(dashboard_frame, text="Scatter Plot", command=show_scatter, width=15).grid(row=0, column=2, padx=5)
Button(dashboard_frame, text="Heatmap", command=show_heatmap, width=15).grid(row=0, column=3, padx=5)
Button(dashboard_frame, text="Pie Chart", command=show_piechart, width=15).grid(row=0, column=4, padx=5)

root.mainloop()
