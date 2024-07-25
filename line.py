import os

directory = "/Users/lavoro/Documents/PROGETTI_LAVORO/Romaco_4/05_software/Romaco_APP/"
directory_depth = 100  # How deep you would like to go
extensions_to_consider = [".py", ".css"]  # Change to ["all"] to include all extensions
exclude_filenames = [".venv", ".idea", "__pycache__", "cache"]
skip_file_error_list = True

this_file_dir = os.path.realpath(__file__)

print("Path to ignore:", this_file_dir)
print("-------------------------------------------------")

def _walk(path, depth):
    """Recursively list files and directories up to a certain depth"""
    depth -= 1
    with os.scandir(path) as p:
        for entry in p:

            skip_entry = False
            for fName in exclude_filenames:
                if entry.path.endswith(fName):
                    skip_entry = True
                    break

            if skip_entry:
                print("Skipping entry", entry.path)
                continue

            yield entry.path
            if entry.is_dir() and depth > 0:
                yield from _walk(entry.path, depth)

print("Caching entries")
files = list(_walk(directory, directory_depth))
print("\n\n |==================================================================================================|")

print(f" |{'Counting Lines':>45} \t{' ':>44}|")
file_err_list = []
line_count = 0
len_files = len(files)
for i, file_dir in enumerate(files):

    if not os.path.isfile(file_dir):
        continue

    skip_File = True
    for ending in extensions_to_consider:
        if file_dir.endswith(ending) or ending == "all":
            skip_File = False

    if not skip_File:
        try:
            with open(file_dir, "r") as file:
                local_count = 0
                for line in file:
                    if line != "\n":
                        local_count += 1
                relative_path = os.path.relpath(file_dir, directory)
                print(f" |{relative_path:<80} |\t {local_count:>10} |")
                line_count += local_count
        except:
            file_err_list.append(file_dir)
            continue

print(" |==================================================================================================| ")
print(f" |{'Total lines':<80} |\t {line_count:>10} | ")