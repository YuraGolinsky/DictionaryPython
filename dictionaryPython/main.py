import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
import json
import os

# Файли для зберігання даних
USERS_FILE = 'users.json'
DICTIONARY_FILE = 'dictionary.json'

# Завантаження користувачів
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        users = json.load(f)
else:
    users = {}

# Завантаження словника
if os.path.exists(DICTIONARY_FILE):
    with open(DICTIONARY_FILE, 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
else:
    dictionary = {}

def save_users():
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f)

def save_dictionary():
    with open(DICTIONARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f)

def register():
    username = simpledialog.askstring("Реєстрація", "Введіть ім'я користувача:")
    if not username:
        return
    if username in users:
        messagebox.showerror("Помилка", "Користувач вже існує")
        return
    password = simpledialog.askstring("Реєстрація", "Введіть пароль:", show='*')
    if not password:
        return
    users[username] = password
    save_users()
    messagebox.showinfo("Успіх", "Користувача зареєстровано успішно")

def set_style():
    root.option_add('*TButton', {'font': ('Arial', 12, 'bold'), 'padding': 10, 'background': '#0000FF'})
    root.option_add('*TLabel', {'font': ('Arial', 16, 'bold'), 'padding': 10, 'background': '#FFFAF0', 'foreground': '#FFA500'})
    root.option_add('*TFrame', {'background': '#FFFAF0'})
    root.option_add('*TMenubutton', {'font': ('Arial', 12)})

def login():
    global current_user
    username = simpledialog.askstring("Вхід", "Введіть ім'я користувача:")
    if not username:
        return
    password = simpledialog.askstring("Вхід", "Введіть пароль:", show='*')
    if not password:
        return
    if username not in users or users[username] != password:
        messagebox.showerror("Помилка", "Невірні облікові дані")
        return
    current_user = username
    messagebox.showinfo("Успіх", f"Ласкаво просимо, {current_user}!")

def view_dictionary():
    if not current_user:
        messagebox.showerror("Помилка", "Будь ласка, увійдіть спочатку")
        return
    dict_str = ""
    for word, info in dictionary.items():
        dict_str += f"Слово: {word}\n"
        dict_str += f"Частина мови: {info['part_of_speech']}\n"
        dict_str += f"Правила відмінювання: {info['declension_rules']}\n"
        dict_str += f"Переклад: {info.get('translation', 'немає перекладу')}\n\n"
    text_window = tk.Toplevel(root)
    text_window.title("Словник")
    text_area = tk.Text(text_window, wrap='word', font=("Arial", 12))
    text_area.insert(tk.END, dict_str)
    text_area.config(state=tk.DISABLED)
    text_area.pack(expand=True, fill='both')

def add_word():
    if not current_user:
        messagebox.showerror("Помилка", "Будь ласка, увійдіть спочатку")
        return
    word = simpledialog.askstring("Додавання слова", "Введіть слово:")
    if not word:
        return
    part_of_speech = simpledialog.askstring("Додавання слова", "Введіть частину мови:")
    if not part_of_speech:
        return
    declension_rules = simpledialog.askstring("Додавання слова", "Введіть правила відмінювання:")
    if not declension_rules:
        return
    translation = simpledialog.askstring("Додавання слова", "Введіть переклад слова:")
    if not translation:
        return
    dictionary[word] = {"part_of_speech": part_of_speech, "declension_rules": declension_rules, "translation": translation}
    save_dictionary()
    messagebox.showinfo("Успіх", "Слово додано успішно")

def edit_word():
    if not current_user:
        messagebox.showerror("Помилка", "Будь ласка, увійдіть спочатку")
        return
    word = simpledialog.askstring("Редагування слова", "Введіть слово для редагування:")
    if not word or word not in dictionary:
        messagebox.showerror("Помилка", "Слово не знайдено")
        return
    part_of_speech = simpledialog.askstring("Редагування слова", "Введіть нову частину мови:")
    if not part_of_speech:
        return
    declension_rules = simpledialog.askstring("Редагування слова", "Введіть нові правила відмінювання:")
    if not declension_rules:
        return
    translation = simpledialog.askstring("Редагування слова", "Введіть новий переклад слова:")
    if not translation:
        return
    dictionary[word] = {"part_of_speech": part_of_speech, "declension_rules": declension_rules, "translation": translation}
    save_dictionary()
    messagebox.showinfo("Успіх", "Слово оновлено успішно")

