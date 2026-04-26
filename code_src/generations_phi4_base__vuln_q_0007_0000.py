import os
import shutil

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def copy_file(source, destination):
    shutil.copy(source, destination)

def delete_file(file_path):
    os.remove(file_path)

def change_permissions(file_path, permissions):
    os.chmod(file_path, permissions)

def main():
    directory = "/path/to/shared/directory"
    source_file = "/path/to/source/file.txt"
    destination_file = "/path/to/destination/file.txt"
    file_to_delete = "/path/to/file/to/delete.txt"
    permissions = 0o755  # Example permissions: read, write, execute for owner, read and execute for group and others

    create_directory(directory)
    copy_file(source_file, destination_file)
    delete_file(file_to_delete)
    change_permissions(destination_file, permissions)

if __name__ == "__main__":
    main()