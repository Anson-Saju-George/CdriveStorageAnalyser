import os
import humanize
from tabulate import tabulate

# Configuration
DRIVE_PATH = "C:\\"
MAX_LEVEL = 3 # Depth of the dir tree to display
SIZE_LIMIT = 1 * 1024 * 1024 * 1024
# SIZE_LIMIT = 500 * 1024 * 1024 # If you want to test with smaller size limit in MB
USE_SIZE_LIMIT = True

def get_directory_size(path):
    # Recursively calculate the total size of a directory.
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total_size += os.path.getsize(fp)
            except Exception as e:
                print(f"Access Denied! {fp}")
    return total_size

def collect_storage_data(path, max_level, level=0):
    # Recursively collect storage data for each directory level.
    if level >= max_level:
        return []
    
    size = get_directory_size(path)
    
    # Apply size limit filter if enabled
    if USE_SIZE_LIMIT and size < SIZE_LIMIT:
        return []

    # Prepare tabulate row based on current directory level
    row = [""] * (max_level * 2)
    row[level * 2] = os.path.basename(path) or path
    row[level * 2 + 1] = humanize.naturalsize(size)

    data = [row]

    if os.path.isdir(path) and level < max_level:
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    data.extend(collect_storage_data(item_path, max_level, level + 1))
        except PermissionError:
            print(f"Access denied at {path}. Size calculated only for accessible parts.")
    return data

# Collect data and display as a table
data = collect_storage_data(DRIVE_PATH, MAX_LEVEL) # Data collection starts from the root directory
headers = [f"Level {i}" if i % 2 == 1 else "Space" for i in range(1, MAX_LEVEL * 2 + 1)] # Generate headers based on max level
print(tabulate(data, headers=headers, tablefmt="grid"))