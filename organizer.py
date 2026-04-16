import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer")
        self.root.geometry("450x250")
        self.root.configure(bg="#f0f0f0")

        # Словарь категорий и расширений
        self.categories = {
            "Картинки": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
            "Документы": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
            "Видео": [".mp4", ".avi", ".mkv", ".mov"],
            "Аудио": [".mp3", ".wav", ".flac"],
            "Игры_и_Программы": [".exe", ".msi"],
            "Архивы": [".zip", ".rar", ".7z", ".tar"]
        }

        # UI Элементы
        title = ttk.Label(root, text="Умный сортировщик файлов", font=("Arial", 16, "bold"), background="#f0f0f0")
        title.pack(pady=20)

        desc = ttk.Label(root, text="Выберите папку (например, Загрузки), \nчтобы навести в ней порядок.", justify=tk.CENTER, background="#f0f0f0")
        desc.pack(pady=10)

        self.btn_organize = ttk.Button(root, text="Выбрать папку и отсортировать", command=self.organize_folder)
        self.btn_organize.pack(pady=15, ipadx=10, ipady=5)

    def get_unique_filename(self, target_dir, filename):
        """Безопасность: если файл существует, добавляет (1), (2) и т.д."""
        base_name, extension = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        
        while os.path.exists(os.path.join(target_dir, new_filename)):
            new_filename = f"{base_name}({counter}){extension}"
            counter += 1
            
        return new_filename

    def organize_folder(self):
        # Открываем диалоговое окно выбора папки
        folder_path = filedialog.askdirectory(title="Выберите папку для сортировки")
        
        if not folder_path:
            return # Если пользователь нажал "Отмена"

        # Создаем или открываем файл для логов
        log_path = os.path.join(folder_path, "report.txt")
        moved_count = 0

        try:
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(f"\n--- Сортировка запущена: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")

                # Сканируем все файлы в папке
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)

                    # Пропускаем папки, сам скрипт и файл отчета
                    if os.path.isdir(item_path) or item == "report.txt" or item.endswith(".py"):
                        continue

                    file_ext = os.path.splitext(item)[1].lower()
                    moved = False

                    # Ищем подходящую категорию
                    for category, extensions in self.categories.items():
                        if file_ext in extensions:
                            target_dir = os.path.join(folder_path, category)
                            
                            # Создаем папку категории, если её нет
                            if not os.path.exists(target_dir):
                                os.makedirs(target_dir)

                            # Проверяем совпадение имен и получаем безопасное имя
                            safe_filename = self.get_unique_filename(target_dir, item)
                            final_dest = os.path.join(target_dir, safe_filename)

                            # Перемещаем файл
                            shutil.move(item_path, final_dest)
                            
                            # Записываем в лог
                            log_msg = f"Перемещен файл: '{item}' -> в папку '{category}' (Сохранен как '{safe_filename}')\n"
                            log_file.write(log_msg)
                            
                            moved_count += 1
                            moved = True
                            break # Переходим к следующему файлу

                    # Если расширение неизвестно, можно раскомментировать код ниже, чтобы кидать их в "Другое"
                    # if not moved:
                    #     other_dir = os.path.join(folder_path, "Другое")
                    #     if not os.path.exists(other_dir): os.makedirs(other_dir)
                    #     safe_filename = self.get_unique_filename(other_dir, item)
                    #     shutil.move(item_path, os.path.join(other_dir, safe_filename))

            if moved_count > 0:
                messagebox.showinfo("Готово!", f"Успешно отсортировано файлов: {moved_count}.\nПодробности в файле report.txt")
            else:
                messagebox.showinfo("Пусто", "В выбранной папке нет файлов для сортировки.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()