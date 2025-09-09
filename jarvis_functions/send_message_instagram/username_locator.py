FILE_PATH = "D:/pycharm/opencv/PythonProject1/jarvis_functions/send_message_instagram/usernames.txt"

# Function to read usernames and URLs from the file
def get_url_for_username(target_username: str):
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            for line in file:
                if " - " in line:
                    username, url = line.strip().split(" - ", 1)
                    if username.strip() == target_username.strip():
                        return url.strip()
        print(f"Username '{target_username}' not found in {FILE_PATH}")
        return None
    except FileNotFoundError:
        print(f"Error: {FILE_PATH} not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

