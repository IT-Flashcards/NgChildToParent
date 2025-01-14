import os
import time
import subprocess
import pyautogui


LOG_FILE = "/home/mafi/Desktop/setup.log"

def log_message(message):
    """Loguje wiadomość do pliku oraz drukuje ją w konsoli."""
    with open(LOG_FILE, "a") as log:
        log.write(f"{time.strftime('Setup.py - %Y-%m-%d %H:%M:%S')} - {message}\n")
    print(message)


def main():
    # Get screen size via PyAutoGUI
    screen_width, screen_height = pyautogui.size()
    log_message(f"Detected screen size: {screen_width}x{screen_height}")

    # Paths
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(desktop_path, "CurrentFlashcard")
    ng_parent_to_child_path = os.path.join(folder_path, "NgParentToChild")

    # 1. Open file manager (e.g. nautilus) with 'CurrentFlashcard'
    if os.path.exists(folder_path):
        log_message("Opening file manager in 'CurrentFlashcard'...")
        subprocess.Popen(
            ["xdg-open", folder_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        time.sleep(5)  # Wait 5s for file manager to open
    else:
        log_message("Folder 'CurrentFlashcard' does not exist on Desktop.")

    # 2. Open Visual Studio Code in `NgParentToChild`
    if os.path.exists(ng_parent_to_child_path):
        try:
            log_message("Opening Visual Studio Code...")
            subprocess.Popen(
                ["/snap/bin/code", ng_parent_to_child_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            time.sleep(30)  # Wait for VS Code to load

            # Próbujemy ustawić fokus na VS Code
            # log_message("Setting focus to Visual Studio Code window.")
            # pyautogui.hotkey("alt", "tab")  # Przełącz na okno Visual Studio Code
            # time.sleep(2)

            # Wywołanie terminala: Ctrl + `
            log_message("Sending Ctrl+`")
            pyautogui.hotkey("ctrl", "`")
            time.sleep(10)

            # Wpisz 'npm i' i zatwierdź Enter
            log_message("Sending 'npm i -f'")
            pyautogui.typewrite("npm i -f\n", interval=0.05)
            time.sleep(30)  # Czekamy np. 30s na instalację

            # Wpisz 'ng s -o' i zatwierdź Enter
            log_message("Sending 'ng s -o'")
            pyautogui.typewrite("ng s -o\n", interval=0.05)

        except FileNotFoundError:
            log_message("VS Code not found. Make sure it is installed and added to PATH.")
        except Exception as e:
            log_message(f"Error while handling Visual Studio Code: {e}")
    else:
        log_message("Folder 'NgParentToChild' does not exist.")

if __name__ == "__main__":
    main()
    log_message("setup.py executed successfully.")