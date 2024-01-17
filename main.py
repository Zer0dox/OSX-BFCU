import os
import stat
import mimetypes
import textwrap
import time


def cls():
    time.sleep(1)
    os.system("clear")


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
                        'size': str((round(file_size/1024/1024)))+"MB",
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


def print_file_info_in_box(file_info, box_width=80):
    wrapper = textwrap.TextWrapper(width=box_width - 4)  # 4 characters for '| ' and ' |'

    print("+" + "-" * (box_width - 2) + "+")
    for key, value in file_info.items():
        wrapped_text = wrapper.wrap(f"{key.capitalize()}: {value}")
        for line in wrapped_text:
            print("| " + line.ljust(box_width - 4) + " |")
    print("+" + "-" * (box_width - 2) + "+")


def main():
    directory_to_search = input("Enter the directory to search: ")
    min_size_mb = float(input("Enter the minimum file size in MB: "))
    large_files = find_large_files(directory_to_search, min_size_mb)

    for file in large_files:
        print_file_info_in_box(file)
        user_choice = input("Do you want to delete this file? (yes/no): ").lower()
        if user_choice == 'yes':
            shred_file(file['path'])
            print(f"File {file['filename']} has been shredded.")
            cls()
        else:
            print(f"File {file['filename']} has been kept.")
            cls()


if __name__ == "__main__":
    main()