def search_word():
    if not current_user:
        messagebox.showerror("Помилка", "Будь ласка, увійдіть спочатку")
        return
    query = simpledialog.askstring("Пошук слова", "Введіть слово для пошуку:")
    if not query:
        return
    results = {word: info for word, info in dictionary.items() if query.lower() in word.lower()}
    results_str = ""
    for word, info in results.items():
        results_str += f"Слово: {word}\n"
        results_str += f"Частина мови: {info['part_of_speech']}\n"
        results_str += f"Правила відмінювання: {info['declension_rules']}\n"
        results_str += f"Переклад: {info.get('translation', 'немає перекладу')}\n\n"
    text_window = tk.Toplevel(root)
    text_window.title("Результати пошуку")
    text_area = tk.Text(text_window, wrap='word', font=("Arial", 12))
    text_area.insert(tk.END, results_str)
    text_area.config(state=tk.DISABLED)
    text_area.pack(expand=True, fill='both')

def import_dictionary():
    if not current_user:
        messagebox.showerror("Помилка", "Будь ласка, увійдіть спочатку")
        return
    file_path = filedialog.askopenfilename(title="Виберіть JSON файл", filetypes=[("JSON files", "*.json")])
    if not file_path:
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        imported_dict = json.load(f)
    dictionary.update(imported_dict)
    save_dictionary()
    messagebox.showinfo("Успіх", "Словник імпортовано успішно")

def about_software():
    messagebox.showinfo("Про програмне забезпечення", "Це програмне забезпечення для управління словником. Ви можете додавати, редагувати, переглядати та шукати слова в словнику. Версія 1.0")

def instructions():
    instruction_text = """
    Інструкція з користування:

    1. Реєстрація:
       - Натисніть "Реєстрація"
       - Введіть ім'я користувача та пароль
       - Натисніть "OK" для збереження

    2. Вхід:
       - Натисніть "Вхід"
       - Введіть ім'я користувача та пароль
       - Натисніть "OK" для входу

    3. Перегляд словника:
       - Натисніть "Перегляд словника" для перегляду всіх слів

    4. Додавання слова:
       - Натисніть "Додавання слова"
       - Введіть слово, частину мови та правила відмінювання
       - Натисісніть "OK" для збереження

    5. Редагування слова:
       - Натисніть "Редагування слова"
       - Введіть слово для редагування
       - Введіть нову частину мови та правила відмінювання
       - Натисніть "OK" для збереження змін

    6. Пошук слова:
       - Натисніть "Пошук слова"
       - Введіть слово для пошуку
       - Натисніть "OK" для перегляду результатів

    7. Імпорт словника:
       - Натисніть "Імпорт словника"
       - Виберіть файл JSON для імпорту
       - Натисніть "OK" для імпорту

    8. Вихід:
       - Натисніть "Файл" -> "Вихід" для завершення роботи
    """
    instruction_window = tk.Toplevel(root)
    instruction_window.title("Інструкція")
    text_area = tk.Text(instruction_window, wrap='word', font=("Arial", 12))
    text_area.insert(tk.END, instruction_text)
    text_area.config(state=tk.DISABLED)
    text_area.pack(expand=True, fill='both')

def main():
    global root, current_user
    current_user = None
    root = tk.Tk()
    root.title("Словник")
    root.geometry("500x600")
    root.config(bg="#FFFAF0")
    root.iconbitmap(r'D:\Фриланс\12712\dictionaryPython\.venv\image-removebg-preview.ico')

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12, "bold"), padding=10, background="#0000FF",
                    focuscolor="none")
    style.configure("TLabel", font=("Arial", 16, "bold"), padding=10, background="#FFFAF0", foreground="#FFA500")
    style.configure("TFrame", background="#FFFAF0")
    style.configure("TMenubutton", font=("Arial", 12))

    # Панель меню
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Додавання меню "Файл"
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label ="Імпорт словника", command=import_dictionary)
    file_menu.add_separator()
    file_menu.add_command(label="Вихід", command=root.quit)
    menu_bar.add_cascade(label="Файл", menu=file_menu)

    # Додавання меню "Довідка"
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Про програмне забезпечення", command=about_software)
    help_menu.add_command(label="Інструкція", command=instructions)
    menu_bar.add_cascade(label="Довідка", menu=help_menu)

    main_frame = ttk.Frame(root)
    main_frame.pack(pady=20, padx=20, fill='both', expand=True)

    ttk.Label(main_frame, text="Словник", anchor="center").pack(pady=10)

    ttk.Button(main_frame, text="Реєстрація", command=register).pack(pady=5, fill='x')
    ttk.Button(main_frame, text="Вхід", command=login).pack(pady=5, fill='x')
    ttk.Button(main_frame, text="Перегляд словника", command=view_dictionary).pack(pady=5, fill='x')
    ttk.Button(main_frame, text="Додавання слова", command=add_word).pack(pady=5, fill='x')
    ttk.Button(main_frame, text="Редагування слова", command=edit_word).pack(pady=5, fill='x')
    ttk.Button(main_frame, text="Пошук слова", command=search_word).pack(pady=5, fill='x')
    ttk.Button(main_frame, text="Імпорт словника", command=import_dictionary).pack(pady=5, fill='x')

    root.mainloop()

if __name__ == '__main__':
    main()

