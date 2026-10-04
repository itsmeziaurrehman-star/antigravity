import os
import tkinter as tk
from tkinter import messagebox

# ==============================================================================
# Modern Password Reset GUI (Pure Python & Tkinter - No External Libraries)
# ==============================================================================

class PasswordResetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Key | Password Reset")
        self.root.geometry("480x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f172a")

        # Determine file path relative to this script
        self.file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "password.txt")
        self.ensure_password_file_exists()

        # State variables for show/hide passwords
        self.show_old = False
        self.show_new = False
        self.show_confirm = False

        # Fonts
        self.font_title = ("Segoe UI", 16, "bold")
        self.font_subtitle = ("Segoe UI", 9)
        self.font_label = ("Segoe UI", 9, "bold")
        self.font_entry = ("Segoe UI", 11)
        self.font_criteria = ("Segoe UI", 9)
        self.font_btn = ("Segoe UI", 10, "bold")

        self.setup_ui()

    def ensure_password_file_exists(self):
        """Ensures password.txt exists with a default password if missing."""
        if not os.path.exists(self.file_name):
            with open(self.file_name, "w", encoding="utf-8") as f:
                f.write("Admin@12345")

    def read_saved_password(self):
        """Reads current password from password.txt."""
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            return ""

    def setup_ui(self):
        # Header Container
        header_frame = tk.Frame(self.root, bg="#0f172a")
        header_frame.pack(fill="x", padx=30, pady=(20, 10))

        # Badge / Icon
        badge = tk.Label(
            header_frame,
            text="LOCK",
            bg="#312e81",
            fg="#a5b4fc",
            font=("Segoe UI", 8, "bold"),
            padx=10,
            pady=3,
        )
        badge.pack(anchor="w", pady=(0, 6))

        title_lbl = tk.Label(
            header_frame,
            text="Reset Your Password",
            font=self.font_title,
            fg="#f8fafc",
            bg="#0f172a",
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            header_frame,
            text="Enter your old password and choose a strong new one.",
            font=self.font_subtitle,
            fg="#94a3b8",
            bg="#0f172a",
        )
        subtitle_lbl.pack(anchor="w", pady=(3, 0))

        # Main Card Container
        self.card = tk.Frame(self.root, bg="#1e293b", bd=1, relief="solid")
        self.card.configure(highlightbackground="#334155", highlightthickness=1)
        self.card.pack(fill="both", expand=True, padx=25, pady=(5, 15))

        # --- 1. Old Password Field ---
        lbl_old = tk.Label(self.card, text="Current Password", font=self.font_label, fg="#cbd5e1", bg="#1e293b")
        lbl_old.pack(anchor="w", padx=20, pady=(15, 4))

        old_row = tk.Frame(self.card, bg="#0f172a", highlightthickness=1, highlightbackground="#334155")
        old_row.pack(fill="x", padx=20, pady=(0, 10))

        self.entry_old = tk.Entry(
            old_row,
            show="*",
            font=self.font_entry,
            fg="#f8fafc",
            bg="#0f172a",
            insertbackground="#ffffff",
            bd=0,
            relief="flat",
        )
        self.entry_old.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=8)

        self.btn_eye_old = tk.Button(
            old_row,
            text="Show",
            command=self.toggle_old_pass,
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#0f172a",
            activebackground="#0f172a",
            activeforeground="#f8fafc",
            bd=0,
            cursor="hand2",
            padx=8,
        )
        self.btn_eye_old.pack(side="right")

        # --- 2. New Password Field ---
        lbl_new = tk.Label(self.card, text="New Password", font=self.font_label, fg="#cbd5e1", bg="#1e293b")
        lbl_new.pack(anchor="w", padx=20, pady=(4, 4))

        new_row = tk.Frame(self.card, bg="#0f172a", highlightthickness=1, highlightbackground="#334155")
        new_row.pack(fill="x", padx=20, pady=(0, 6))

        self.entry_new = tk.Entry(
            new_row,
            show="*",
            font=self.font_entry,
            fg="#f8fafc",
            bg="#0f172a",
            insertbackground="#ffffff",
            bd=0,
            relief="flat",
        )
        self.entry_new.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=8)
        self.entry_new.bind("<KeyRelease>", self.on_password_change)

        self.btn_eye_new = tk.Button(
            new_row,
            text="Show",
            command=self.toggle_new_pass,
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#0f172a",
            activebackground="#0f172a",
            activeforeground="#f8fafc",
            bd=0,
            cursor="hand2",
            padx=8,
        )
        self.btn_eye_new.pack(side="right")

        # Strength Bar
        bar_frame = tk.Frame(self.card, bg="#1e293b")
        bar_frame.pack(fill="x", padx=20, pady=(0, 8))

        self.meter_canvas = tk.Canvas(bar_frame, height=6, bg="#334155", bd=0, highlightthickness=0)
        self.meter_canvas.pack(side="left", fill="x", expand=True, pady=4)
        self.meter_rect = self.meter_canvas.create_rectangle(0, 0, 0, 6, fill="#ef4444", width=0)

        self.lbl_strength = tk.Label(bar_frame, text="", font=("Segoe UI", 8, "bold"), fg="#64748b", bg="#1e293b", width=8, anchor="e")
        self.lbl_strength.pack(side="right", padx=(8, 0))

        # Checklist of requirements
        req_frame = tk.Frame(self.card, bg="#1e293b")
        req_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.crit_labels = {}
        criteria = [
            ("len", "Greater than 8 characters (> 8)"),
            ("num", "Contains at least one number (0-9)"),
            ("alpha", "Contains at least one alphabet letter"),
            ("upper", "Contains uppercase letter (A-Z)"),
            ("special", "Contains special character (!@#$%^&*...)"),
        ]

        for key, text in criteria:
            lbl = tk.Label(
                req_frame,
                text=f"  [x]  {text}",
                font=self.font_criteria,
                fg="#64748b",
                bg="#1e293b",
                anchor="w",
            )
            lbl.pack(fill="x", pady=1)
            self.crit_labels[key] = (lbl, text)

        # --- 3. Confirm Password Field ---
        lbl_conf = tk.Label(self.card, text="Confirm New Password", font=self.font_label, fg="#cbd5e1", bg="#1e293b")
        lbl_conf.pack(anchor="w", padx=20, pady=(4, 4))

        conf_row = tk.Frame(self.card, bg="#0f172a", highlightthickness=1, highlightbackground="#334155")
        conf_row.pack(fill="x", padx=20, pady=(0, 4))

        self.entry_conf = tk.Entry(
            conf_row,
            show="*",
            font=self.font_entry,
            fg="#f8fafc",
            bg="#0f172a",
            insertbackground="#ffffff",
            bd=0,
            relief="flat",
        )
        self.entry_conf.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=8)
        self.entry_conf.bind("<KeyRelease>", self.on_confirm_change)

        self.btn_eye_conf = tk.Button(
            conf_row,
            text="Show",
            command=self.toggle_conf_pass,
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#0f172a",
            activebackground="#0f172a",
            activeforeground="#f8fafc",
            bd=0,
            cursor="hand2",
            padx=8,
        )
        self.btn_eye_conf.pack(side="right")

        # Match status label
        self.lbl_match = tk.Label(
            self.card,
            text="",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#1e293b",
            anchor="w",
        )
        self.lbl_match.pack(fill="x", padx=20, pady=(0, 10))

        # Status / Feedback Banner
        self.lbl_status = tk.Label(
            self.card,
            text="",
            font=("Segoe UI", 9, "bold"),
            fg="#ffffff",
            bg="#1e293b",
            wraplength=380,
            justify="center",
            pady=2,
        )
        self.lbl_status.pack(fill="x", padx=20, pady=(0, 10))

        # Submit Button
        self.btn_submit = tk.Button(
            self.card,
            text="Update Password",
            command=self.submit_password_reset,
            font=self.font_btn,
            fg="#ffffff",
            bg="#4f46e5",
            activebackground="#4338ca",
            activeforeground="#ffffff",
            bd=0,
            relief="flat",
            cursor="hand2",
            pady=10,
        )
        self.btn_submit.pack(fill="x", padx=20, pady=(5, 15))

    # --- Eye Toggles ---
    def toggle_old_pass(self):
        self.show_old = not self.show_old
        self.entry_old.config(show="" if self.show_old else "*")
        self.btn_eye_old.config(text="Hide" if self.show_old else "Show")

    def toggle_new_pass(self):
        self.show_new = not self.show_new
        self.entry_new.config(show="" if self.show_new else "*")
        self.btn_eye_new.config(text="Hide" if self.show_new else "Show")

    def toggle_conf_pass(self):
        self.show_confirm = not self.show_confirm
        self.entry_conf.config(show="" if self.show_confirm else "*")
        self.btn_eye_conf.config(text="Hide" if self.show_confirm else "Show")

    # --- Live Validation ---
    def validate_rules(self, pwd):
        special_chars = "!@#$%^&*()-_=+[{]};:'\",<.>/?`~|\\ "
        checks = {
            "len": len(pwd) > 8,
            "num": any('0' <= ch <= '9' for ch in pwd),
            "alpha": any(('a' <= ch <= 'z') or ('A' <= ch <= 'Z') for ch in pwd),
            "upper": any('A' <= ch <= 'Z' for ch in pwd),
            "special": any(ch in special_chars for ch in pwd),
        }
        return checks

    def on_password_change(self, event=None):
        pwd = self.entry_new.get()
        checks = self.validate_rules(pwd)

        # Update checklist labels
        for key, passed in checks.items():
            lbl, text = self.crit_labels[key]
            if passed:
                lbl.config(text=f"  [+]  {text}", fg="#10b981")
            else:
                lbl.config(text=f"  [-]  {text}", fg="#64748b")

        # Update Strength Meter
        passed_count = sum(1 for v in checks.values() if v)
        self.root.update_idletasks()
        canvas_width = self.meter_canvas.winfo_width()
        fill_width = int(canvas_width * (passed_count / 5.0))

        colors = ["#ef4444", "#f97316", "#eab308", "#38bdf8", "#10b981"]
        text_labels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        color = colors[max(0, passed_count - 1)] if passed_count > 0 else "#334155"

        self.meter_canvas.coords(self.meter_rect, 0, 0, fill_width, 6)
        self.meter_canvas.itemconfig(self.meter_rect, fill=color)

        if passed_count > 0:
            self.lbl_strength.config(text=text_labels[passed_count - 1], fg=color)
        else:
            self.lbl_strength.config(text="", fg="#64748b")

        # Re-check confirm match
        self.on_confirm_change()

    def on_confirm_change(self, event=None):
        new_pwd = self.entry_new.get()
        conf_pwd = self.entry_conf.get()

        if not conf_pwd:
            self.lbl_match.config(text="", fg="#64748b")
        elif new_pwd == conf_pwd:
            self.lbl_match.config(text="[+] Passwords match", fg="#10b981")
        else:
            self.lbl_match.config(text="[-] Passwords do not match", fg="#ef4444")

    # --- Submit Handler ---
    def submit_password_reset(self):
        old_pwd = self.entry_old.get()
        new_pwd = self.entry_new.get()
        conf_pwd = self.entry_conf.get()

        saved_password = self.read_saved_password()

        # Step 1: Verify Old Password
        if not old_pwd:
            self.show_status("Please enter your current password.", is_error=True)
            return

        if old_pwd != saved_password:
            self.show_status("Current password is incorrect! Access denied.", is_error=True)
            return

        # Step 2: Validate New Password Rules
        checks = self.validate_rules(new_pwd)
        if not all(checks.values()):
            self.show_status("New password does not meet all security requirements.", is_error=True)
            return

        # Step 3: Check confirmation
        if new_pwd != conf_pwd:
            self.show_status("Confirmed password does not match new password.", is_error=True)
            return

        # Step 4: Write to password.txt
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                f.write(new_pwd)

            self.show_status("SUCCESS: Password updated & saved to password.txt!", is_error=False)
            messagebox.showinfo("Success", "Password has been successfully updated and saved to password.txt!")

            # Clear inputs
            self.entry_old.delete(0, tk.END)
            self.entry_new.delete(0, tk.END)
            self.entry_conf.delete(0, tk.END)
            self.on_password_change()
            self.lbl_match.config(text="")
        except Exception as e:
            self.show_status(f"Error saving password: {e}", is_error=True)

    def show_status(self, message, is_error=False):
        color = "#ef4444" if is_error else "#10b981"
        self.lbl_status.config(text=message, fg=color)


def main():
    root = tk.Tk()
    app = PasswordResetApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
