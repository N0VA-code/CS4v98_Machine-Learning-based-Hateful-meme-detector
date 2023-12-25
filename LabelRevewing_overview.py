import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Function for data analysis and visualization
def analyze_and_visualize(csv_file):
    data = pd.read_csv(csv_file)

    # Data analysis
    # Count the number of occurrences for each reviewer_label (0, 1, -1, -5, -7, -88, -99) and display the results.
    specified_labels = [0, 1, -1, -5, -7, -88, -99]
    label_counts = data['reviewer_label'].value_counts().reindex(specified_labels, fill_value=0)
    # Calculate the progress rate, defined as the proportion of reviewer_label entries that are marked as 0, 1, or -99, out of the total reviewer_label entries (including those not labeled).
    progress_labels = [0, 1, -99]
    progress_count = data['reviewer_label'].isin(progress_labels).sum()
    total_labels = len(data['reviewer_label'])
    progress_rate = progress_count / total_labels
    # Calculate the label agreement rate, which is the percentage of cases where both reviewer_label and label are not empty, and the values in these two fields are the same.
    non_empty_labels = data.dropna(subset=['reviewer_label', 'label'])
    matches = non_empty_labels[non_empty_labels['reviewer_label'] == non_empty_labels['label']].shape[0]
    match_rate = matches / non_empty_labels.shape[0] if non_empty_labels.shape[0] > 0 else 0

    # Data visualization
    fig, axs = plt.subplots(3, 1, figsize=(6, 8))

    # Bar chart
    axs[0].bar(label_counts.index.astype(str), label_counts.values, color='skyblue')
    axs[0].set_title('Reviewer Label Counts')
    axs[0].set_xlabel('Reviewer Labels')
    axs[0].set_ylabel('Counts')

    # Pie chart for progress rate
    axs[1].pie([progress_rate, 1 - progress_rate], labels=['Progress Rate', 'Remaining'], autopct='%1.1f%%',
               startangle=90, colors=['lightgreen', 'lightgrey'])
    axs[1].set_title('Progress Rate')

    # Pie chart for match rate
    axs[2].pie([match_rate, 1 - match_rate], labels=['Match Rate', 'Mismatch'], autopct='%1.1f%%', startangle=90,
               colors=['gold', 'lightgrey'])
    axs[2].set_title('Match Rate')

    plt.tight_layout()
    return label_counts, progress_rate, match_rate, fig


# Function to select file and display visualization
def upload_action():
    filename = filedialog.askopenfilename()
    if filename:
        label_counts, progress_rate, match_rate, fig = analyze_and_visualize(filename)

        # Display results in text
        results_text = f"Reviewer Label Counts:\n{label_counts}\n\n" \
                       f"Progress Rate: {progress_rate * 100:.2f}%\n" \
                       f"Match Rate: {match_rate * 100:.2f}%"
        results_label.config(text=results_text)

        # Display visualization
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack()


# tkinter GUI setup
root = tk.Tk()
root.title("Data Analysis and Visualization")

upload_button = tk.Button(root, text="Upload CSV", command=upload_action)
upload_button.pack()

# Label for displaying results
results_label = tk.Label(root, text="", justify=tk.LEFT)
results_label.pack()

root.mainloop()
