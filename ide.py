
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import sys
import os
import sys
from io import StringIO

class FelixIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Felix IDE")
        self.current_file = None
        
        # Create main menu
        self.create_menu()
        
        # Create main container
        self.main_container = ttk.PanedWindow(root, orient=tk.VERTICAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create editor
        self.editor_frame = ttk.Frame(self.main_container)
        self.editor = scrolledtext.ScrolledText(self.editor_frame, wrap=tk.WORD, width=80, height=20)
        self.editor.pack(fill=tk.BOTH, expand=True)
        
        # Create output window
        self.output_frame = ttk.Frame(self.main_container)
        self.output = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, width=80, height=10, bg='black', fg='white')
        self.output.pack(fill=tk.BOTH, expand=True)
        
        # Add frames to paned window
        self.main_container.add(self.editor_frame)
        self.main_container.add(self.output_frame)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Run menu
        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="Run Program", command=self.run_program)
        menubar.add_cascade(label="Run", menu=run_menu)
        
        self.root.config(menu=menubar)

    def new_file(self):
        self.editor.delete(1.0, tk.END)
        self.current_file = None
        
    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".fx",
            filetypes=[("Felix files", "*.fx"), ("All files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            with open(file_path, 'r') as file:
                content = file.read()
                self.editor.delete(1.0, tk.END)
                self.editor.insert(1.0, content)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                content = self.editor.get(1.0, tk.END)
                file.write(content)
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".fx",
            filetypes=[("Felix files", "*.fx"), ("All files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            self.save_file()

    def run_program(self):
        if not self.current_file:
            response = messagebox.askyesno("Save Required", "You need to save your program before running. Would you like to save now?")
            if response:
                self.save_as()
            else:
                return
                
        if not self.current_file:  # User cancelled save
            return
            
        # Save any unsaved changes
        self.save_file()
            
        # Clear output window
        self.output.delete(1.0, tk.END)
        
        try:
            # Get felix executable path
            felix_exe = "felix.exe" if sys.platform == "win32" else "./felix"
            if getattr(sys, 'frozen', False):
                # If running as bundled exe
                felix_exe = os.path.join(os.path.dirname(sys.executable), felix_exe)
            
            # Run the program using felix executable
            process = subprocess.Popen(
                [felix_exe, self.current_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            output, error = process.communicate()
            
            if error:
                self.output.insert(tk.END, f"Error: {error}\n")
            else:
                self.output.insert(tk.END, output)
        except Exception as e:
            self.output.insert(tk.END, f"Error: {str(e)}\n")
        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)

def main():
    root = tk.Tk()
    ide = FelixIDE(root)
    root.mainloop()

if __name__ == "__main__":
    main()
