import tkinter as tk

root = tk.Tk()

entry = tk.Entry(root, state='readonly')
entry.pack()

def update_entry():
    entry.config(state='normal')           # временно делаем поле редактируемым
    entry.delete(0, 'end')                 # очищаем старое
    entry.insert(0, "Новый текст")         # вставляем новый
    entry.config(state='readonly')         # снова запрещаем редактирование

btn = tk.Button(root, text="Обновить", command=update_entry)
btn.pack()

root.mainloop()
