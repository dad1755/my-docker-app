import streamlit as st
import os
import subprocess
import pandas as pd
import platform
import shutil

# CSV file to store created folder names
CSV_FILE = 'created_folders.csv'

def load_created_folders():
    """Load folder names from a CSV file."""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return df['folder_name'].tolist()  # Return list of folder names
    return []  # Return empty list if file doesn't exist

def save_created_folder(folder_name):
    """Save a new folder name to the CSV file."""
    df = pd.DataFrame({'folder_name': [folder_name]})
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)  # Append to the CSV file
    else:
        df.to_csv(CSV_FILE, index=False)  # Create the CSV file with header

def delete_folder_from_csv(folder_name):
    """Remove a folder name from the CSV file."""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = df[df['folder_name'] != folder_name]  # Remove the folder name
        df.to_csv(CSV_FILE, index=False)  # Save the updated DataFrame back to the CSV file

def create_folder(folder_name):
    """Create a folder if it does not already exist, and save its name to the CSV file if successful."""
    folder_path = os.path.join(os.getcwd(), folder_name)

    # Check if the folder already exists on the filesystem
    if os.path.exists(folder_path):
        st.error(f"Folder '{folder_name}' already exists. Please choose a different name.")
        return False  # Indicate that folder creation was not successful

    try:
        os.makedirs(folder_path)  # Create the folder
        save_created_folder(folder_name)  # Save to CSV if creation is successful
        return True  # Indicate that folder creation was successful
    except Exception as e:
        st.error(f"Error creating folder: {e}")
        return False

def delete_file(file_path):
    """Delete a specified file."""
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        st.error(f"Error deleting file: {e}")
        return False

def delete_folder(folder_path):
    """Delete a specified folder and all its contents."""
    try:
        # Check if the folder exists
        if os.path.exists(folder_path):
            # Remove all contents in the folder
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)  # Delete file
                else:
                    shutil.rmtree(item_path)  # Delete directory and its contents
            os.rmdir(folder_path)  # Remove the empty folder
            return True
        else:
            st.error(f"Folder '{folder_path}' does not exist.")
            return False
    except Exception as e:
        st.error(f"Error deleting folder: {e}")
        return False

def manage_folders():
    """Manage folders and files."""
    st.header("Folder Management")

    # Load existing folders
    created_folders = load_created_folders()

    # Input for new folder name
    new_folder_name = st.text_input("Enter folder name to create:")

    # Button to create a folder
    if st.button("Create Folder"):
        if new_folder_name:
            if create_folder(new_folder_name):  # Call create_folder function
                st.success(f"Folder '{new_folder_name}' created.")
                # Reload created folders from CSV to reflect the new state
                created_folders = load_created_folders()
        else:
            st.error("Please provide a folder name.")

    # Display total created folders
    st.write(f"Total Folders Created: {len(created_folders)}")

    # Select box to manage created folders
    if created_folders:
        selected_folder = st.selectbox("Select a folder to view or manage:", created_folders)

        # Button to open selected folder
        if st.button("Open Folder"):
            folder_full_path = os.path.join(os.getcwd(), selected_folder)
            # Determine the OS and open the folder using the appropriate command
            if platform.system() == "Windows":
                subprocess.Popen(f'explorer "{os.path.realpath(folder_full_path)}"')
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", folder_full_path])
            else:  # Assume Linux
                subprocess.Popen(["xdg-open", folder_full_path])

        st.write(f"Files in {selected_folder}:")
        files = os.listdir(os.path.join(os.getcwd(), selected_folder))  # Get files from the selected folder
        if files:
            for file in files:
                st.write(f"- {file}")

            # Select box for file deletion
            file_to_delete = st.selectbox("Select a file to delete:", files)

            # Button to delete selected file
            if st.button("Delete Selected File"):
                file_path = os.path.join(selected_folder, file_to_delete)
                if delete_file(file_path):
                    st.success(f"File '{file_to_delete}' deleted from '{selected_folder}'.")
                    files.remove(file_to_delete)  # Remove the file from the displayed list after deletion
                    st.rerun()
                else:
                    st.error("Failed to delete the file.")

        else:
            st.write("No files found in this folder.")

        # Input for new file creation
        new_file_name = st.text_input("Enter new file name (with extension):")
        new_file_content = st.text_area("Enter content for the new file:")

        # Button to create a new file
        if st.button("Create File"):
            if new_file_name:
                file_path = os.path.join(selected_folder, new_file_name)
                try:
                    with open(file_path, 'w') as f:
                        f.write(new_file_content or '')  # Write empty string if no content
                    st.success(f"File '{new_file_name}' created in '{selected_folder}'.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error creating file: {e}")
            else:
                st.error("Please provide a file name.")

        # Button to delete the selected folder
        if st.button("Delete Selected Folder"):
            folder_path = os.path.join(os.getcwd(), selected_folder)
            if delete_folder(folder_path):
                delete_folder_from_csv(selected_folder)  # Remove from CSV after successful deletion
                st.success(f"Folder '{selected_folder}' and its contents have been deleted.")
                # Reload created folders from CSV to reflect the new state
                created_folders = load_created_folders()  # Refresh the folder list
                st.rerun()
            else:
                st.error(f"Failed to delete the folder '{selected_folder}'.")

    return created_folders  # Return the created folders

# Call the manage_folders function when the script runs
if __name__ == "__main__":
    manage_folders()
