import os
import json

# Load config
with open("config.json", "r") as file:
    config = json.load(file)

LOG_FOLDER = config["default_folder"]

POSITIONS_FILE = "positions.json"

# Load previous positions
if os.path.exists(POSITIONS_FILE):
    with open(POSITIONS_FILE, "r") as file:
        positions = json.load(file)
else:
    positions = {}


def check_all_logs():

    folder_errors = {}

    for folder in os.listdir(LOG_FOLDER):

        folder_path = os.path.join(LOG_FOLDER, folder)

        if not os.path.isdir(folder_path):
            continue

        error_count = 0

        for root, dirs, files in os.walk(folder_path):

            for file in files:

                if not (file.endswith(".log") or file.endswith(".txt")):
                    continue

                file_path = os.path.join(root, file)

                try:

                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:

                        # Read only new content
                        last_position = positions.get(file_path, 0)

                        f.seek(last_position)

                        for line in f:

                            if "ERROR" in line.upper():
                                error_count += 1

                        # Save new position
                        positions[file_path] = f.tell()

                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

        folder_errors[folder] = error_count

    # Save updated positions
    with open(POSITIONS_FILE, "w") as file:
        json.dump(positions, file, indent=4)

    return folder_errors