import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name

    def on_modified(self, event):
        if event.src_path.endswith(self.script_name):
            print("\n🔄 Изменения обнаружены. Перезапуск...")
            os.system(f"taskkill /f /im python.exe >nul 2>&1")
            time.sleep(1)
            os.system(f"start cmd /k python {self.script_name}")
            os._exit(0)

if __name__ == "__main__":
    script = "bot.py"
    print("🚀 Запуск бота...")
    os.system(f"start cmd /k python {script}")

    print(f"👀 Отслеживание изменений в {script}...")
    event_handler = RestartHandler(script)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
