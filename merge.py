import os

# Quell- und Zielverzeichnisse definieren
SRC_DIR = "src"
ROOT_FILE = "main.py"
OUTPUT_FILE = "temp/merged.py"

# Funktion zum Zusammenführen aller Python-Dateien
def merge_files(src_dir, root_file, output_file):
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Das Verzeichnis {src_dir} existiert nicht.")

    if not os.path.exists(root_file):
        raise FileNotFoundError(f"Die Datei {root_file} existiert nicht.")

    # Sicherstellen, dass der Zielordner existiert
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as merged_file:
        # Zuerst die Dateien aus dem src-Verzeichnis
        for root, _, files in os.walk(src_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        merged_file.write(f"# Inhalt von {file_path}\n")
                        merged_file.write(f.read())
                        merged_file.write("\n\n")

        # Dann die main.py-Datei
        with open(root_file, "r", encoding="utf-8") as main_file:
            merged_file.write(f"# Inhalt von {root_file}\n")
            merged_file.write(main_file.read())

    print(f"Alle Dateien wurden erfolgreich nach {output_file} zusammengeführt.")

# Skript ausführen
if __name__ == "__main__":
    merge_files(SRC_DIR, ROOT_FILE, OUTPUT_FILE)
