import os
import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import messagebox
import shutil
import json
import subprocess

selected_project_directory = ""  # Variable to store the selected project directory
selected_directory = ""


def open_directory_dialog():
    global selected_directory

    # Ask the user to select a directory
    selected_directory = filedialog.askdirectory()

    # write work space to project_file
    with open("./project_file.json", "r") as file:
        project_file = json.load(file)
    project_file['work_space'] = selected_directory
    with open("./project_file.json", "w") as file:
        json.dump(project_file, file)

    # Display the selected directory in the label
    label.config(text="work space: " + selected_directory)

    # Update the contents of the Listbox with the selected directory
    update_listbox(selected_directory)


def open_project():
    global selected_project_directory
    selected_project_index = listbox.curselection()

    if selected_project_index:
        selected_project = listbox.get(selected_project_index)
        selected_project_directory = os.path.join(label.cget("text").split(": ")[1], selected_project)

        with open('./project_file.json', 'r') as file:
            l_project_file = json.load(file)

        l_project_file['current_project'] = selected_project_directory

        with open('./project_file.json', 'w') as file:
            json.dump(l_project_file, file)

        subprocess.run(['python', 'main.py'])

    else:
        messagebox.showerror("Error", "Please select a project.")


def create_fzy_file():
    new_fzy_file = os.path.join(selected_directory, "new_project.fzy")
    # Ask the user for the project name
    project_name = simpledialog.askstring("Project Name", "Enter the project name:")
    if project_name is None:
        # User clicked cancel, do not proceed
        return
    os.mkdir(selected_directory + "/" + project_name + ".fzy")
    os.mkdir(selected_directory + "/" + project_name + ".fzy/GameData")
    shutil.copytree('ProjectTemplate/GameData',
                    selected_directory + "/" + project_name + ".fzy/GameData",
                    dirs_exist_ok=True)

    update_listbox(selected_directory)


def update_listbox(directory):
    # Clear the existing items in the Listbox
    listbox.delete(0, tk.END)

    # Get the list of files and subdirectories in the selected directory
    contents = os.listdir(directory)

    # Filter files with the .fzy extension
    fzy_files = [item for item in contents if item.endswith('.fzy')]

    # Display each .fzy file in the Listbox
    for fzy_file in fzy_files:
        listbox.insert(tk.END, fzy_file)


# Create the main Tkinter window
root = tk.Tk()
root.title("Fuzzy Projects")

# Set the dimensions of the window to 600x400
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create a button to trigger the directory dialog
button = tk.Button(root, text="Select WorkSpace", command=open_directory_dialog)
button.pack(side=tk.LEFT, pady=0, padx=20, )

# Create a label to display the selected directory
label = tk.Label(root, text="Workspace: ")
label.pack(anchor=tk.W, padx=20)

# Create a frame to hold the Listbox
frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Create a Listbox to display the contents of the selected directory
listbox = tk.Listbox(frame)
listbox.pack(fill=tk.BOTH, expand=True)

# Create a button to open the selected project
open_project_button = tk.Button(root, text="Open Project", command=open_project)
open_project_button.pack(side=tk.LEFT, pady=20, padx=20)

# Create a button to create a new .fzy file
create_fzy_file_button = tk.Button(root, text="Create .fzy File", command=create_fzy_file)
create_fzy_file_button.pack(side=tk.LEFT, pady=20, padx=20)

# read project_file
with open("./project_file.json", 'r') as file:
    g_project_file = json.load(file)

try:

    update_listbox(g_project_file['work_space'])
    # Display the selected directory in the label
    label.config(text="work space: " + g_project_file['work_space'])
except:
    label.config(text='work_space: None Found')
# Run the Tkinter event loop
root.mainloop()
