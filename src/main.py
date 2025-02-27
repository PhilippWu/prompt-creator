import sys
import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import copy

print("Starting application...")

# Prüfe, ob die Anwendung als exe (gefroren) läuft.
if getattr(sys, 'frozen', False) or hasattr(sys, '_MEIPASS'):
    # Bei einer gefrorenen (Onefile) Anwendung: 
    # Der Basisordner soll das Verzeichnis der exe sein.
    BASE_DIR = os.path.dirname(sys.executable)
    CONFIG_FILE = os.path.join(BASE_DIR, "Config.json")
    EXCLUDE_FILE = os.path.join(BASE_DIR, "Exclude.json")
else:
    # Lokale Ausführung: Verwende den Ordner "resources"
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    CONFIG_FILE = os.path.join(BASE_DIR, "resources", "Config.json")
    EXCLUDE_FILE = os.path.join(BASE_DIR, "resources", "Exclude.json")

# Default-Konfigurationen
DEFAULT_CONFIG = {"lastProjectPath": BASE_DIR}
DEFAULT_EXCLUDE = {
    "excludedDirectories": [
        ".venv", ".git", ".copier", ".prerun", "node_modules",
        ".vscode", ".idea", "dist", "build", "out", ".pytest_cache",
        ".mypy_cache", "coverage", ".mvn", ".gradle", "target",
        ".vagrant", ".terraform", ".pnpm-store", ".yarn", "img"
    ],
    "excludedFiles": ["appprompt.txt"],
    "excludedPathPatterns": ["frontend/public/assets/images"]
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf8") as f:
            return json.load(f)
    else:
        with open(CONFIG_FILE, "w", encoding="utf8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf8") as f:
        json.dump(config, f, indent=4)

def load_exclude():
    if os.path.exists(EXCLUDE_FILE):
        with open(EXCLUDE_FILE, "r", encoding="utf8") as f:
            return json.load(f)
    else:
        with open(EXCLUDE_FILE, "w", encoding="utf8") as f:
            json.dump(DEFAULT_EXCLUDE, f, indent=4)
        return DEFAULT_EXCLUDE.copy()

def save_exclude(data):
    with open(EXCLUDE_FILE, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)

# ----- Folder Selection Window -----
class FolderSelectionWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Select Project Folder")
        self.root.geometry("400x150+100+100")
        
        tk.Label(self.root, text="Please select the project folder:").pack(pady=5)
        
        self.folder_var = tk.StringVar()
        config_data = load_config()
        default_folder = config_data.get("lastProjectPath", BASE_DIR)
        self.folder_var.set(default_folder)
        
        tk.Entry(self.root, textvariable=self.folder_var, width=40).pack(pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_folder).pack(pady=5)
        tk.Button(self.root, text="OK", command=self.on_ok).pack(pady=5)
        
        self.selected_folder = None

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_var.get())
        if folder:
            self.folder_var.set(folder)

    def on_ok(self):
        folder = self.folder_var.get()
        if folder and os.path.isdir(folder):
            self.selected_folder = folder
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Please select a valid folder.")

    def run(self):
        self.root.mainloop()
        return self.selected_folder

