import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
import mysql.connector
from mysql.connector import Error

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.insertdanhmuc import insert_danhmuc
from common.deletedanhmuc import delete_danhmuc
from common.updatedanhmuc import update_danhmuc
from common.getdanhmuc import get_all_danhmuc

get_all_danhmuc()
# -------------------------------
root = tk.Tk()
root.title("Quản lý Danh Mục - CRUD MySQL")
root.geometry("700x500")
# Hàm cập nhật danh sách trên Treeview
# -------------------------------
def load_data():
    for i in tree.get_children():
        tree.delete(i)
    data = get_all_danhmuc()
    for row in data:
        tree.insert("", tk.END, values=row)

# -------------------------------
# Hàm thêm danh mục
# -------------------------------
def add_danhmuc():
    ten = entry_ten.get()
    mota = entry_mota.get()
    if ten.strip() == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập tên danh mục!")
        return
    insert_danhmuc(ten, mota)
    load_data()
    entry_ten.delete(0, tk.END)
    entry_mota.delete(0, tk.END)

# -------------------------------
# Hàm xóa danh mục
# -------------------------------
def delete_selected():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn danh mục cần xóa.")
        return
    ma = tree.item(selected)['values'][0]
    confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa danh mục ID {ma}?")
    if confirm:
        delete_danhmuc(ma)
        load_data()

# -------------------------------
# Hàm chọn hàng trong Treeview để sửa
# -------------------------------
def on_select(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected)['values']
        entry_id.delete(0, tk.END)
        entry_id.insert(0, values[0])
        entry_ten.delete(0, tk.END)
        entry_ten.insert(0, values[1])
        entry_mota.delete(0, tk.END)
        entry_mota.insert(0, values[2])

# -------------------------------
# Hàm cập nhật danh mục
# -------------------------------
def update_current():
    ma = entry_id.get()
    ten = entry_ten.get()
    mota = entry_mota.get()
    if ma == "":
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn danh mục để sửa.")
        return
    update_danhmuc(ma, ten, mota)
    load_data()

# --- Frame nhập liệu ---
tk.Label(root, text="QUẢN LÝ DANH MỤC", font=("Arial", 18, "bold"), bg="#F5F7FA", fg="#2E7D32").pack(pady=15)

# --- Khung nhập liệu ---
frame_input = tk.LabelFrame(root, text="Thông tin danh mục", font=("Arial", 11, "bold"), bg="#FFFFFF", padx=10, pady=10)
frame_input.pack(fill="x", padx=15, pady=10)

tk.Label(frame_input, text="Mã Danh Mục:", font=("Arial", 10), bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_id = tk.Entry(frame_input, width=10, state='readonly', font=("Arial", 10))
entry_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Tên Danh Mục:", font=("Arial", 10), bg="#FFFFFF").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_ten = tk.Entry(frame_input, width=30, font=("Arial", 10))
entry_ten.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Mô tả:", font=("Arial", 10), bg="#FFFFFF").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_mota = tk.Entry(frame_input, width=50, font=("Arial", 10))
entry_mota.grid(row=2, column=1, padx=5, pady=5)

# --- Nút chức năng ---
frame_buttons = tk.Frame(root, bg="#F5F7FA")
frame_buttons.pack(pady=10)

btn_add = tk.Button(frame_buttons, text="➕ Thêm", bg="#43A047", fg="white", font=("Arial", 10, "bold"), width=10, command=add_danhmuc)
btn_update = tk.Button(frame_buttons, text="✏️ Sửa", bg="#1E88E5", fg="white", font=("Arial", 10, "bold"), width=10, command=update_current)
btn_delete = tk.Button(frame_buttons, text="🗑️ Xóa", bg="#E53935", fg="white", font=("Arial", 10, "bold"), width=10, command=delete_selected)
btn_reload = tk.Button(frame_buttons, text="🔄 Tải lại", bg="#757575", fg="white", font=("Arial", 10, "bold"), width=10, command=load_data)

btn_add.grid(row=0, column=0, padx=8)
btn_update.grid(row=0, column=1, padx=8)
btn_delete.grid(row=0, column=2, padx=8)
btn_reload.grid(row=0, column=3, padx=8)

# --- Bảng hiển thị ---
columns = ("Mã", "Tên Danh Mục", "Mô tả")
tree_frame = tk.Frame(root, bg="#FFFFFF")
tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set)
tree_scroll.config(command=tree.yview)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200 if col != "Mô tả" else 300)

tree.pack(fill="both", expand=True)
tree.bind("<ButtonRelease-1>", on_select)

# --- Tải dữ liệu ban đầu ---
load_data()

root.mainloop()