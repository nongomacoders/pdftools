import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    from PyPDF2 import PdfReader, PdfWriter


def select_input_file():
    path = filedialog.askopenfilename(
        title="Select PDF file",
        filetypes=[("PDF files", "*.pdf")],
    )
    if path:
        input_var.set(path)
        try:
            reader = PdfReader(path)
            total = len(reader.pages)
            page_info_label.config(text=f"Total pages: {total}")
            start_spin.config(to=total)
            end_spin.config(to=total)
            start_var.set(1)
            end_var.set(total)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read PDF:\n{e}")


def select_output_file():
    input_path = input_var.get()
    initial_name = ""
    if input_path:
        base = os.path.splitext(os.path.basename(input_path))[0]
        initial_name = f"{base}_extracted.pdf"

    path = filedialog.asksaveasfilename(
        title="Save extracted PDF as",
        defaultextension=".pdf",
        initialfile=initial_name,
        filetypes=[("PDF files", "*.pdf")],
    )
    if path:
        output_var.set(path)


def extract():
    input_path = input_var.get().strip()
    output_path = output_var.get().strip()

    if not input_path:
        messagebox.showwarning("Missing input", "Please select an input PDF file.")
        return
    if not output_path:
        messagebox.showwarning("Missing output", "Please specify an output file path.")
        return

    try:
        start = int(start_var.get())
        end = int(end_var.get())
    except ValueError:
        messagebox.showerror("Invalid range", "Page numbers must be integers.")
        return

    try:
        reader = PdfReader(input_path)
        total = len(reader.pages)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read PDF:\n{e}")
        return

    if start < 1 or end < 1 or start > end or end > total:
        messagebox.showerror(
            "Invalid range",
            f"Page range must be between 1 and {total}, with start ≤ end.",
        )
        return

    try:
        writer = PdfWriter()
        for i in range(start - 1, end):
            writer.add_page(reader.pages[i])
        with open(output_path, "wb") as f:
            writer.write(f)
        messagebox.showinfo(
            "Done",
            f"Extracted pages {start}–{end} ({end - start + 1} page(s))\nSaved to:\n{output_path}",
        )
    except Exception as e:
        messagebox.showerror("Error", f"Extraction failed:\n{e}")


def rotate_180():
    input_path = input_var.get().strip()
    output_path = output_var.get().strip()

    if not input_path:
        messagebox.showwarning("Missing input", "Please select an input PDF file.")
        return
    if not output_path:
        messagebox.showwarning("Missing output", "Please specify an output file path.")
        return

    try:
        start = int(start_var.get())
        end = int(end_var.get())
    except ValueError:
        messagebox.showerror("Invalid range", "Page numbers must be integers.")
        return

    try:
        reader = PdfReader(input_path)
        total = len(reader.pages)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read PDF:\n{e}")
        return

    if start < 1 or end < 1 or start > end or end > total:
        messagebox.showerror(
            "Invalid range",
            f"Page range must be between 1 and {total}, with start \u2264 end.",
        )
        return

    try:
        writer = PdfWriter()
        for i in range(start - 1, end):
            page = reader.pages[i]
            page.rotate(180)
            writer.add_page(page)
        with open(output_path, "wb") as f:
            writer.write(f)
        messagebox.showinfo(
            "Done",
            f"Rotated pages {start}\u2013{end} 180\u00b0 ({end - start + 1} page(s))\nSaved to:\n{output_path}",
        )
    except Exception as e:
        messagebox.showerror("Error", f"Rotation failed:\n{e}")


# ── Window ──────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("PDF Page Extractor")
root.resizable(False, False)

PAD = {"padx": 10, "pady": 6}

frame = ttk.Frame(root, padding=16)
frame.grid(row=0, column=0, sticky="nsew")

# ── Input file ───────────────────────────────────────────────────────────────
ttk.Label(frame, text="Input PDF:").grid(row=0, column=0, sticky="w", **PAD)
input_var = tk.StringVar()
ttk.Entry(frame, textvariable=input_var, width=48).grid(row=0, column=1, sticky="ew", **PAD)
ttk.Button(frame, text="Browse…", command=select_input_file).grid(row=0, column=2, **PAD)

page_info_label = ttk.Label(frame, text="Total pages: —", foreground="gray")
page_info_label.grid(row=1, column=1, sticky="w", padx=10)

# ── Page range ───────────────────────────────────────────────────────────────
range_frame = ttk.LabelFrame(frame, text="Page range", padding=8)
range_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=8)

start_var = tk.IntVar(value=1)
end_var = tk.IntVar(value=1)

ttk.Label(range_frame, text="From page:").grid(row=0, column=0, sticky="w", padx=6)
start_spin = ttk.Spinbox(range_frame, from_=1, to=9999, textvariable=start_var, width=8)
start_spin.grid(row=0, column=1, padx=6)

ttk.Label(range_frame, text="To page:").grid(row=0, column=2, sticky="w", padx=6)
end_spin = ttk.Spinbox(range_frame, from_=1, to=9999, textvariable=end_var, width=8)
end_spin.grid(row=0, column=3, padx=6)

# ── Output file ──────────────────────────────────────────────────────────────
ttk.Label(frame, text="Output PDF:").grid(row=3, column=0, sticky="w", **PAD)
output_var = tk.StringVar()
ttk.Entry(frame, textvariable=output_var, width=48).grid(row=3, column=1, sticky="ew", **PAD)
ttk.Button(frame, text="Browse…", command=select_output_file).grid(row=3, column=2, **PAD)

# ── Action buttons ───────────────────────────────────────────────────────────
btn_frame = ttk.Frame(frame)
btn_frame.grid(row=4, column=0, columnspan=3, pady=(12, 4))

ttk.Button(btn_frame, text="Extract Pages", command=extract).grid(row=0, column=0, padx=6)
ttk.Button(btn_frame, text="Rotate 180°", command=rotate_180).grid(row=0, column=1, padx=6)

root.mainloop()
