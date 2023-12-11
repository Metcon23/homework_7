import os
import shutil
import sys
from pathlib import Path

#create new folder for sort 
def create_directories(sort_folder, categories):
    for category in categories:
        folder_path = os.path.join(sort_folder, category)
        os.makedirs(folder_path, exist_ok=True)

#all folders and files translete name 
def normalize(name):
    transliteration_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': "'", 'ю': 'iu', 'я': 'ia',
    }

    base_name, file_extension = os.path.splitext(name)

    transliterated_name = ''.join(transliteration_dict.get(char, char) for char in base_name)
    normalize_name = ''.join('_' if not char.isalnum() else char for char in transliterated_name)

    return f"{normalize_name}{file_extension}"

# функція переміщення файлів та класифікації
def move_file(source_filepath, destination_folder):
    _, filename = os.path.split(source_filepath)
    destination_path = os.path.join(destination_folder, normalize(filename))
    shutil.move(source_filepath, destination_path)

    file_extension = os.path.splitext(filename)[1].lower()
    if file_extension in {'.jpeg', '.png', '.jpg', '.svg'}:
        category = 'images'
    elif file_extension in {'.avi', '.mp4', '.mov', '.mkv'}:
        category = 'video'
    elif file_extension in {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'}:
        category = 'documents'
    elif file_extension in {'.mp3', '.ogg', '.wav', '.amr'}:
        category = 'audio'
    elif file_extension in {'.zip', '.gz', '.tar'}:
        category = 'archives'
    else:
        category = 'other'
    
    files_by_category[category].append(normalize(filename))

    if category == 'other':
        unknown_extensions.add(file_extension)
    else:
        known_extensions.add(file_extension)

# функція сортування папок
def sort_folder(folder_path):
    categories = ["images", "video", "documents", "audio", "archives", "other"]
    create_directories(folder_path, categories)

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            move_file(file_path, folder_path)

    # Оновлення інформації про файли після переміщення
    updated_files_by_category = {
        'images': [],
        'video': [],
        'documents': [],
        'audio': [],
        'archives': [],
        'other': []
    }
    updated_known_extensions = set()
    updated_unknown_extensions = set()

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_extension = os.path.splitext(filename)[1].lower()

            if file_extension in {'.jpeg', '.png', '.jpg', '.svg'}:
                category = 'images'
            elif file_extension in {'.avi', '.mp4', '.mov', '.mkv'}:
                category = 'video'
            elif file_extension in {'.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'}:
                category = 'documents'
            elif file_extension in {'.mp3', '.ogg', '.wav', '.amr'}:
                category = 'audio'
            elif file_extension in {'.zip', '.gz', '.tar'}:
                category = 'archives'
            else:
                category = 'other'

            updated_files_by_category[category].append(normalize(filename))

            if category == 'other':
                updated_unknown_extensions.add(file_extension)
            else:
                updated_known_extensions.add(file_extension)

    # Вивід інформації про файли після оновлення
    for category, files in updated_files_by_category.items():
        print(f"Files in {category}:")
        for file_path in files:
            print(f"- {file_path}")

    print("\nKnown extension:")
    for ext in updated_known_extensions:
        print(f"- {ext}")

    print("\nUnknown extension:")
    for ext in updated_unknown_extensions:
        print(f"- {ext}")

    # Видалення порожніх папок
    for dirpath, dirnames, _ in os.walk(folder_path, topdown=False):
        for dirname in dirnames:
            current_dir = os.path.join(dirpath, dirname)
            if not os.listdir(current_dir):
                os.rmdir(current_dir)

# Ініціалізація словників та множин
files_by_category = {
    'images': [],
    'video': [],
    'documents': [],
    'audio': [],
    'archives': [],
    'other': []
}

known_extensions = set()
unknown_extensions = set()


def main():
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_to_sort = sys.argv[1]

    if not os.path.isdir(folder_to_sort):
        print(f"{folder_to_sort} is not a directory.")
        sys.exit(1)

    sort_folder(folder_to_sort)
