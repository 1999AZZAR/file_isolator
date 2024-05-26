# Duplicate File Isolator

## Deskripsi Proyek

Duplicate File Isolator adalah sebuah aplikasi GUI yang dibuat dengan Python untuk mengisolasi file duplikat berdasarkan prefiks (mengabaikan sejumlah karakter tertentu) dalam sebuah folder dan subfoldernya. File duplikat akan dipindahkan ke folder baru yang dinamai "Isolated".

## Fitur

- Memilih folder sumber untuk diproses
- Mengatur jumlah karakter yang akan diabaikan
- Memilih arah (depan atau belakang) dari karakter yang akan diabaikan
- Memindahkan file duplikat ke folder "Isolated"

## Persyaratan

Sebelum menjalankan aplikasi ini, pastikan Anda telah menginstal:

- Python 3.x
- Modul `tkinter` (biasanya sudah termasuk dalam instalasi Python standar)

## Cara Menggunakan

### 1. Persiapan

1. **Instal Python 3.x**
   Pastikan Python 3.x terinstal di komputer Anda. Jika belum, unduh dan instal dari [python.org](https://www.python.org/).

2. **Instal Modul yang Dibutuhkan**
   Modul `tkinter` biasanya sudah termasuk dalam instalasi Python standar. Jika karena suatu alasan modul ini tidak ada, Anda bisa menginstalnya menggunakan pip:
   ```bash
   pip install tk
   ```

### 2. Menjalankan Aplikasi

1. **Membuka Terminal atau Command Prompt**
   Buka terminal atau command prompt di komputer Anda.

2. **Navigasi ke Direktori Proyek**
   Pindah ke direktori tempat file `file_isolator.py` berada. Gunakan perintah `cd` untuk berpindah direktori. Misalnya:
   ```bash
   cd path/to/directory
   ```

3. **Menjalankan Skrip Python**
   Jalankan skrip dengan perintah berikut:
   ```bash
   python file_isolator.py
   ```

### 3. Menggunakan Aplikasi

1. **Memilih Folder Sumber**
   Klik tombol "Browse Source Folder" dan pilih folder yang ingin Anda proses.

2. **Mengatur Jumlah Karakter yang Diabaikan**
   Masukkan jumlah karakter yang ingin diabaikan pada kotak teks yang tersedia.

3. **Memilih Arah Karakter yang Diabaikan**
   Pilih apakah karakter yang akan diabaikan berasal dari depan atau belakang nama file dengan menggunakan dropdown menu.

4. **Mengisolasi File Duplikat**
   Klik tombol "Isolate Duplicates" untuk memulai proses. File duplikat akan dipindahkan ke folder baru bernama "Isolated" di dalam folder sumber.

5. **Melihat Pesan Status**
   Pesan status akan ditampilkan di bawah tombol "Isolate Duplicates" untuk memberi tahu apakah proses berhasil atau terjadi kesalahan.

## Kode Sumber

Berikut adalah kode sumber untuk aplikasi Duplicate File Isolator:

```python
import os
from tkinter import filedialog, Tk, Button, Label, Entry, StringVar, OptionMenu

def isolate_duplicate_files(source_folder, num_chars, direction, target_folder_name="Isolated"):
    print(f"Source folder: {source_folder}")
    print(f"Number of characters to exclude: {num_chars}")
    print(f"Direction: {direction}")

    def process_directory(directory_path):
        isolated_folder_path = os.path.join(directory_path, target_folder_name)
        if not os.path.exists(isolated_folder_path):
            os.makedirs(isolated_folder_path)
            print(f"Created isolated folder: {isolated_folder_path}")

        seen_filenames = {}

        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)

            if item == target_folder_name:
                print(f"Skipping isolated folder: {item_path}")
                continue

            if os.path.isdir(item_path):
                print(f"Recursively processing directory: {item_path}")
                process_directory(item_path)
                continue

            base_name, ext = os.path.splitext(item)

            if base_name.startswith('.'):
                print(f"Skipping hidden file: {item_path}")
                continue

            if direction == 'back':
                common_name = base_name[:-num_chars] if len(base_name) > num_chars else ''
            elif direction == 'front':
                common_name = base_name[num_chars:]

            print(f"Processing file: {item}")
            print(f"Common name: {common_name}")

            if common_name in seen_filenames:
                destination_file = os.path.join(isolated_folder_path, item)
                os.rename(item_path, destination_file)
                print(f"Moved file {item} to {isolated_folder_path}")
            else:
                seen_filenames[common_name] = item
                print(f"Added {common_name} to seen filenames")

    process_directory(source_folder)

def browse_source_folder():
    global source_folder_path
    source_folder_path = filedialog.askdirectory(title="Select Source Folder")
    source_folder_label.config(text=f"Selected Folder: {source_folder_path}")

def isolate_duplicates():
    if not source_folder_path:
        message_label.config(text="Please select a source folder first!", fg="red")
        return

    try:
        num_chars = int(num_chars_var.get())
        if num_chars < 0:
            raise ValueError
    except ValueError:
        message_label.config(text="Please enter a valid number of characters to exclude!", fg="red")
        return

    direction = direction_var.get()

    isolate_duplicate_files(source_folder_path, num_chars, direction)
    message_label.config(text="Duplicate files isolated successfully!", fg="green")

root = Tk()
root.title("Duplicate File Isolator")

source_folder_label = Label(root, text="Selected Folder: None")
source_folder_label.pack(pady=10)

browse_button = Button(root, text="Browse Source Folder", command=browse_source_folder)
browse_button.pack(pady=5)

num_chars_label = Label(root, text="Number of characters to exclude:")
num_chars_label.pack(pady=5)
num_chars_var = StringVar()
num_chars_entry = Entry(root, textvariable=num_chars_var)
num_chars_entry.pack(pady=5)

direction_label = Label(root, text="Direction to exclude characters from:")
direction_label.pack(pady=5)
direction_var = StringVar(root)
direction_var.set("back")
direction_menu = OptionMenu(root, direction_var, "back", "front")
direction_menu.pack(pady=5)

isolate_button = Button(root, text="Isolate Duplicates", command=isolate_duplicates)
isolate_button.pack(pady=5)

message_label = Label(root, text="")
message_label.pack(pady=10)

source_folder_path = ""

root.mainloop()
```

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini, silakan fork repository ini dan kirim pull request dengan perubahan atau fitur baru yang ingin Anda tambahkan.
