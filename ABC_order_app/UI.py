import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os

# Assuming your backend classes and filename_cleanup are in a file named backend.py
# If they are in the same file, just make sure they are defined above this.
from ABC_order_app.backend import FileManager, filename_cleanup

# --- Setup ---
folder = "word_files"
os.makedirs(folder, exist_ok=True)
file_manager = FileManager(folder)

root = tk.Tk()
root.title("Word List Manager")
root.geometry("450x600") # Set a default starting size

# --- UI LOGIC ---

def update_word_list(*args):
    """Refreshes the Listbox based on selected file and prefix."""
    listbox.delete(0, tk.END)
    selected_file = file_var.get().strip()
    words = []

    if selected_file and selected_file != "--- All Files ---":
        # 1. Show words from specific file
        if selected_file in file_manager.word_managers:
            words = file_manager.word_managers[selected_file].get_words()
        enable_word_controls(True)
    else:
        # 2. Show all words from all files
        for manager in file_manager.word_managers.values():
            words.extend(manager.get_words())
        enable_word_controls(False)

    # Apply prefix filter (case-insensitive)
    prefix = prefix_var.get().strip().lower()
    if prefix:
        words = [w for w in words if w.lower().startswith(prefix)]

    # Sort and remove duplicates for display
    display_words = sorted(list(set(words)))
    for w in display_words:
        listbox.insert(tk.END, w)
    
    # UPDATE WORD COUNT
    status_var.set(f"Total Words Displayed: {len(display_words)}")

def refresh_dropdown():
    """Updates the dropdown list and ensures 'All Files' is an option."""
    names = file_manager.get_filenames()
    file_dropdown['values'] = ["--- All Files ---"] + names

def enable_word_controls(is_enabled):
    """Enables or disables word-editing buttons based on selection."""
    state = "normal" if is_enabled else "disabled"
    btn_add_word.config(state=state)
    btn_remove_word.config(state=state)
    btn_edit_word.config(state=state)

# --- ACTION FUNCTIONS ---

def add_word():
    selected_file = file_var.get()
    word = word_entry.get().strip()
    if word and selected_file in file_manager.word_managers:
        file_manager.word_managers[selected_file].add_word(word)
        word_entry.delete(0, tk.END)
        update_word_list()

def remove_word():
    selected = listbox.curselection()
    selected_file = file_var.get()
    if selected and selected_file in file_manager.word_managers:
        word = listbox.get(selected[0])
        file_manager.word_managers[selected_file].remove_word(word)
        update_word_list()

def edit_word():
    selected = listbox.curselection()
    selected_file = file_var.get()
    if selected and selected_file in file_manager.word_managers:
        old_word = listbox.get(selected[0])
        new_word = simpledialog.askstring("Edit Word", f"Replace '{old_word}' with:")
        if new_word:
            file_manager.word_managers[selected_file].edit_word(new_word.strip(), old_word)
            update_word_list()

def add_file():
    name = file_entry.get().strip()
    if name and file_manager.add_file(name):
        refresh_dropdown()
        file_var.set(filename_cleanup(name))
        file_entry.delete(0, tk.END)

def remove_file():
    selected = file_var.get()
    if selected and selected != "--- All Files ---":
        if messagebox.askyesno("Confirm", f"Delete '{selected}' permanently?"):
            file_manager.remove_file(selected)
            refresh_dropdown()
            file_var.set("--- All Files ---")

def rename_file():
    selected = file_var.get()
    if selected and selected != "--- All Files ---":
        new_name = simpledialog.askstring("Rename", f"New name for '{selected}':")
        if new_name and file_manager.rename_file(selected, new_name.strip()):
            refresh_dropdown()
            file_var.set(filename_cleanup(new_name))

# --- UI LAYOUT ---

# 1. Filters
filter_frame = tk.LabelFrame(root, text="View & Filters")
filter_frame.pack(fill="x", padx=10, pady=5)

file_var = tk.StringVar()
file_dropdown = ttk.Combobox(filter_frame, textvariable=file_var, state="readonly")
file_dropdown.grid(row=0, column=0, padx=5, pady=5)
file_var.trace_add("write", update_word_list)

prefix_var = tk.StringVar()
tk.Label(filter_frame, text="Search:").grid(row=0, column=1)
prefix_entry = tk.Entry(filter_frame, textvariable=prefix_var)
prefix_entry.grid(row=0, column=2, padx=5)
prefix_var.trace_add("write", update_word_list)

# 2. Main Word List with Scrollbar
list_frame = tk.Frame(root)
list_frame.pack(padx=10, pady=5, fill="both", expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(list_frame, width=50, height=15, yscrollcommand=scrollbar.set, font=("Courier", 10))
listbox.pack(side="left", fill="both", expand=True)
scrollbar.config(command=listbox.yview)

# 3. Word Management
word_frame = tk.LabelFrame(root, text="Edit Words (Select a File First)")
word_frame.pack(fill="x", padx=10, pady=5)

word_entry = tk.Entry(word_frame)
word_entry.grid(row=0, column=0, padx=5, pady=5)

btn_add_word = tk.Button(word_frame, text="Add", command=add_word)
btn_add_word.grid(row=0, column=1, padx=2)
btn_remove_word = tk.Button(word_frame, text="Remove", command=remove_word)
btn_remove_word.grid(row=0, column=2, padx=2)
btn_edit_word = tk.Button(word_frame, text="Edit", command=edit_word)
btn_edit_word.grid(row=0, column=3, padx=2)

# 4. File Management
file_frame = tk.LabelFrame(root, text="File Management")
file_frame.pack(fill="x", padx=10, pady=5)

file_entry = tk.Entry(file_frame)
file_entry.grid(row=0, column=0, padx=5, pady=5)

tk.Button(file_frame, text="New File", command=add_file).grid(row=0, column=1, padx=2)
tk.Button(file_frame, text="Remove File", command=remove_file).grid(row=0, column=2, padx=2)
tk.Button(file_frame, text="Rename File", command=rename_file).grid(row=0, column=3, padx=2)

# 5. Status Bar (Word Count)
status_var = tk.StringVar()
status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Startup
refresh_dropdown()
file_var.set("--- All Files ---") 

# Exit Logic
def on_closing():
    file_manager.save_all()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()