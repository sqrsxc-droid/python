import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime, timedelta
from pathlib import Path
import os


class Event:
    """Класс для представления события"""
    EVENT_TYPES = ["Встреча", "Телефонный звонок", "День рождения",
                   "Задание", "Консультация", "Совещание", "Другое"]

    def __init__(self, title="", event_type="Встреча", date=None,
                 start_time="09:00", duration=60, description=""):
        self.title = title
        self.event_type = event_type
        self.date = date if date else datetime.now().date()
        self.start_time = start_time
        self.duration = max(duration, 15)  # Минимум 15 минут
        self.description = description

    @property
    def end_time(self):
        """Вычисление времени окончания события"""
        start_dt = datetime.strptime(self.start_time, "%H:%M")
        end_dt = start_dt + timedelta(minutes=self.duration)
        return end_dt.strftime("%H:%M")

    def to_dict(self):
        """Преобразование в словарь для сохранения в JSON"""
        return {
            "title": self.title,
            "type": self.event_type,
            "date": self.date.isoformat() if isinstance(self.date, datetime) else str(self.date),
            "start_time": self.start_time,
            "duration": self.duration,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        """Создание объекта Event из словаря"""
        event = cls()
        event.title = data.get("title", "")
        event.event_type = data.get("type", "Встреча")

        # Обработка даты
        date_str = data.get("date", "")
        try:
            event.date = datetime.fromisoformat(date_str).date()
        except:
            try:
                event.date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                event.date = datetime.now().date()

        event.start_time = data.get("start_time", "09:00")
        event.duration = max(data.get("duration", 60), 15)
        event.description = data.get("description", "")
        return event

    def __str__(self):
        return f"{self.title} ({self.event_type}) - {self.date} {self.start_time}-{self.end_time}"


class EventOrganizer:
    """Главный класс приложения-органайзера"""

    def __init__(self, root):
        self.root = root
        self.root.title("Органайзер событий")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)

        # Центрирование окна
        self.center_window()

        # Файл для хранения данных
        self.data_file = "events.json"

        # Список событий
        self.events = []

        # Текущее выбранное событие
        self.selected_event = None

        # Настройка стилей
        self.configure_styles()

        # Создание интерфейса
        self.create_widgets()

        # Загрузка данных
        self.load_events()

        # Обновление списка событий
        self.refresh_events_list()

    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def configure_styles(self):
        """Настройка стилей элементов"""
        style = ttk.Style()
        style.theme_use('clam')

        # Цветовая схема
        self.colors = {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'button': '#4CAF50',
            'button_hover': '#45a049',
            'danger': '#f44336',
            'danger_hover': '#d32f2f',
            'warning': '#ff9800',
            'warning_hover': '#f57c00',
            'sidebar': '#e8e8e8'
        }

    def create_widgets(self):
        """Создание всех элементов интерфейса"""

        # Основной контейнер
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Левая панель - форма добавления/редактирования
        left_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        # Правая панель - список событий
        right_frame = tk.Frame(main_frame, bg=self.colors['sidebar'])
        right_frame.pack(side='right', fill='both', expand=True)

        # Заголовок формы
        form_title = tk.Label(
            left_frame,
            text="Добавление события",
            font=('Arial', 16, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        form_title.pack(pady=(0, 20), anchor='w')

        # Поле названия события
        tk.Label(
            left_frame,
            text="Название события:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        ).pack(anchor='w', pady=(0, 5))

        self.title_entry = tk.Entry(
            left_frame,
            font=('Arial', 11),
            width=40
        )
        self.title_entry.pack(pady=(0, 15), fill='x')

        # Поле типа события
        tk.Label(
            left_frame,
            text="Тип события:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        ).pack(anchor='w', pady=(0, 5))

        self.type_combo = ttk.Combobox(
            left_frame,
            values=Event.EVENT_TYPES,
            font=('Arial', 11),
            state='readonly'
        )
        self.type_combo.set(Event.EVENT_TYPES[0])
        self.type_combo.pack(pady=(0, 15), fill='x')

        # Фрейм для даты и времени
        datetime_frame = tk.Frame(left_frame, bg=self.colors['bg'])
        datetime_frame.pack(fill='x', pady=(0, 15))

        # Дата
        tk.Label(
            datetime_frame,
            text="Дата:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        ).pack(side='left', padx=(0, 10))

        self.date_entry = tk.Entry(
            datetime_frame,
            font=('Arial', 11),
            width=12
        )
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(side='left', padx=(0, 20))

        # Время начала
        tk.Label(
            datetime_frame,
            text="Время начала:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        ).pack(side='left', padx=(0, 10))

        self.time_entry = tk.Entry(
            datetime_frame,
            font=('Arial', 11),
            width=8
        )
        self.time_entry.insert(0, "09:00")
        self.time_entry.pack(side='left')

        # Продолжительность
        tk.Label(
            left_frame,
            text="Продолжительность (минут, мин. 15):",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        ).pack(anchor='w', pady=(0, 5))

        duration_frame = tk.Frame(left_frame, bg=self.colors['bg'])
        duration_frame.pack(fill='x', pady=(0, 15))

        self.duration_var = tk.IntVar(value=60)
        self.duration_spinbox = tk.Spinbox(
            duration_frame,
            from_=15,
            to=1440,
            increment=15,
            textvariable=self.duration_var,
            font=('Arial', 11),
            width=10
        )
        self.duration_spinbox.pack(side='left', padx=(0, 10))

        # Поле описания
        tk.Label(
            left_frame,
            text="Описание:",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        ).pack(anchor='w', pady=(0, 5))

        self.desc_text = tk.Text(
            left_frame,
            font=('Arial', 11),
            height=8,
            width=40
        )
        self.desc_text.pack(pady=(0, 20), fill='both', expand=True)

        # Кнопки управления
        buttons_frame = tk.Frame(left_frame, bg=self.colors['bg'])
        buttons_frame.pack(fill='x', pady=(10, 0))

        self.add_button = tk.Button(
            buttons_frame,
            text="Добавить событие",
            font=('Arial', 11, 'bold'),
            bg=self.colors['button'],
            fg='white',
            command=self.add_event,
            cursor='hand2'
        )
        self.add_button.pack(side='left', padx=(0, 10), ipadx=15, ipady=8)

        self.update_button = tk.Button(
            buttons_frame,
            text="Обновить событие",
            font=('Arial', 11),
            bg=self.colors['warning'],
            fg='white',
            command=self.update_event,
            state='disabled',
            cursor='hand2'
        )
        self.update_button.pack(side='left', padx=(0, 10), ipadx=15, ipady=8)

        self.cancel_button = tk.Button(
            buttons_frame,
            text="Отменить",
            font=('Arial', 11),
            bg=self.colors['sidebar'],
            fg=self.colors['fg'],
            command=self.cancel_edit,
            state='disabled',
            cursor='hand2'
        )
        self.cancel_button.pack(side='left', ipadx=15, ipady=8)

        # Правая панель - список событий
        tk.Label(
            right_frame,
            text="Список событий",
            font=('Arial', 16, 'bold'),
            bg=self.colors['sidebar'],
            fg=self.colors['fg']
        ).pack(pady=(0, 10), anchor='w')

        # Панель фильтров
        filter_frame = tk.Frame(right_frame, bg=self.colors['sidebar'])
        filter_frame.pack(fill='x', pady=(0, 10))

        tk.Label(
            filter_frame,
            text="Фильтр по дате:",
            font=('Arial', 10),
            bg=self.colors['sidebar'],
            fg=self.colors['fg']
        ).pack(side='left', padx=(0, 10))

        self.filter_date_var = tk.StringVar(value="all")
        date_filters = [
            ("Все", "all"),
            ("Сегодня", "today"),
            ("Завтра", "tomorrow"),
            ("Эта неделя", "week"),
            ("Этот месяц", "month")
        ]

        for text, value in date_filters:
            rb = tk.Radiobutton(
                filter_frame,
                text=text,
                variable=self.filter_date_var,
                value=value,
                font=('Arial', 10),
                bg=self.colors['sidebar'],
                fg=self.colors['fg'],
                command=self.refresh_events_list
            )
            rb.pack(side='left', padx=(0, 10))

        # Список событий в Treeview
        columns = ("ID", "Название", "Тип", "Дата", "Время", "Длительность")
        self.events_tree = ttk.Treeview(
            right_frame,
            columns=columns,
            show='headings',
            height=20
        )

        # Настройка колонок
        self.events_tree.heading("ID", text="ID")
        self.events_tree.heading("Название", text="Название")
        self.events_tree.heading("Тип", text="Тип")
        self.events_tree.heading("Дата", text="Дата")
        self.events_tree.heading("Время", text="Время")
        self.events_tree.heading("Длительность", text="Длительность")

        self.events_tree.column("ID", width=30, stretch=False)
        self.events_tree.column("Название", width=150)
        self.events_tree.column("Тип", width=100, stretch=False)
        self.events_tree.column("Дата", width=90, stretch=False)
        self.events_tree.column("Время", width=90, stretch=False)
        self.events_tree.column("Длительность", width=80, stretch=False)

        # Скроллбар для списка
        tree_scroll = ttk.Scrollbar(
            right_frame,
            orient='vertical',
            command=self.events_tree.yview
        )
        self.events_tree.configure(yscrollcommand=tree_scroll.set)

        self.events_tree.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')

        # Привязка события выбора
        self.events_tree.bind('<<TreeviewSelect>>', self.on_event_select)

        # Кнопки для списка событий
        list_buttons_frame = tk.Frame(right_frame, bg=self.colors['sidebar'])
        list_buttons_frame.pack(fill='x', pady=(10, 0))

        tk.Button(
            list_buttons_frame,
            text="Редактировать",
            font=('Arial', 10),
            bg=self.colors['warning'],
            fg='white',
            command=self.edit_selected_event,
            cursor='hand2'
        ).pack(side='left', padx=(0, 10), ipadx=10, ipady=5)

        tk.Button(
            list_buttons_frame,
            text="Удалить",
            font=('Arial', 10),
            bg=self.colors['danger'],
            fg='white',
            command=self.delete_selected_event,
            cursor='hand2'
        ).pack(side='left', ipadx=10, ipady=5)

        # Статус-бар
        self.status_bar = tk.Label(
            self.root,
            text="Готово",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=('Arial', 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def validate_input(self):
        """Валидация введенных данных"""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Ошибка", "Введите название события!")
            return False

        date_str = self.date_entry.get().strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
            return False

        time_str = self.time_entry.get().strip()
        try:
            datetime.strptime(time_str, "%H:%M")
        except ValueError:
            messagebox.showerror("Ошибка", "Время должно быть в формате ЧЧ:ММ")
            return False

        duration = self.duration_var.get()
        if duration < 15:
            messagebox.showerror("Ошибка", "Продолжительность должна быть не менее 15 минут")
            return False

        return True

    def clear_form(self):
        """Очистка формы"""
        self.title_entry.delete(0, tk.END)
        self.type_combo.set(Event.EVENT_TYPES[0])
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "09:00")
        self.duration_var.set(60)
        self.desc_text.delete(1.0, tk.END)

        self.selected_event = None
        self.add_button.config(state='normal')
        self.update_button.config(state='disabled')
        self.cancel_button.config(state='disabled')

        form_title = self.root.nametowidget(self.root.winfo_children()[0].winfo_children()[0])
        form_title.config(text="Добавление события")

    def add_event(self):
        """Добавление нового события"""
        if not self.validate_input():
            return

        event = Event(
            title=self.title_entry.get().strip(),
            event_type=self.type_combo.get(),
            date=datetime.strptime(self.date_entry.get().strip(), "%Y-%m-%d").date(),
            start_time=self.time_entry.get().strip(),
            duration=self.duration_var.get(),
            description=self.desc_text.get(1.0, tk.END).strip()
        )

        self.events.append(event)
        self.save_events()
        self.refresh_events_list()
        self.clear_form()

        self.status_bar.config(text=f"Событие '{event.title}' добавлено")

    def update_event(self):
        """Обновление выбранного события"""
        if not self.selected_event or not self.validate_input():
            return

        # Обновляем выбранное событие
        self.selected_event.title = self.title_entry.get().strip()
        self.selected_event.event_type = self.type_combo.get()
        self.selected_event.date = datetime.strptime(self.date_entry.get().strip(), "%Y-%m-%d").date()
        self.selected_event.start_time = self.time_entry.get().strip()
        self.selected_event.duration = self.duration_var.get()
        self.selected_event.description = self.desc_text.get(1.0, tk.END).strip()

        self.save_events()
        self.refresh_events_list()
        self.clear_form()

        self.status_bar.config(text=f"Событие '{self.selected_event.title}' обновлено")

    def edit_selected_event(self):
        """Заполнение формы для редактирования выбранного события"""
        selection = self.events_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите событие для редактирования")
            return

        # Получаем ID события из первого столбца
        event_id = int(self.events_tree.item(selection[0])['values'][0])

        # Находим событие в списке
        for event in self.events:
            if id(event) == event_id:
                self.selected_event = event
                break

        if self.selected_event:
            # Заполняем форму данными события
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, self.selected_event.title)

            self.type_combo.set(self.selected_event.event_type)

            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, self.selected_event.date.strftime("%Y-%m-%d"))

            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, self.selected_event.start_time)

            self.duration_var.set(self.selected_event.duration)

            self.desc_text.delete(1.0, tk.END)
            self.desc_text.insert(1.0, self.selected_event.description)

            # Меняем состояние кнопок
            self.add_button.config(state='disabled')
            self.update_button.config(state='normal')
            self.cancel_button.config(state='normal')

            # Меняем заголовок формы
            form_title = self.root.nametowidget(self.root.winfo_children()[0].winfo_children()[0])
            form_title.config(text="Редактирование события")

            self.status_bar.config(text=f"Редактирование события '{self.selected_event.title}'")

    def cancel_edit(self):
        """Отмена редактирования"""
        self.clear_form()
        self.status_bar.config(text="Редактирование отменено")

    def delete_selected_event(self):
        """Удаление выбранного события"""
        selection = self.events_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите событие для удаления")
            return

        # Получаем ID события из первого столбца
        event_id = int(self.events_tree.item(selection[0])['values'][0])

        # Подтверждение удаления
        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить это событие?"):
            return

        # Находим и удаляем событие
        for i, event in enumerate(self.events):
            if id(event) == event_id:
                deleted_title = event.title
                del self.events[i]
                break

        self.save_events()
        self.refresh_events_list()
        self.clear_form()

        self.status_bar.config(text=f"Событие '{deleted_title}' удалено")

    def on_event_select(self, event):
        """Обработка выбора события в списке"""
        selection = self.events_tree.selection()
        if selection:
            event_id = int(self.events_tree.item(selection[0])['values'][0])

            # Находим событие
            for ev in self.events:
                if id(ev) == event_id:
                    # Показываем подробности в статус-баре
                    self.status_bar.config(
                        text=f"Выбрано: {ev.title} - {ev.date} {ev.start_time}-{ev.end_time}"
                    )
                    break

    def refresh_events_list(self):
        """Обновление списка событий с учетом фильтра"""
        # Очищаем список
        for item in self.events_tree.get_children():
            self.events_tree.delete(item)

        # Получаем текущую дату для фильтрации
        now = datetime.now()
        today = now.date()

        # Фильтруем события
        filtered_events = []
        filter_type = self.filter_date_var.get()

        for event in self.events:
            include = True

            if filter_type == "today":
                include = event.date == today
            elif filter_type == "tomorrow":
                tomorrow = today + timedelta(days=1)
                include = event.date == tomorrow
            elif filter_type == "week":
                # События на текущей неделе
                week_start = today - timedelta(days=today.weekday())
                week_end = week_start + timedelta(days=6)
                include = week_start <= event.date <= week_end
            elif filter_type == "month":
                # События в текущем месяце
                include = event.date.year == today.year and event.date.month == today.month

            if include:
                filtered_events.append(event)

        # Сортируем события по дате и времени
        filtered_events.sort(key=lambda x: (x.date, x.start_time))

        # Добавляем события в список
        for event in filtered_events:
            event_id = id(event)
            self.events_tree.insert(
                "",
                tk.END,
                values=(
                    event_id,
                    event.title,
                    event.event_type,
                    event.date.strftime("%d.%m.%Y"),
                    f"{event.start_time}-{event.end_time}",
                    f"{event.duration} мин"
                )
            )

        self.status_bar.config(text=f"Показано событий: {len(filtered_events)}")

    def save_events(self):
        """Сохранение событий в JSON файл"""
        try:
            events_data = [event.to_dict() for event in self.events]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(events_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")

    def load_events(self):
        """Загрузка событий из JSON файла"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    events_data = json.load(f)
                    self.events = [Event.from_dict(data) for data in events_data]
        except Exception as e:
            messagebox.showwarning("Предупреждение",
                                   f"Не удалось загрузить данные из файла: {str(e)}")


def main():
    """Основная функция запуска приложения"""
    root = tk.Tk()
    app = EventOrganizer(root)

    # Обработка закрытия окна
    def on_closing():
        if messagebox.askokcancel("Выход", "Сохранить изменения перед выходом?"):
            app.save_events()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()