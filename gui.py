import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

from database import create_table, insert_record, view_records, delete_record

# -----------------------------
# Data
# -----------------------------
MICROSCOPE_TYPES = {
    "Light Microscope": 40,
    "Electron Microscope": 1000,
    "SEM": 5000,
    "TEM": 10000
}

UNIT_TO_METERS = {
    "nm": 1e-9,
    "um": 1e-6,
    "mm": 1e-3,
    "cm": 1e-2,
    "m": 1
}

# -----------------------------
# App Class
# -----------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Microscope Calculator")

        create_table()

        # Variables
        self.username = tk.StringVar()
        self.measured = tk.StringVar()
        self.microscope = tk.StringVar(value="Light Microscope")
        self.unit = tk.StringVar(value="mm")

        self.image_label = None

        self.build_ui()

    # -------------------------
    def build_ui(self):
        tk.Label(self.root, text="Username").pack()
        tk.Entry(self.root, textvariable=self.username).pack()

        tk.Label(self.root, text="Measured Size").pack()
        tk.Entry(self.root, textvariable=self.measured).pack()

        tk.Label(self.root, text="Microscope Type").pack()
        tk.OptionMenu(self.root, self.microscope, *MICROSCOPE_TYPES.keys()).pack()

        tk.Label(self.root, text="Output Unit").pack()
        tk.OptionMenu(self.root, self.unit, *UNIT_TO_METERS.keys()).pack()

        tk.Button(self.root, text="Upload Image", command=self.upload_image).pack()

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        tk.Button(self.root, text="Calculate", command=self.calculate).pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        tk.Button(self.root, text="View Records", command=self.show_records).pack()
        tk.Button(self.root, text="Delete Record", command=self.delete_record_ui).pack()

    # -------------------------
    def upload_image(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            img = Image.open(file_path)
            img = img.resize((150, 150))
            img = ImageTk.PhotoImage(img)

            self.image_label.configure(image=img)
            self.image_label.image = img

    # -------------------------
    def calculate(self):
        username = self.username.get().strip()

        if not username:
            messagebox.showerror("Error", "Username required")
            return

        try:
            measured = float(self.measured.get())
            if measured <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid measured size")
            return

        microscope = self.microscope.get()
        magnification = MICROSCOPE_TYPES[microscope]
        unit = self.unit.get()

        real_size = measured / magnification
        final_value = real_size / UNIT_TO_METERS[unit]

        self.result_label.config(
            text=f"Real Size: {final_value:.3f} {unit}"
        )

        insert_record(username, measured, real_size)

    # -------------------------
    def show_records(self):
        records = view_records()

        if not records:
            messagebox.showinfo("Info", "No records found")
            return

        text = "\n".join(
            f"ID:{r[0]} | {r[1]} | {r[2]} → {r[3]}"
            for r in records
        )

        messagebox.showinfo("Records", text)

    # -------------------------
    def delete_record_ui(self):
        def delete():
            try:
                rid = int(entry.get())
                delete_record(rid)
                messagebox.showinfo("Success", "Deleted")
                win.destroy()
            except:
                messagebox.showerror("Error", "Invalid ID")

        win = tk.Toplevel(self.root)
        win.title("Delete Record")

        tk.Label(win, text="Enter Record ID").pack()
        entry = tk.Entry(win)
        entry.pack()

        tk.Button(win, text="Delete", command=delete).pack()


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
