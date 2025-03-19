import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, Button, Label, Frame, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
root.title("COVID-19 Analytics App")
root.geometry("900x700")

frame = Frame(root)
frame.pack(pady=20)

label = Label(frame, text="COVID-19 Analytics Dashboard", font=("Helvetica", 16, "bold"))
label.pack()

plot_frame = Frame(root)
plot_frame.pack()

df_clean = None  # Global dataframe to store cleaned data

def load_file():
    global df_clean
    file_path = filedialog.askopenfilename(title="Select CSV or Excel File", filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx *.xls")])
    
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file_path)
    else:
        print("Unsupported file format")
        return

    # Preprocessing
    df_clean = df.dropna(subset=['Confirmed', 'Deaths', 'Recovered', 'Active', 'Country/Region'])
    df_clean['Fatality Rate (%)'] = (df_clean['Deaths'] / df_clean['Confirmed']) * 100
    df_clean['Recovery Rate (%)'] = (df_clean['Recovered'] / df_clean['Confirmed']) * 100
    print("File loaded and cleaned successfully!")

def clear_plot_frame():
    for widget in plot_frame.winfo_children():
        widget.destroy()
    plt.close('all')

def show_barplot():
    if df_clean is not None:
        clear_plot_frame()
        fig, ax = plt.subplots(figsize=(8, 5))
        top_10_cases = df_clean.nlargest(10, 'Confirmed')
        sns.barplot(data=top_10_cases, x='Confirmed', y='Country/Region', hue='Country/Region', palette="Blues_d", legend=False, ax=ax)
        ax.set_title('Top 10 Countries by Confirmed COVID-19 Cases')
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

def show_scatter():
    if df_clean is not None:
        clear_plot_frame()
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.scatterplot(data=df_clean, x='Confirmed', y='Deaths', hue='WHO Region', alpha=0.7, ax=ax)
        ax.set_title('Confirmed Cases vs Deaths by WHO Region')
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

def show_heatmap():
    if df_clean is not None:
        clear_plot_frame()
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.heatmap(df_clean[['Confirmed', 'Deaths', 'Recovered', 'Active']].corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Correlation Heatmap')
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

def show_piechart():
    if df_clean is not None:
        clear_plot_frame()
        fig, ax = plt.subplots(figsize=(5, 5))
        top_5_cases = df_clean.nlargest(5, 'Confirmed')
        ax.pie(top_5_cases['Confirmed'], labels=top_5_cases['Country/Region'], autopct='%1.1f%%', startangle=140)
        ax.set_title('Top 5 Countries Share of Global Confirmed Cases')
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

# GUI buttons
Button(frame, text="Load CSV or Excel File", command=load_file, width=30).pack(pady=5)
Button(frame, text="Show Bar Plot", command=show_barplot, width=30).pack(pady=5)
Button(frame, text="Show Scatter Plot", command=show_scatter, width=30).pack(pady=5)
Button(frame, text="Show Correlation Heatmap", command=show_heatmap, width=30).pack(pady=5)
Button(frame, text="Show Pie Chart", command=show_piechart, width=30).pack(pady=5)

root.mainloop()
