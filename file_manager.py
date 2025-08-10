import subprocess
import tempfile
import sys
import os
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import QModelIndex # Import QModelIndex for type hinting

class FileManager:
    """
    Manages file operations such as creating new projects/files, opening, saving notes,
    and tracking the unsaved status of the current file.
    """
    def __init__(self, parent, editor, model, tree_view, update_title_callback):
        self.parent = parent  # Reference to the MainWindow instance
        self.editor = editor  # Reference to the QTextEdit (code editor)
        self.model = model    # Reference to the QFileSystemModel
        self.tree_view = tree_view # Reference to the QTreeView
        self.update_title_callback = update_title_callback # Callback to update MainWindow title

        self.file_filter = "C++ Files (*.cpp);;Text Files (*.txt);;All Files (*)"
        self.file_name = "Untitled" # Default file name
        self.file_path = None       # Current file path
        self.is_unsaved = False     # Flag to track unsaved changes

    def _show_message_box(self, title, text, icon=QMessageBox.Information, buttons=QMessageBox.Ok):
        """Helper to show a custom message box instead of alert/confirm."""
        msg_box = QMessageBox(self.parent)
        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(buttons)
        return msg_box.exec()

    def _prompt_save_if_unsaved(self):
        """Prompts the user to save the current file if it has unsaved changes."""
        if self.is_unsaved:
            reply = self._show_message_box(
                "Unsaved Changes",
                "Do you want to save your current file before proceeding?",
                QMessageBox.Warning,
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self.save_note()
            elif reply == QMessageBox.Cancel:
                return False # User cancelled the operation
        return True # No unsaved changes, or user chose to discard/saved

    def new_project(self):
        """
        Handles creating a new project (a new directory with an initial file).
        Prompts the user to save the current file if unsaved.
        """
        if not self._prompt_save_if_unsaved():
            return

        file_path, _ = QFileDialog.getSaveFileName(self.parent, "Create New Project File", "", self.file_filter)
        if not file_path:
            return # User cancelled file dialog

        base_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(base_name)[0]
        base_dir = os.path.dirname(file_path)
        
        # Create a new folder named after the file (without extension) in the chosen directory
        new_folder_path = os.path.join(base_dir, name_without_ext)
        os.makedirs(new_folder_path, exist_ok=True) # Create directory if it doesn't exist

        # Construct the full path for the new file inside the new folder
        full_file_path = os.path.join(new_folder_path, base_name)
        
        try:
            with open(full_file_path, 'w') as f:
                f.write("") # Create an empty file
        except IOError as e:
            self._show_message_box("Error", f"Could not create project file: {e}", QMessageBox.Critical)
            return

        self.editor.setPlainText("") # Clear the editor initially
        self.file_name = base_name
        self.file_path = full_file_path
        self.is_unsaved = False # Set unsaved to False after clearing editor

        # Update the main window title before potentially loading template that triggers textChanged
        self.update_title_callback() 
        
        # Update the file system model to show the new directory
        self.model.setRootPath(new_folder_path)
        self.tree_view.setRootIndex(self.model.index(new_folder_path))
        self.tree_view.expandAll() # Expand the new folder in the tree view
        self._show_message_box("New Project", f"New project '{name_without_ext}' created successfully.", QMessageBox.Information)
        
        try:
            with open("Resources/template.cpp", "r") as template_file:
                content = template_file.read()
        except FileNotFoundError:
            # QMessageBox.warning(createFile, "Error", "template.cpp file not found!")
            content = "" # Default to empty if template not found
        
        # Write the content to the new file AND update editor, then mark as not unsaved
        try:
            with open(self.file_path, "w") as new_file:
                new_file.write(content)
            
            # Load the content into the editor, which will trigger textChanged
            with open(self.file_path, "r") as new_file:
                self.editor.setPlainText(new_file.read())
            
            self.is_unsaved = False # Crucially set to False *after* setPlainText
            self.update_title_callback() # Update title again to remove asterisk if it appeared
        except Exception as e:
            self._show_message_box("Error", f"Could not write to new project file: {e}", QMessageBox.Critical)
            return

    def new_file(self):
        """
        Handles creating a new file within the current project/directory.
        Prompts the user to save the current file if unsaved.
        """
        if not self._prompt_save_if_unsaved():
            return

        # Determine the directory where the new file should be created
        target_dir = None
        if self.file_path:
            # If a file is open, create the new file in the same directory
            target_dir = os.path.dirname(self.file_path)
        else:
            # If no file is open, use the current root of the file system model
            target_dir = self.model.rootPath()
            if not target_dir: # Fallback if root path is not set (shouldn't happen with initial setup)
                target_dir = os.getcwd()

        file_path, _ = QFileDialog.getSaveFileName(self.parent, "Create New File", target_dir, self.file_filter)
        if not file_path:
            return # User cancelled file dialog

        base_name = os.path.basename(file_path)
        
        try:
            with open(file_path, 'w') as f:
                f.write("") # Create an empty file
        except IOError as e:
            self._show_message_box("Error", f"Could not create file: {e}", QMessageBox.Critical)
            return

        self.editor.setPlainText("") # Clear the editor, this triggers textChanged
        self.file_name = base_name
        self.file_path = file_path
        self.is_unsaved = False # Set this to False *after* setPlainText
        self.update_title_callback() # Update the main window title (should now be without asterisk)
        
        # Refresh the tree view to show the new file
        # This is important if the new file is in a directory that's already visible
        self.model.setRootPath(os.path.dirname(file_path)) # Ensure the model is rooted correctly
        self.tree_view.setRootIndex(self.model.index(os.path.dirname(file_path)))
        self.tree_view.expandAll() # Expand the directory to show the new file
        self.tree_view.setCurrentIndex(self.model.index(file_path)) # Select the new file
        self._show_message_box("New File", f"New file '{base_name}' created successfully.", QMessageBox.Information)


    def open_note(self):

        if not self._prompt_save_if_unsaved():
            return
        
        if hasattr(self.parent, 'highlighter'):
            self.parent.highlighter.rehighlight()
        file_path, _ = QFileDialog.getOpenFileName(self.parent, "Open File", "", self.file_filter)
        if file_path:
            self._load_file_into_editor(file_path)

    def open_file_from_tree_view(self, index: QModelIndex):

        file_path = self.model.filePath(index)
        
        # Check if the clicked item is a file and not a directory
        if os.path.isfile(file_path):
            if not self._prompt_save_if_unsaved():
                return # User cancelled opening the new file

            self._load_file_into_editor(file_path)
        else:
            # If it's a directory, expand/collapse it
            if self.tree_view.isExpanded(index):
                self.tree_view.collapse(index)
            else:
                self.tree_view.expand(index)

    def _load_file_into_editor(self, file_path):
        """
        Internal helper to load file content into the editor and update state.
        """
        try:
            with open(file_path, 'r') as f:
                self.editor.setPlainText(f.read()) # Load file content into editor
            self.file_path = file_path
            self.file_name = os.path.basename(file_path)
            self.is_unsaved = False
            self.update_title_callback() # Update the main window title
            
            # Set the tree view root to the directory of the opened file
            dir_path = os.path.dirname(file_path)
            self.model.setRootPath(dir_path)
            self.tree_view.setRootIndex(self.model.index(dir_path))
            self.tree_view.expandAll() # Expand the directory
            
            # Select the opened file in the tree view
            index = self.model.index(file_path)
            self.tree_view.setCurrentIndex(index)
        except IOError as e:
            self._show_message_box("Error", f"Could not open file: {e}", QMessageBox.Critical)


    def save_note(self):
        """
        Saves the current file. If it's a new, unsaved file, it calls save_as_note.
        """
        if self.file_path:
            if self.is_unsaved:
                try:
                    with open(self.file_path, 'w') as f:
                        f.write(self.editor.toPlainText()) # Write editor content to file
                    self.is_unsaved = False
                    self.update_title_callback() # Update the main window title
                    self._show_message_box("Save", f"File '{self.file_name}' saved successfully.", QMessageBox.Information)
                except IOError as e:
                    self._show_message_box("Error", f"Could not save file: {e}", QMessageBox.Critical)
        else:
            # If no file path is set (e.g., brand new "Untitled" file), prompt for "Save As"
            self.save_as_note()

    def save_as_note(self):
        """
        Saves the current file to a new location or with a new name.
        """
        file_path, _ = QFileDialog.getSaveFileName(self.parent, "Save File As", "", self.file_filter)
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.editor.toPlainText()) # Write editor content to new file
                self.file_path = file_path
                self.file_name = os.path.basename(file_path)
                self.is_unsaved = False
                self.update_title_callback() # Update the main window title
                self._show_message_box("Save As", f"File saved as '{self.file_name}' successfully.", QMessageBox.Information)
                
                # Update the file system model to the directory of the new file
                dir_path = os.path.dirname(file_path)
                self.model.setRootPath(dir_path)
                self.tree_view.setRootIndex(self.model.index(dir_path))
                self.tree_view.expandAll()
                
                # Select the saved file in the tree view
                index = self.model.index(file_path)
                self.tree_view.setCurrentIndex(index)

            except IOError as e:
                self._show_message_box("Error", f"Could not save file as: {e}", QMessageBox.Critical)
    
    def load_template(self):
        try:
            with open("Resources/template.cpp", "r") as template_file:
                content = template_file.read()
        except FileNotFoundError:
            #QMessageBox.warning(createFile, "Error", "template.cpp file not found!")
            return
        
        # Write the content to the new file
        try:
            with open(self.file_path, "w") as new_file:
                new_file.write(content)
            # Reopen the file in read mode
            with open(self.file_path, "r") as new_file:
                self.editor.setPlainText(new_file.read())
        
        except Exception as e:
            return
            #QMessageBox.warning(createFile, "Error", f"Failed to create file: {str(e)}")
    
    def save_template(self):
        # Define the path to your template file
        template_file_path = os.path.join("Resources", "template.cpp")

        
        try:
            # Write the content to the file specified by self.file_path (now the template's path)
            with open(template_file_path, "w") as new_file:
                new_file.write(self.editor.toPlainText())
            
        except Exception as e:
            # QMessageBox.warning(self.main_window, "Error", f"Could not open/write to file: {e}")
            print(f"An error occurred while writing to file: {e}")
            return


    def build_code1(self):
        """
        Builds the current C++ file using g++ compiler.
        Shows build output in the build output area.
        """
        if not self.file_path:
            self._show_message_box("Error", "No file is currently open to build.", QMessageBox.Warning)
            return

        # Check if the file has unsaved changes
        if self.is_unsaved:
            reply = self._show_message_box(
                "Unsaved Changes",
                "The file has unsaved changes. Save before building?",
                QMessageBox.Question,
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                self.save_note()
            elif reply == QMessageBox.Cancel:
                return  # User cancelled the build

        # Get the file directory and base name without extension
        file_dir = os.path.dirname(self.file_path)
        file_base = os.path.splitext(os.path.basename(self.file_path))[0]
        output_path = os.path.join(file_dir, file_base)

        # Prepare the build command
        build_cmd = f"g++ \"{self.file_path}\" -o \"{output_path}\""

        try:
            # Execute the build command
            process = subprocess.Popen(
                build_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()

            # Display build output
            output_text = f"> {build_cmd}\n\n"
            if stdout:
                output_text += f"Output:\n{stdout}\n"
            if stderr:
                output_text += f"Errors:\n{stderr}\n"

            # Check if build was successful
            if process.returncode == 0:
                output_text += "\nBuild successful!\n"
                output_text += f"Executable created: {output_path}"
                # CORRECTED: Access build_output through self.parent.bottom_tabs
                self.parent.bottom_tabs.build_output.setPlainText(output_text)
            else:
                output_text += "\nBuild failed!"
                # CORRECTED: Access build_output through self.parent.bottom_tabs
                self.parent.bottom_tabs.build_output.setPlainText(output_text)

        except Exception as e:
            error_msg = f"Error during build: {str(e)}"
            # CORRECTED: Access build_output through self.parent.bottom_tabs
            self.parent.bottom_tabs.build_output.setPlainText(error_msg)



    def build_and_run(self):
        self.build_code1()

        # Check if build was successful (from build_code1's output)
        output_text = self.parent.bottom_tabs.build_output.toPlainText()
        if "Build successful!" not in output_text:
            self.parent.bottom_tabs.build_output.append("\nRun aborted: Build failed.")
            return

        # Get executable path (without .exe extension, as cmd handles it implicitly sometimes)
        # This `file_dir` should be the directory where your .cpp, .in, and .out files are located.
        file_dir = os.path.dirname(self.file_path)
        file_base = os.path.splitext(os.path.basename(self.file_path))[0]
        executable_name = file_base # The name of the executable (e.g., "my_program")

        # --- Let's add some print statements here to confirm the paths Python sees ---
        print(f"DEBUG: self.file_path is: {self.file_path}")
        print(f"DEBUG: Calculated file_dir (project folder) is: {file_dir}")
        print(f"DEBUG: Executable name is: {executable_name}")
        # --- End DEBUG prints ---

        try:
            # Create a temporary batch file
            with tempfile.NamedTemporaryFile(suffix='.bat', mode='w', delete=False) as temp_bat:
                # THIS IS THE CRITICAL PART:
                # We explicitly change the directory inside the batch file
                # to the project folder (`file_dir`) before running the executable.
                batch_content = f"""@echo off
    REM Change directory to where the executable and data files are located
    cd /d "{file_dir}"
    REM Run the executable
    "{executable_name}"
    echo.
    echo Program exited with code %errorlevel%
    pause
    exit
    """
                temp_bat.write(batch_content)
                temp_bat_path = temp_bat.name

            print(f"DEBUG: Temporary batch file created at: {temp_bat_path}")
            print(f"DEBUG: Batch content will be:\n{batch_content}")

            # Run the batch file in a new console window
            subprocess.Popen(
                ['cmd', '/c', 'start', temp_bat_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE # Ensures a new window on Windows
            )

        except Exception as e:
            error_msg = f"Error running program: {str(e)}"
            self.parent.bottom_tabs.build_output.append(error_msg)

    def mark_unsaved(self):
        if not self.is_unsaved: 
            self.is_unsaved = True
            self.update_title_callback() 

    def get_filename_and_status(self):
        return self.file_name, self.is_unsaved
