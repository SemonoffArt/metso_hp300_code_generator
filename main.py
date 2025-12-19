import tkinter as tk
from tkinter import ttk
import sys
import os

from core.calculator import calculate_engineering_code


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main() -> None:
    """Start the minimal METSO HP300 code generator UI.

    MVP: simple window with input field and a button without calculation logic.
    """
    root = tk.Tk()
    root.title("METSO HP300 Code Generator")
    
    # Set window icon if icon.ico exists
    try:
        icon_path = resource_path("icon.ico")
        root.iconbitmap(icon_path)
    except (tk.TclError, FileNotFoundError):
        pass  # Icon file not found, continue without it

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    main_frame = ttk.Frame(root, padding=16)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=1)

    def validate_code(new_value: str) -> bool:
        """Allow only up to 4 hex characters (0-9, A-F)."""
        if new_value == "":
            return True
        if len(new_value) > 4:
            return False
        for ch in new_value:
            if ch not in "0123456789abcdefABCDEF":
                return False
        return True

    vcmd = (root.register(validate_code), "%P")

    code_label = ttk.Label(main_frame, text="Input hexcode:", font=("TkDefaultFont", 16))
    code_label.grid(row=0, column=0, sticky="w")

    code_var = tk.StringVar()
    code_entry = ttk.Entry(main_frame, textvariable=code_var, width=30, validate="key", validatecommand=vcmd, font=("TkDefaultFont", 20))
    code_entry.grid(row=1, column=0, sticky="ew")
    # Bind Enter key to trigger calculation
    code_entry.bind("<Return>", lambda event: on_generate())

    result_label = ttk.Label(main_frame, text="Result:", font=("TkDefaultFont", 16))
    result_label.grid(row=2, column=0, sticky="w", pady=(16, 0))

    result_var = tk.StringVar(value="")
    # Use tk.Entry instead of ttk.Entry for better readonly text selection
    result_entry = tk.Entry(main_frame, textvariable=result_var, width=30, state="readonly", 
                            font=("TkDefaultFont", 20), readonlybackground="white", 
                            relief="solid", borderwidth=1)
    result_entry.grid(row=3, column=0, sticky="ew")

    def on_generate() -> None:
        """Handle Generate button: validate input, run algorithm, show result."""
        raw_code = code_var.get().strip().upper()

        if len(raw_code) != 4:
            result_var.set("Unlock code length 4 digit!")
            return

        try:
            engineering_code = calculate_engineering_code(raw_code)
        except ValueError:
            result_var.set("Invalid unlock code!")
            return

        result_var.set(engineering_code)

    generate_button = ttk.Button(main_frame, text="Convert", command=on_generate)
    generate_button.config(width=10)
    # Apply custom style with larger font and padding for button height
    style = ttk.Style()
    style.configure('Large.TButton', font=('TkDefaultFont', 16), padding=(0, 5))
    generate_button.configure(style='Large.TButton')
    generate_button.grid(row=4, column=0, pady=(8, 0), sticky="e")

    code_entry.focus_set()

    root.mainloop()


if __name__ == "__main__":
    main()