# ----- Main Application Window -----
class MainApp(tk.Tk):
    def __init__(self, project_path):
        super().__init__()
        self.title("Project Structure Generator")
        self.geometry("800x600+100+100")
        self.project_path = project_path

        # Speichere den ausgewählten Ordner in der Konfiguration
        config_data = load_config()
        config_data["lastProjectPath"] = project_path
        save_config(config_data)

        self.exclude_data = load_exclude()
        self.checkbox_states = {}  # True = ausgewählt, False = nicht ausgewählt
        self.item_to_path = {}
        self.item_excluded = {}    # True, wenn in exclude.json enthalten

        # Output mode: "clipboard" oder "clipboard_file"
        self.output_mode = tk.StringVar(value="clipboard")
        self.output_file = os.path.join(self.project_path, "PromptOutput.txt")
        
        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        tk.Label(top_frame, text="Project Folder: " + self.project_path).pack(side=tk.LEFT)
        tk.Button(top_frame, text="Edit Exclude", command=self.edit_exclude).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Generate", command=self.generate_output).pack(side=tk.LEFT, padx=5)
        
        # Radio buttons für Output Mode
        radio_frame = tk.Frame(self)
        radio_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        tk.Label(radio_frame, text="Output Mode:").pack(side=tk.LEFT)
        tk.Radiobutton(radio_frame, text="Clipboard Only", variable=self.output_mode, value="clipboard", command=self.update_output_mode).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(radio_frame, text="Clipboard and File", variable=self.output_mode, value="clipboard_file", command=self.update_output_mode).pack(side=tk.LEFT, padx=5)
        
        # Frame für den Output-Dateipfad (nur bei "Clipboard and File")
        self.output_file_frame = tk.Frame(self)
        if self.output_mode.get() == "clipboard_file":
            self.output_file_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.output_file_entry = tk.Entry(self.output_file_frame, width=50)
        self.output_file_entry.insert(0, self.output_file)
        self.output_file_entry.config(state="disabled")
        self.output_file_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(self.output_file_frame, text="Browse", command=self.browse_output_file).pack(side=tk.LEFT, padx=5)
        
        # Treeview: Spalte #0 für den Namen, extra Spalte "check"
        self.tree = ttk.Treeview(self, columns=("check",), show="tree headings")
        self.tree.heading("#0", text="Name")
        self.tree.heading("check", text="Check")
        self.tree.column("#0", width=600)
        self.tree.column("check", width=50, anchor="center")
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tree.bind("<Button-1>", self.on_tree_click)
        
        # Tag-Konfiguration für ausgeschlossene Items (roter Hintergrund)
        self.tree.tag_configure("excluded", background="red")
        
        self.populate_tree()

    def update_output_mode(self):
        if self.output_mode.get() == "clipboard_file":
            self.output_file_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        else:
            self.output_file_frame.forget()

    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=self.project_path,
            initialfile="PromptOutput.txt",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.output_file = file_path
            self.output_file_entry.config(state="normal")
            self.output_file_entry.delete(0, tk.END)
            self.output_file_entry.insert(0, file_path)
            self.output_file_entry.config(state="disabled")

    def is_excluded(self, full_path, name, is_dir):
        rel_path = os.path.relpath(full_path, self.project_path)
        patterns = self.exclude_data.get("excludedPathPatterns", [])
        if any(pat in rel_path for pat in patterns):
            return True
        if is_dir:
            if name in self.exclude_data.get("excludedDirectories", []):
                return True
        else:
            if name in self.exclude_data.get("excludedFiles", []):
                return True
        return False

    def insert_item(self, parent, name, full_path):
        is_dir = os.path.isdir(full_path)
        excluded = self.is_excluded(full_path, name, is_dir)
        checkbox_val = "☐" if excluded else "☑"
        item = self.tree.insert(parent, "end", text=name, values=(checkbox_val,), open=False)
        self.checkbox_states[item] = (False if excluded else True)
        self.item_to_path[item] = full_path
        self.item_excluded[item] = excluded
        if excluded:
            self.tree.item(item, tags=("excluded",))
        return item

    def populate_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.checkbox_states.clear()
        self.item_to_path.clear()
        self.item_excluded.clear()
        root_item = self.insert_item("", os.path.basename(self.project_path), self.project_path)
        self.tree.item(root_item, open=True)
        self._populate_tree_recursive(root_item, self.project_path)

    def _populate_tree_recursive(self, parent, path):
        try:
            entries = sorted(os.listdir(path))
        except Exception as e:
            print("Error reading directory", path, ":", e)
            return
        dirs = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
        files = [entry for entry in entries if not os.path.isdir(os.path.join(path, entry))]
        for d in dirs:
            full_path = os.path.join(path, d)
            item = self.insert_item(parent, d, full_path)
            self.tree.item(item, open=False)
            self._populate_tree_recursive(item, full_path)
        for f in files:
            full_path = os.path.join(path, f)
            self.insert_item(parent, f, full_path)

    def on_tree_click(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if item and column == "#1":
            self.toggle_item(item)

    def toggle_item(self, item):
        current_state = self.checkbox_states.get(item, True)
        new_state = not current_state
        self.checkbox_states[item] = new_state
        new_val = "☑" if new_state else "☐"
        self.tree.set(item, "check", new_val)
        self.recursive_toggle(item, new_state)

    def recursive_toggle(self, parent_item, state):
        for child in self.tree.get_children(parent_item):
            if self.item_excluded.get(child, False):
                continue
            self.checkbox_states[child] = state
            new_val = "☑" if state else "☐"
            self.tree.set(child, "check", new_val)
            self.recursive_toggle(child, state)

    def propagate_excluded_selection(self, item, effective_checkbox):
        for child in self.tree.get_children(item):
            effective_checkbox[child] = True
            self.propagate_excluded_selection(child, effective_checkbox)

    def edit_exclude(self):
        editor = tk.Toplevel(self)
        editor.title("Edit Exclude File")
        editor.geometry("600x400+150+150")
        text_area = tk.Text(editor, width=80, height=20)
        text_area.pack(fill=tk.BOTH, expand=True)
        try:
            with open(EXCLUDE_FILE, "r", encoding="utf8") as f:
                content = f.read()
        except Exception as e:
            print("Error reading EXCLUDE_FILE:", e)
            content = ""
        text_area.insert("1.0", content)
        
        def save_changes():
            new_content = text_area.get("1.0", tk.END)
            try:
                data = json.loads(new_content)
                save_exclude(data)
                self.exclude_data = data
                messagebox.showinfo("Success", "Exclude file saved.")
                self.populate_tree()
            except Exception:
                messagebox.showerror("Error", "Invalid JSON format.")
        
        tk.Button(editor, text="Save", command=save_changes).pack(pady=5)

    def _generate_structure_text(self, item, prefix, effective_checkbox, output_lines):
        if not effective_checkbox.get(item, False):
            return
        name_val = self.tree.item(item, "text")
        output_lines.append(prefix + name_val)
        for idx, child in enumerate(self.tree.get_children(item)):
            connector = "└── " if idx == len(self.tree.get_children(item)) - 1 else "├── "
            self._generate_structure_text(child, prefix + connector, effective_checkbox, output_lines)

    def _generate_file_contents_text(self, item, effective_checkbox, output_lines):
        if not effective_checkbox.get(item, False):
            return
        full_path = self.item_to_path.get(item)
        if full_path and not os.path.isdir(full_path):
            ext = os.path.splitext(full_path)[1].lower()
            text_ext = [".txt", ".md", ".json", ".xml", ".html", ".css", ".js", ".ts",
                        ".jsx", ".tsx", ".py", ".java", ".cs", ".cpp", ".c", ".h",
                        ".sh", ".bat", ".ps1", ".yaml", ".yml", ".toml", ".ini"]
            if ext in text_ext:
                rel_path = os.path.relpath(full_path, self.project_path)
                output_lines.append("--- " + rel_path)
                try:
                    with open(full_path, "r", encoding="utf8") as file_obj:
                        content = file_obj.read()
                        output_lines.append(content)
                except Exception:
                    output_lines.append("ERROR: Could not read file.")
                output_lines.append("")
        for child in self.tree.get_children(item):
            self._generate_file_contents_text(child, effective_checkbox, output_lines)

    def build_output_text(self, show_warning=True):
        effective_checkbox = dict(self.checkbox_states)
        if show_warning:
            selected_excluded = [item for item in self.item_to_path if self.item_excluded.get(item, False) and effective_checkbox.get(item, False)]
            if selected_excluded:
                msg = ("Warning: The following excluded items are selected:\n" +
                       "\n".join([self.item_to_path[item] for item in selected_excluded]) +
                       "\nOutput may contain credentials or be unnecessarily long.\nDo you want to include them?")
                include_excluded = messagebox.askyesno("Warning", msg)
                if include_excluded:
                    for item in selected_excluded:
                        self.propagate_excluded_selection(item, effective_checkbox)
                else:
                    for item in self.item_to_path:
                        if self.item_excluded.get(item, False):
                            effective_checkbox[item] = False
        structure_lines = []
        for item in self.tree.get_children():
            self._generate_structure_text(item, "", effective_checkbox, structure_lines)
        file_lines = []
        for item in self.tree.get_children():
            self._generate_file_contents_text(item, effective_checkbox, file_lines)
        output_lines = []
        output_lines.extend(structure_lines)
        output_lines.append("")
        output_lines.append("-------Content of Files---------")
        output_lines.append("")
        output_lines.extend(file_lines)
        output_lines.append("")
        output_lines.append("### Project Structure from '{}'".format(self.project_path))
        output_lines.append("-----------------------------------")
        return "\n".join(output_lines)

    def generate_output(self):
        output_text = self.build_output_text(show_warning=True)
        self.clipboard_clear()
        self.clipboard_append(output_text)
        if self.output_mode.get() == "clipboard_file":
            try:
                with open(self.output_file, "w", encoding="utf8") as f:
                    f.write(output_text)
                messagebox.showinfo("Success", f"Output saved to '{self.output_file}' and copied to clipboard.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save output: {e}")
        self.show_output_window(output_text)

    def show_output_window(self, output_text):
        self.output_window = tk.Toplevel(self)
        self.output_window.title("Output Text")
        self.output_window.geometry("600x400+150+150")
        refresh_button = tk.Button(self.output_window, text="Refresh Prompt", command=self.refresh_prompt)
        refresh_button.pack(side=tk.TOP, pady=5)
        self.output_text_widget = tk.Text(self.output_window, wrap="word")
        self.output_text_widget.insert("1.0", output_text)
        self.output_text_widget.config(state="disabled")
        self.output_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(self.output_window, command=self.output_text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text_widget.config(yscrollcommand=scrollbar.set)

    def refresh_prompt(self):
        new_output_text = self.build_output_text(show_warning=False)
        self.output_text_widget.config(state="normal")
        self.output_text_widget.delete("1.0", tk.END)
        self.output_text_widget.insert("1.0", new_output_text)
        self.output_text_widget.config(state="disabled")
        self.clipboard_clear()
        self.clipboard_append(new_output_text)
        if self.output_mode.get() == "clipboard_file":
            try:
                with open(self.output_file, "w", encoding="utf8") as f:
                    f.write(new_output_text)
            except Exception as e:
                messagebox.showerror("Error", f"Could not save output: {e}")

if __name__ == "__main__":
    folder_selector = FolderSelectionWindow()
    selected_folder = folder_selector.run()
    
    if selected_folder:
        print("Selected project folder:", selected_folder)
        app = MainApp(selected_folder)
        app.mainloop()
    else:
        print("No valid folder selected. Exiting.")

# TODO Very High - Add Prompt Context Window to extent Promt generation
# TODO High - Uncheck all children when parent Folder is unchecked because of exclude.json
# TODO High - Check all children when parent Folder is checked by user after it was uncheck at start because of exclude.json - but only if the child folder oder File is not explicitly excluded in exclude.json
# TODO Medium - Add Multi-Project support at startup and ability to save current project as a new project
# TODO Low - Hide Console Window when running as exe
# TODO Low - Add a status bar at the bottom of the main window