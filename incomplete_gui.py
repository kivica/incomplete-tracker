import tkinter as tk
import webbrowser
import json
import os

FILE_NAME = "incomplete_data.json"

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def open_link(url):
    if url:
        webbrowser.open(url)

def edit_site(index):
    def save_edit():
        data[index]["name"] = name_var.get()
        data[index]["url"] = url_var.get()
        save_data(data)
        update_ui()
        edit_window.destroy()

    edit_window = tk.Toplevel(root)
    edit_window.title("사이트 수정")
    tk.Label(edit_window, text="이름:").grid(row=0, column=0)
    name_var = tk.StringVar(value=data[index]["name"])
    tk.Entry(edit_window, textvariable=name_var).grid(row=0, column=1)

    tk.Label(edit_window, text="URL:").grid(row=1, column=0)
    url_var = tk.StringVar(value=data[index]["url"])
    tk.Entry(edit_window, textvariable=url_var).grid(row=1, column=1)

    tk.Button(edit_window, text="저장", command=save_edit).grid(row=2, columnspan=2)

def delete_site(index):
    del data[index]
    save_data(data)
    update_ui()

def add_site():
    def save_new():
        new_site = {
            "name": name_var.get(),
            "url": url_var.get()
        }
        data.append(new_site)
        save_data(data)
        update_ui()
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("사이트 추가")
    tk.Label(add_window, text="이름:").grid(row=0, column=0)
    name_var = tk.StringVar()
    tk.Entry(add_window, textvariable=name_var).grid(row=0, column=1)

    tk.Label(add_window, text="URL:").grid(row=1, column=0)
    url_var = tk.StringVar()
    tk.Entry(add_window, textvariable=url_var).grid(row=1, column=1)

    tk.Button(add_window, text="추가", command=save_new).grid(row=2, columnspan=2)

def update_ui():
    for widget in frame.winfo_children():
        widget.destroy()

    col = 0
    row = 0
    max_row = 20  # 세로 최대 줄 수

    for idx, item in enumerate(data):
        col_frame = tk.Frame(frame)
        col_frame.grid(row=row, column=col, padx=10, pady=3, sticky="w")

        tk.Label(col_frame, text=item["name"], width=20, anchor="w").pack(side="left")
        tk.Button(col_frame, text="접속", command=lambda i=idx: open_link(data[i].get("url", ""))).pack(side="left")
        tk.Button(col_frame, text="수정", command=lambda i=idx: edit_site(i)).pack(side="left")
        tk.Button(col_frame, text="삭제", command=lambda i=idx: delete_site(i)).pack(side="left")

        row += 1
        if row >= max_row:
            row = 0
            col += 1

# 실행
data = load_data()
root = tk.Tk()
root.title("테스트넷 웹사이트")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

update_ui()

bottom = tk.Frame(root)
bottom.pack(pady=10)
tk.Button(bottom, text="➕ 사이트 추가", command=add_site, bg="#d0f0c0").pack()

root.mainloop()
