import os
import tarfile
from pathlib import Path

def folder_not_empty(path) -> bool:
    if len(os.listdir(path)) != 0:
        return True
    return False

def extract_tar(file_path, destination_dir):
    file_name, file_ext = os.path.splitext(Path(file_path).name)
    path = destination_dir / file_name
    if path.exists() and folder_not_empty(path):
        print("There is data in preferred directory", path)
        return path

    with tarfile.open(file_path, 'r:gz') as tar:
        tar.extractall(path=destination_dir, filter="data")
        print(file_path, 'extracted to', path)
        return path

def delete_file(file_path):
    os.remove(file_path)
    print(file_path, "removed")