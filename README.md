---
# 📂 Directory Storage Analyzer with Size Limit 📊

**Author:** Anson Saju George

---

## 🎉 Introduction

Hey there! I created this storage analyzer script not just for myself, but for the entire community. With this tool, you can analyze your directory structure and understand your storage usage in a clear, organized table. 📈

This code isn't just for storage analysis—it can also be adapted for data analysis tasks in data science! By understanding how much space your data occupies and organizing your files at different directory levels, you can manage resources effectively and even incorporate this into larger data projects. 🛠️

---

## 🚀 How It Works

The script traverses a specified directory tree, calculates the size of each folder up to a certain depth (level), and displays the results in a tabular format. This is especially helpful for identifying large folders and managing storage on your machine.

Here are the key features of this script:

- **Customizable Directory Depth**: Define how deep into your directory structure you want to analyze.
- **Size Limit Filter**: Optionally display only directories that exceed a specified size limit, perfect for spotting oversized folders quickly.
- **Human-Readable Sizes**: Outputs sizes in formats like KB, MB, or GB for easier understanding.
- **Tabulated Output**: Provides a clean, table-style display of directory sizes, improving readability.

---

## 📜 Code

Here's the code that powers this tool:

```python
import os
import humanize
from tabulate import tabulate

# Configuration
DRIVE_PATH = "C:\\"  # The starting directory for analysis
MAX_LEVEL = 3        # Depth of the directory tree to display
SIZE_LIMIT = 1 * 1024 * 1024 * 1024  # Size limit in bytes for filtering
USE_SIZE_LIMIT = True  # Set to True to enable the size limit filter

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
data = collect_storage_data(DRIVE_PATH, MAX_LEVEL)
headers = [f"Level {i}" if i % 2 == 1 else "Space" for i in range(1, MAX_LEVEL * 2 + 1)]
print(tabulate(data, headers=headers, tablefmt="grid"))
```

---

## 🛠️ How to Use

1. **Set the `DRIVE_PATH`**: Define the starting directory for the analysis.
2. **Configure `MAX_LEVEL`**: Specify how deep you want to analyze the directory tree.
3. **Enable Size Filter**: If `USE_SIZE_LIMIT` is set to `True`, the script will only display directories that exceed `SIZE_LIMIT` (in bytes).

### Example Output:

The output is displayed in a well-organized table format with columns for each directory level, making it easy to see which folders take up the most space. Here’s what it might look like:

```
+--------------+-------------+---------------+-------------+
| Level 1      | Space       | Level 2       | Space       |
+--------------+-------------+---------------+-------------+
| Users        | 20 GB       | Documents     | 1.5 GB      |
| Program Files| 8.2 GB      | Windows       | 5 GB        |
+--------------+-------------+---------------+-------------+
```

---

## 🏆 Conclusion

I hope this script helps you and others manage storage better and uncover data organization opportunities! Give it a try, tweak the settings, and feel free to adapt it for any data science needs. Happy analyzing! 😊
