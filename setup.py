from pywinauto import Application, Desktop
import os
import time
from win32api import GetSystemMetrics
import subprocess

# Pobieranie wymiarów ekranu
screen_width = GetSystemMetrics(0)  # Szerokość ekranu
screen_height = GetSystemMetrics(1)  # Wysokość ekranu

# Ścieżka do katalogu na pulpicie
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
folder_path = os.path.join(desktop_path, 'CurrentFlashcard')

# Sprawdzenie, czy katalog istnieje
if os.path.exists(folder_path):
    # Uruchomienie Eksploratora Windows z wybranym katalogiem
    app = Application().start(f'explorer.exe "{folder_path}"')

    # Krótki czas oczekiwania, aby okno zdążyło się załadować
    time.sleep(2)

    # Szukanie okna Eksploratora Windows
    try:
        desktop = Desktop(backend="win32")
        explorer_window = None

        # Iteracja przez otwarte okna, aby znaleźć Eksplorator Windows
        for w in desktop.windows():
            print(f"Okno: {w.window_text()}")  # Debugowanie: Wyświetlenie wszystkich otwartych okien
            if "CurrentFlashcard" in w.window_text():  # Dopasowanie na podstawie nazwy okna
                explorer_window = w
                break

        if explorer_window:
            # Przesunięcie okna do lewej górnej krawędzi
            explorer_window.move_window(x=0, y=0, width=screen_width // 2, height=screen_height // 2)
            print("Okno zostało przesunięte.")
        else:
            print("Nie znaleziono okna Eksploratora Windows dla katalogu 'CurrentFlashcard'.")
    except Exception as e:
        print(f"Nie udało się znaleźć okna: {e}")
else:
    print("Katalog 'CurrentFlashcard' nie istnieje na pulpicie.")

# Ścieżki do katalogów
current_flashcard_path = os.path.join(desktop_path, 'CurrentFlashcard')
ng_parent_to_child_path = os.path.join(current_flashcard_path, 'NgParentToChild')

# Ścieżka do Git Extensions
git_extensions_exe = r"C:\\Program Files (x86)\\GitExtensions\\GitExtensions.exe"

# Otwarcie Git Extensions w bieżącym katalogu
if os.path.exists(current_flashcard_path):
    if os.path.exists(git_extensions_exe):
        try:
            subprocess.Popen([git_extensions_exe, current_flashcard_path])  # Użycie pełnej ścieżki do GitExtensions.exe
            print(f"Git Extensions otwarty w katalogu: {current_flashcard_path}")
        except Exception as e:
            print(f"Błąd podczas otwierania Git Extensions: {e}")
    else:
        print(f"Plik wykonywalny Git Extensions nie został znaleziony w {git_extensions_exe}.")
else:
    print("Katalog 'CurrentFlashcard' nie istnieje.")

# Otwarcie Visual Studio Code w katalogu `NgParentToChild`
if os.path.exists(ng_parent_to_child_path):
    try:
        subprocess.Popen(["code", ng_parent_to_child_path])  # Zakłada, że "code" (Visual Studio Code) jest w PATH
        print(f"Visual Studio Code otwarty w katalogu: {ng_parent_to_child_path}")
        time.sleep(2)  # Czekamy na załadowanie VS Code

        # Wysyłanie klawiszy do Visual Studio Code
        try:
            desktop = Desktop(backend="uia")
            vscode_window = desktop.window(title_re=".*Visual Studio Code.*")

            # Aktywacja okna Visual Studio Code
            vscode_window.set_focus()
            time.sleep(1)

            # Wyślij kombinację klawiszy Ctrl + ` (tylda)
            vscode_window.type_keys('^`', with_spaces=True)  # ^ oznacza Ctrl

            # Czekamy chwilę na otwarcie terminala
            time.sleep(2)

            # Wpisz polecenie `npm i` i wyślij Enter
            vscode_window.type_keys('npm i{ENTER}', with_spaces=True)
            print("Polecenie 'npm i' zostało wysłane do terminala w Visual Studio Code.")

            # Czekamy na zakończenie instalacji pakietów
            time.sleep(60)

            # Wpisz polecenie `ng s -o` i wyślij Enter
            vscode_window.type_keys('ng s -o{ENTER}', with_spaces=True)
            print("Polecenie 'ng s -o' zostało wysłane do terminala w Visual Studio Code.")
        except Exception as e:
            print(f"Nie udało się wysłać poleceń do Visual Studio Code: {e}")
    except FileNotFoundError:
        print("Nie znaleziono Visual Studio Code. Upewnij się, że jest zainstalowany i dodany do PATH.")
else:
    print("Katalog 'NgParentToChild' nie istnieje.")
