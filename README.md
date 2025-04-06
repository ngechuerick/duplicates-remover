
# 🧹 Duplicates File Remover

A Python-based desktop GUI application that scans a selected folder for duplicate **files and images** using hashing techniques. The app not only detects but also allows users to safely delete duplicate files with a clear log of what's removed.


## 🔍 Features

- ✅ Detects duplicate **images** using perceptual hashing (`imagehash`)
- ✅ Detects duplicate **files** using MD5 checksum
- ✅ Supports popular image formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.tiff`
- ✅ Easy-to-use **graphical interface** built with `Tkinter`
- ✅ Visual **progress bars** with `tqdm` for scanning and deleting
- ✅ Option to **review duplicates** before deletion
- ✅ Generates a **log file** (`deleted_files_log.txt`) of deleted files for safety



## Installation

Install my-project with npm

```bash
  pip install pillow imagehash tqdm
```
    
## Run Locally

Clone the project

```bash
  git clone https://github.com/ngechuerick/duplicates-remover
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
pip install pillow imagehash tqdm
```

Run on your machine

```bash
python duplicate_cleaner.py
```

## ⚠ Disclaimer
- Use with care! While the app retains one copy of each duplicate, always backup important files before bulk deletion.
- This tool is designed for **local** use and does not upload or share your data.

## 📌 Future improvements (ideas)
- Add support for customizable hash sensitivity
- Support for duplicate music/video detection
- Dark mode UI
- Drag and drop folder selection

## 💻 Author
- Built with ♥ and Python by Ngechu