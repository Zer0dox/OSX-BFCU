import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import stat
import mimetypes


def find_large_files(directory, min_size_mb):
    large_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                file_size = os.path.getsize(filepath)
                if file_size > min_size_mb * 1024 * 1024:
                    file_info = {
                        'filename': file,
                        'path': filepath,
                        'size': file_size,
                        'permissions': stat.filemode(os.stat(filepath).st_mode),
                        'type': mimetypes.guess_type(filepath)[0] or 'Unknown'
                    }
                    large_files.append(file_info)
            except OSError:
                continue
    return sorted(large_files, key=lambda x: x['size'], reverse=True)


def shred_file(file_path, chunk_size=1024 * 1024):  # Default chunk size is 1 MB
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)

        with open(file_path, "ba+") as file:
            for _ in range(3):  # Overwrite 3 times for a basic level of security
                file.seek(0)
                chunks = file_size // chunk_size + 1
                for _ in range(chunks):
                    file.write(os.urandom(min(chunk_size, file_size)))
                    file_size -= chunk_size
                    if file_size <= 0:
                        break

        os.remove(file_path)


def search_files():
    directory = filedialog.askdirectory()
    if not directory:
        return
    min_size_mb = simpledialog.askfloat("Input", "Enter the minimum file size in MB:", minvalue=0.1, maxvalue=10000)
    if min_size_mb is None:
        return

    large_files = find_large_files(directory, min_size_mb)
    for file in large_files:
        frame = tk.Frame(window)
        frame.pack()

        label = tk.Label(frame, text=f"{file['filename']} ({file['size']} bytes)")
        label.pack(side=tk.LEFT)

        delete_button = tk.Button(frame, text="Delete", command=lambda f=file['path']: shred_file_and_update(f, frame))
        delete_button.pack(side=tk.RIGHT)


def shred_file_and_update(file_path, frame):
    shred_file(file_path)
    frame.pack_forget()
    messagebox.showinfo("Info", f"File {os.path.basename(file_path)} has been shredded.")


window = tk.Tk()
window.title("File Shredder")

search_button = tk.Button(window, text="Search Files", command=search_files)
search_button.pack()

window.mainloop()
