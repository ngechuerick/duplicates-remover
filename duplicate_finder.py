import os
import hashlib
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import imagehash
from tqdm import tqdm
import time

IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')


def is_image(file_path):
    return file_path.lower().endswith(IMAGE_EXTS)


def hash_image(file_path):
    try:
        with Image.open(file_path) as img:
            return str(imagehash.average_hash(img))
    except Exception as e:
        print(f"[ImageHash Error] {file_path}: {e}")
        return None


def hash_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            hasher = hashlib.md5()
            while chunk := f.read(4096):
                hasher.update(chunk)
            return hasher.hexdigest()
    except Exception as e:
        print(f"[FileHash Error] {file_path}: {e}")
        return None


def find_duplicates(folder, check_images=True):
    hash_map = {}
    duplicates = []

    all_files = []
    for dirpath, _, filenames in os.walk(folder):
        for fname in filenames:
            path = os.path.join(dirpath, fname)
            all_files.append(path)

    with tqdm(total=len(all_files), desc="Scanning files") as pbar:
        for file_path in all_files:
            hash_val = hash_image(file_path) if check_images and is_image(file_path) else hash_file(file_path)

            if hash_val is None:
                pbar.update(1)
                continue

            if hash_val in hash_map:
                duplicates.append((hash_val, hash_map[hash_val] + [file_path]))
            else:
                hash_map[hash_val] = [file_path]

            pbar.update(1)

    return duplicates


def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        scan_duplicates(folder)


def scan_duplicates(folder):
    duplicates = find_duplicates(folder)
    display_duplicates(duplicates)


def display_duplicates(duplicates):
    results.delete(1.0, END)

    if not duplicates:
        messagebox.showinfo("No Duplicates", "No duplicates found.")
        return

    for idx, (hash_val, files) in enumerate(duplicates, start=1):
        results.insert(END, f"\nGroup {idx} (Hash: {hash_val}):\n")
        for file in files:
            results.insert(END, f"  - {file}\n")

    delete_button.config(state=NORMAL)


def delete_duplicates():
    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete duplicates?")
    if not confirm:
        return

    folder = filedialog.askdirectory()
    duplicates = find_duplicates(folder)

    deleted = []
    with tqdm(total=len(duplicates), desc="Deleting files") as pbar:
        for _, files in duplicates:
            for file in files[1:]:  # keep one
                try:
                    os.remove(file)
                    deleted.append(file)
                except Exception as e:
                    print(f"Failed to delete {file}: {e}")
                pbar.update(1)

    if deleted:
        with open("deleted_files_log.txt", "w") as log:
            for file in deleted:
                log.write(file + "\n")
        messagebox.showinfo("Done", f"{len(deleted)} duplicate files deleted.")
        display_deleted_files(deleted)


def display_deleted_files(deleted_files):
    window = Toplevel(root)
    window.title("Deleted Files")

    box = Listbox(window, width=80, height=15)
    box.pack(pady=10)
    for file in deleted_files:
        box.insert(END, file)


# GUI Setup
root = Tk()
root.title("Duplicate File & Image Cleaner")
root.geometry("700x500")

Button(root, text="Browse Folder", command=browse_folder).pack(pady=10)

results = Text(root, width=80, height=20)
results.pack(pady=10)

delete_button = Button(root, text="Delete Duplicates", command=delete_duplicates, state=DISABLED)
delete_button.pack(pady=10)

root.mainloop()
