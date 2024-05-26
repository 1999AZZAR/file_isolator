import os
from tkinter import filedialog, Tk, Button, Label, Entry, StringVar, OptionMenu

def isolate_duplicate_files(source_folder, num_chars, direction, target_folder_name="Isolated"):
    """
    This function isolates files with the same prefix (excluding the specified number of characters)
    within a folder and its subfolders, moving them to a new folder named "Isolated".

    Args:
        source_folder: Path to the folder containing the files to organize.
        num_chars: Number of characters to exclude.
        direction: Direction to exclude characters from ('front' or 'back').
        target_folder_name: Name of the folder to create for isolated files (defaults to "Isolated").
    """
    print(f"Source folder: {source_folder}")
    print(f"Number of characters to exclude: {num_chars}")
    print(f"Direction: {direction}")

    def process_directory(directory_path):
        isolated_folder_path = os.path.join(directory_path, target_folder_name)

        # Create the "Isolated" folder if it doesn't exist
        if not os.path.exists(isolated_folder_path):
            os.makedirs(isolated_folder_path)
            print(f"Created isolated folder: {isolated_folder_path}")

        seen_filenames = {}

        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)

            # Skip the isolated folder to prevent infinite recursion
            if item == target_folder_name:
                print(f"Skipping isolated folder: {item_path}")
                continue

            if os.path.isdir(item_path):
                print(f"Recursively processing directory: {item_path}")
                process_directory(item_path)
                continue

            # Extract filename and extension
            base_name, ext = os.path.splitext(item)

            # Skip hidden files
            if base_name.startswith('.'):
                print(f"Skipping hidden file: {item_path}")
                continue

            # Get the common prefix of the filename based on the specified criteria
            if direction == 'back':
                common_name = base_name[:-num_chars] if len(base_name) > num_chars else ''
            elif direction == 'front':
                common_name = base_name[num_chars:]

            print(f"Processing file: {item}")
            print(f"Common name: {common_name}")

            # Check if the common name has already been seen
            if common_name in seen_filenames:
                # Move the file to the "Isolated" folder
                destination_file = os.path.join(isolated_folder_path, item)
                os.rename(item_path, destination_file)
                print(f"Moved file {item} to {isolated_folder_path}")
            else:
                # Add the common name to the set of seen filenames
                seen_filenames[common_name] = item
                print(f"Added {common_name} to seen filenames")

    # Start processing from the source folder
    process_directory(source_folder)

def browse_source_folder():
    global source_folder_path
    # Open file dialog to select source folder
    source_folder_path = filedialog.askdirectory(title="Select Source Folder")
    # Update label text with selected folder path
    source_folder_label.config(text=f"Selected Folder: {source_folder_path}")

def isolate_duplicates():
    if not source_folder_path:
        # Show error message if no folder selected
        message_label.config(text="Please select a source folder first!", fg="red")
        return

    try:
        num_chars = int(num_chars_var.get())
        if num_chars < 0:
            raise ValueError
    except ValueError:
        message_label.config(text="Please enter a valid number of characters to exclude!", fg="red")
        return

    direction = direction_var.get()

    # Call isolate_duplicate_files function with selected path and user inputs
    isolate_duplicate_files(source_folder_path, num_chars, direction)
    message_label.config(text="Duplicate files isolated successfully!", fg="green")

# Initialize main window
root = Tk()
root.title("Duplicate File Isolator")

# Label for selected folder path
source_folder_label = Label(root, text="Selected Folder: None")
source_folder_label.pack(pady=10)

# Button to browse source folder
browse_button = Button(root, text="Browse Source Folder", command=browse_source_folder)
browse_button.pack(pady=5)

# Entry for number of characters to exclude
num_chars_label = Label(root, text="Number of characters to exclude:")
num_chars_label.pack(pady=5)
num_chars_var = StringVar()
num_chars_entry = Entry(root, textvariable=num_chars_var)
num_chars_entry.pack(pady=5)

# Dropdown for direction to exclude characters from
direction_label = Label(root, text="Direction to exclude characters from:")
direction_label.pack(pady=5)
direction_var = StringVar(root)
direction_var.set("back")  # default value
direction_menu = OptionMenu(root, direction_var, "back", "front")
direction_menu.pack(pady=5)

# Button to isolate duplicates
isolate_button = Button(root, text="Isolate Duplicates", command=isolate_duplicates)
isolate_button.pack(pady=5)

# Label for messages (success or error)
message_label = Label(root, text="")
message_label.pack(pady=10)

# Global variable to store selected source folder path
source_folder_path = ""

# Run the main loop
root.mainloop()
