import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random

# Глобальные переменные
quotes = [
    {"text": "Знание — сила", "author": "Фрэнсис Бэкон", "topic": "Мудрость"},
    {"text": "Быть или не быть — вот в чём вопрос", "author": "Уильям Шекспир", "topic": "Философия"},
    {"text": "Познай самого себя", "author": "Сократ", "topic": "Самопознание"},
]
history = []

# Виджеты (глобально)
quote_text = None
author_text = None
topic_text = None
history_list = None
author_filter = None
topic_filter = None

def create_widgets(root):
    global quote_text, author_text, topic_text, history_list, author_filter, topic_filter

    # Кнопка генерации цитаты
    tk.Button(root, text="Сгенерировать цитату", command=generate_quote).pack(pady=10)

    # Отображение текущей цитаты
    quote_text = tk.Label(root, text="", wraplength=400, justify="center", font=("Arial", 12))
    quote_text.pack(pady=5)
    author_text = tk.Label(root, text="", font=("Arial", 10, "italic"))
    author_text.pack(pady=2)
    topic_text = tk.Label(root, text="", font=("Arial", 9))
    topic_text.pack(pady=2)

    # Фильтры
    filter_frame = tk.Frame(root)
    filter_frame.pack(pady=5)

    tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0)
    author_filter = ttk.Combobox(filter_frame, state="readonly")
    author_filter.grid(row=0, column=1, padx=5)
    author_filter.bind("<<ComboboxSelected>>", apply_filters)

    tk.Label(filter_frame, text="Фильтр по теме:").grid(row=1, column=0)
    topic_filter = ttk.Combobox(filter_frame, state="readonly")
    topic_filter.grid(row=1, column=1, padx=5)
    topic_filter.bind("<<ComboboxSelected>>", apply_filters)

    # История цитат
    tk.Label(root, text="История цитат:").pack()
    history_list = scrolledtext.ScrolledText(root, height=10, width=60)
    history_list.pack(pady=5, padx=10)

    # Кнопки управления
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Очистить историю", command=clear_history).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Сохранить историю", command=save_data).pack(side="left", padx=5)

    update_filters()
    update_history_display()

def generate_quote():
    if not quotes:
        messagebox.showwarning("Предупреждение", "Нет доступных цитат!")
        return

    quote = random.choice(quotes)
    history.append(quote)

    # Отображаем цитату
    quote_text.config(text=f"\"{quote['text']}\"")
    author_text.config(text=f"— {quote['author']}")
    topic_text.config(text=f"Тема: {quote['topic']}")

    # Обновляем историю
    update_history_display()

def update_history_display():
    history_list.delete(1.0, tk.END)
    for i, quote in enumerate(history[-20:], 1):  # Последние 20 цитат
        history_list.insert(tk.END, f"{i}. \"{quote['text']}\"\n — {quote['author']} ({quote['topic']})\n\n")

def update_filters():
    authors = sorted(set(q["author"] for q in quotes))
    topics = sorted(set(q["topic"] for q in quotes))

    author_filter["values"] = ["Все"] + authors
    topic_filter["values"] = ["Все"] + topics
    author_filter.set("Все")
    topic_filter.set("Все")

def apply_filters(event=None):
    author_filter_val = author_filter.get()
    topic_filter_val = topic_filter.get()

    filtered = quotes
    if author_filter_val != "Все":
        filtered = [q for q in filtered if q["author"] == author_filter_val]
    if topic_filter_val != "Все":
        filtered = [q for q in filtered if q["topic"] == topic_filter_val]

    if not filtered:
        messagebox.showinfo("Информация", "По заданным фильтрам цитат не найдено")
        return

    quote = random.choice(filtered)
    history.append(quote)
    quote_text.config(text=f"\"{quote['text']}\"")
    author_text.config(text=f"— {quote['author']}")
    topic_text.config(text=f"Тема: {quote['topic']}")
    update_history_display()

def clear_history():
    global history
    history = []
    update_history_display()

def save_data():
    data = {
        "quotes": quotes,
        "history": history
    }
    with open("quotes_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Успех", "Данные сохранены в quotes_data.json")

def load_data():
    try:
        with open("quotes_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            global quotes
            quotes = data.get("quotes", quotes)
    except FileNotFoundError:
        # Если файл не найден — используем предустановленные цитаты
        pass
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Random Quote Generator")

    load_data()
    create_widgets(root)

    root.mainloop()

