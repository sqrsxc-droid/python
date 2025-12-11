"""
Органайзер событий
Приложение для планирования событий с хранением данных в JSON файле
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import sys


class Event:
    """Класс для представления события"""

    # Типы событий
    EVENT_TYPES = {
        "meeting": "Встреча",
        "call": "Телефонный звонок",
        "birthday": "День рождения",
        "task": "Задание",
        "reminder": "Напоминание",
        "other": "Другое"
    }

    def __init__(self,
                 event_type: str,
                 title: str,
                 date: str,
                 time: str,
                 duration: int = 30,
                 description: str = "",
                 event_id: Optional[int] = None):
        """
        Инициализация события

        Args:
            event_type: Тип события (ключ из EVENT_TYPES)
            title: Название события
            date: Дата в формате YYYY-MM-DD
            time: Время в формате HH:MM
            duration: Продолжительность в минутах (минимум 15)
            description: Описание события
            event_id: Уникальный идентификатор события
        """
        self.event_id = event_id
        self.event_type = event_type
        self.title = title
        self.date = date
        self.time = time
        self.duration = max(duration, 15)  # Минимальная продолжительность 15 минут
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование события в словарь для сохранения"""
        return {
            "id": self.event_id,
            "type": self.event_type,
            "title": self.title,
            "date": self.date,
            "time": self.time,
            "duration": self.duration,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """Создание события из словаря"""
        return cls(
            event_id=data.get("id"),
            event_type=data["type"],
            title=data["title"],
            date=data["date"],
            time=data["time"],
            duration=data.get("duration", 30),
            description=data.get("description", "")
        )

    def __str__(self) -> str:
        """Строковое представление события"""
        event_type_name = self.EVENT_TYPES.get(self.event_type, self.event_type)
        date_obj = datetime.strptime(self.date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d.%m.%Y")

        return (
            f"[{self.event_id}] {event_type_name}: {self.title}\n"
            f"   📅 Дата: {formatted_date} ⏰ Время: {self.time}\n"
            f"   ⏱️  Продолжительность: {self.duration} мин.\n"
            f"   📝 Описание: {self.description}\n"
            f"{'-' * 50}"
        )


class Organizer:
    """Класс органайзера для управления событиями"""

    def __init__(self, data_file: str = "events.json"):
        """
        Инициализация органайзера

        Args:
            data_file: Путь к файлу для хранения данных
        """
        self.data_file = data_file
        self.events: List[Event] = []
        self.next_id = 1
        self.load_events()

    def load_events(self) -> None:
        """Загрузка событий из файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.events = [Event.from_dict(event_data) for event_data in data]
                    # Определяем следующий ID
                    if self.events:
                        self.next_id = max(event.event_id for event in self.events if event.event_id) + 1
                    else:
                        self.next_id = 1
                print(f"✅ Загружено {len(self.events)} событий из {self.data_file}")
            except Exception as e:
                print(f"❌ Ошибка при загрузке данных: {e}")
                self.events = []
                self.next_id = 1
        else:
            print(f"📁 Файл {self.data_file} не найден. Создан новый органайзер.")
            self.events = []
            self.next_id = 1

    def save_events(self) -> None:
        """Сохранение событий в файл"""
        try:
            data = [event.to_dict() for event in self.events]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"💾 Данные сохранены в {self.data_file}")
        except Exception as e:
            print(f"❌ Ошибка при сохранении данных: {e}")

    def add_event(self) -> None:
        """Добавление нового события"""
        print("\n" + "=" * 50)
        print("➕ ДОБАВЛЕНИЕ НОВОГО СОБЫТИЯ")
        print("=" * 50)

        # Выбор типа события
        print("\n📋 Выберите тип события:")
        for i, (key, value) in enumerate(Event.EVENT_TYPES.items(), 1):
            print(f"  {i}. {value}")

        try:
            type_choice = int(input("\nВыберите номер типа события: ")) - 1
            event_type = list(Event.EVENT_TYPES.keys())[type_choice]
        except (ValueError, IndexError):
            print("❌ Неверный выбор. Используется тип 'other'")
            event_type = "other"

        # Ввод названия
        title = input("\n📝 Введите название события: ").strip()
        if not title:
            print("❌ Название события не может быть пустым!")
            return

        # Ввод даты
        while True:
            date_str = input("\n📅 Введите дату (ГГГГ-ММ-ДД или сегодня/завтра): ").strip()

            if date_str.lower() == "сегодня":
                date_str = datetime.now().strftime("%Y-%m-%d")
                break
            elif date_str.lower() == "завтра":
                date_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                break
            else:
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                    if datetime.strptime(date_str, "%Y-%m-%d").date() >= datetime.now().date():
                        break
                    else:
                        print("❌ Дата не может быть в прошлом!")
                except ValueError:
                    print("❌ Неверный формат даты! Используйте ГГГГ-ММ-ДД")

        # Ввод времени
        while True:
            time_str = input("\n⏰ Введите время (ЧЧ:ММ): ").strip()
            try:
                datetime.strptime(time_str, "%H:%M")
                break
            except ValueError:
                print("❌ Неверный формат времени! Используйте ЧЧ:ММ")

        # Ввод продолжительности
        while True:
            try:
                duration = int(input("\n⏱️  Введите продолжительность в минутах (минимум 15): "))
                if duration >= 15:
                    break
                else:
                    print("❌ Продолжительность должна быть не менее 15 минут!")
            except ValueError:
                print("❌ Введите число!")

        # Ввод описания
        description = input("\n📄 Введите описание события (необязательно): ").strip()

        # Создание и добавление события
        new_event = Event(
            event_id=self.next_id,
            event_type=event_type,
            title=title,
            date=date_str,
            time=time_str,
            duration=duration,
            description=description
        )

        self.events.append(new_event)
        self.next_id += 1

        print(f"\n✅ Событие добавлено с ID: {new_event.event_id}")
        self.save_events()

    def view_events(self, filter_type: Optional[str] = None) -> None:
        """Просмотр событий с возможностью фильтрации"""
        print("\n" + "=" * 50)
        if filter_type:
            print(f"👁️  ПРОСМОТР СОБЫТИЙ: {Event.EVENT_TYPES.get(filter_type, filter_type)}")
        else:
            print("👁️  ПРОСМОТР ВСЕХ СОБЫТИЙ")
        print("=" * 50)

        # Фильтрация событий
        if filter_type:
            filtered_events = [e for e in self.events if e.event_type == filter_type]
        else:
            filtered_events = self.events

        # Сортировка по дате и времени
        filtered_events.sort(key=lambda x: (x.date, x.time))

        if not filtered_events:
            if filter_type:
                print(f"📭 Нет событий типа '{Event.EVENT_TYPES.get(filter_type, filter_type)}'")
            else:
                print("📭 Нет запланированных событий")
            return

        print(f"\nНайдено событий: {len(filtered_events)}\n")

        # Группировка по дате
        events_by_date: Dict[str, List[Event]] = {}
        for event in filtered_events:
            date_obj = datetime.strptime(event.date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d.%m.%Y (%A)")

            if formatted_date not in events_by_date:
                events_by_date[formatted_date] = []
            events_by_date[formatted_date].append(event)

        # Вывод событий по датам
        for date_str, date_events in sorted(events_by_date.items()):
            print(f"\n📅 {date_str}:")
            print("-" * 30)
            for event in date_events:
                event_type_name = Event.EVENT_TYPES.get(event.event_type, event.event_type)
                print(f"  [{event.event_id}] ⏰ {event.time} | {event_type_name}: {event.title}")

    def view_event_details(self, event_id: int) -> None:
        """Просмотр деталей конкретного события"""
        event = self.find_event_by_id(event_id)
        if event:
            print("\n" + "=" * 50)
            print("📋 ДЕТАЛИ СОБЫТИЯ")
            print("=" * 50)
            print(event)
        else:
            print(f"❌ Событие с ID {event_id} не найдено")

    def edit_event(self, event_id: int) -> None:
        """Редактирование события"""
        event = self.find_event_by_id(event_id)
        if not event:
            print(f"❌ Событие с ID {event_id} не найдено")
            return

        print("\n" + "=" * 50)
        print("✏️  РЕДАКТИРОВАНИЕ СОБЫТИЯ")
        print("=" * 50)
        print(f"Редактируем событие: {event.title}")
        print("\nНажмите Enter, чтобы оставить текущее значение")

        # Редактирование типа
        print(f"\n📋 Текущий тип: {Event.EVENT_TYPES.get(event.event_type, event.event_type)}")
        print("Доступные типы:")
        for i, (key, value) in enumerate(Event.EVENT_TYPES.items(), 1):
            print(f"  {i}. {value}")

        type_input = input("Введите новый номер типа (Enter - оставить текущий): ").strip()
        if type_input:
            try:
                type_choice = int(type_input) - 1
                event.event_type = list(Event.EVENT_TYPES.keys())[type_choice]
            except (ValueError, IndexError):
                print("❌ Неверный выбор. Тип не изменен")

        # Редактирование названия
        new_title = input(f"\n📝 Текущее название: {event.title}\nВведите новое название: ").strip()
        if new_title:
            event.title = new_title

        # Редактирование даты
        new_date = input(f"\n📅 Текущая дата: {event.date}\nВведите новую дату (ГГГГ-ММ-ДД): ").strip()
        if new_date:
            try:
                datetime.strptime(new_date, "%Y-%m-%d")
                if datetime.strptime(new_date, "%Y-%m-%d").date() >= datetime.now().date():
                    event.date = new_date
                else:
                    print("❌ Дата не может быть в прошлом! Дата не изменена")
            except ValueError:
                print("❌ Неверный формат даты! Дата не изменена")

        # Редактирование времени
        new_time = input(f"\n⏰ Текущее время: {event.time}\nВведите новое время (ЧЧ:ММ): ").strip()
        if new_time:
            try:
                datetime.strptime(new_time, "%H:%M")
                event.time = new_time
            except ValueError:
                print("❌ Неверный формат времени! Время не изменено")

        # Редактирование продолжительности
        new_duration = input(
            f"\n⏱️  Текущая продолжительность: {event.duration} мин.\nВведите новую продолжительность: ").strip()
        if new_duration:
            try:
                duration = int(new_duration)
                if duration >= 15:
                    event.duration = duration
                else:
                    print("❌ Продолжительность должна быть не менее 15 минут! Значение не изменено")
            except ValueError:
                print("❌ Введите число! Значение не изменено")

        # Редактирование описания
        new_description = input(f"\n📄 Текущее описание: {event.description}\nВведите новое описание: ").strip()
        if new_description:
            event.description = new_description

        print("\n✅ Событие обновлено!")
        self.save_events()

    def delete_event(self, event_id: int) -> None:
        """Удаление события"""
        event = self.find_event_by_id(event_id)
        if not event:
            print(f"❌ Событие с ID {event_id} не найдено")
            return

        print("\n" + "=" * 50)
        print("🗑️  УДАЛЕНИЕ СОБЫТИЯ")
        print("=" * 50)
        print(f"Удаляем событие: {event.title}")
        print(f"Дата: {event.date} Время: {event.time}")

        confirm = input("\nВы уверены? (да/нет): ").strip().lower()
        if confirm == "да":
            self.events = [e for e in self.events if e.event_id != event_id]
            print("✅ Событие удалено!")
            self.save_events()
        else:
            print("❌ Удаление отменено")

    def find_event_by_id(self, event_id: int) -> Optional[Event]:
        """Поиск события по ID"""
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None

    def view_upcoming_events(self) -> None:
        """Просмотр предстоящих событий (на сегодня и завтра)"""
        print("\n" + "=" * 50)
        print("🚀 ПРЕДСТОЯЩИЕ СОБЫТИЯ")
        print("=" * 50)

        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        upcoming_events = [
            e for e in self.events
            if e.date in [today, tomorrow]
        ]

        if not upcoming_events:
            print("📭 Нет предстоящих событий на сегодня и завтра")
            return

        upcoming_events.sort(key=lambda x: (x.date, x.time))

        print("\n📅 На сегодня:")
        today_events = [e for e in upcoming_events if e.date == today]
        if today_events:
            for event in today_events:
                event_type_name = Event.EVENT_TYPES.get(event.event_type, event.event_type)
                print(f"  ⏰ {event.time} | {event_type_name}: {event.title}")
        else:
            print("  📭 Нет событий")

        print("\n📅 На завтра:")
        tomorrow_events = [e for e in upcoming_events if e.date == tomorrow]
        if tomorrow_events:
            for event in tomorrow_events:
                event_type_name = Event.EVENT_TYPES.get(event.event_type, event.event_type)
                print(f"  ⏰ {event.time} | {event_type_name}: {event.title}")
        else:
            print("  📭 Нет событий")

    def search_events(self) -> None:
        """Поиск событий по ключевым словам"""
        print("\n" + "=" * 50)
        print("🔍 ПОИСК СОБЫТИЙ")
        print("=" * 50)

        search_term = input("Введите текст для поиска (название или описание): ").strip().lower()

        if not search_term:
            print("❌ Введите текст для поиска!")
            return

        found_events = [
            e for e in self.events
            if search_term in e.title.lower() or search_term in e.description.lower()
        ]

        if not found_events:
            print(f"📭 События по запросу '{search_term}' не найдены")
            return

        found_events.sort(key=lambda x: (x.date, x.time))

        print(f"\nНайдено событий: {len(found_events)}\n")

        for event in found_events:
            event_type_name = Event.EVENT_TYPES.get(event.event_type, event.event_type)
            date_obj = datetime.strptime(event.date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d.%m.%Y")
            print(f"[{event.event_id}] 📅 {formatted_date} ⏰ {event.time} | {event_type_name}: {event.title}")


def display_menu() -> None:
    """Отображение главного меню"""
    print("\n" + "=" * 50)
    print("📅 ОРГАНАЙЗЕР СОБЫТИЙ")
    print("=" * 50)
    print("1. 📋 Просмотреть все события")
    print("2. 🚀 Просмотреть предстоящие события (сегодня/завтра)")
    print("3. 🔍 Найти события")
    print("4. ➕ Добавить новое событие")
    print("5. ✏️  Редактировать событие")
    print("6. 🗑️  Удалить событие")
    print("7. 👁️  Просмотреть детали события")
    print("8. 📊 Просмотреть события по типу")
    print("9. 💾 Сохранить данные")
    print("0. 🚪 Выход")
    print("=" * 50)


def display_type_menu() -> None:
    """Отображение меню типов событий"""
    print("\n📋 Выберите тип события для просмотра:")
    for i, (key, value) in enumerate(Event.EVENT_TYPES.items(), 1):
        print(f"  {i}. {value}")
    print(" 0. Назад")


def main() -> None:
    """Главная функция приложения"""
    print("=" * 60)
    print("        🎯 ОРГАНАЙЗЕР СОБЫТИЙ")
    print("  Планирование и управление событиями")
    print("=" * 60)

    # Инициализация органайзера
    organizer = Organizer("events.json")

    # Основной цикл программы
    while True:
        display_menu()

        try:
            choice = input("\nВыберите действие (0-9): ").strip()

            if choice == "0":  # Выход
                print("\n👋 До свидания! Не забудьте о запланированных событиях!")
                break

            elif choice == "1":  # Просмотреть все события
                organizer.view_events()

            elif choice == "2":  # Предстоящие события
                organizer.view_upcoming_events()

            elif choice == "3":  # Поиск событий
                organizer.search_events()

            elif choice == "4":  # Добавить событие
                organizer.add_event()

            elif choice == "5":  # Редактировать событие
                try:
                    event_id = int(input("Введите ID события для редактирования: "))
                    organizer.edit_event(event_id)
                except ValueError:
                    print("❌ Введите числовой ID!")

            elif choice == "6":  # Удалить событие
                try:
                    event_id = int(input("Введите ID события для удаления: "))
                    organizer.delete_event(event_id)
                except ValueError:
                    print("❌ Введите числовой ID!")

            elif choice == "7":  # Детали события
                try:
                    event_id = int(input("Введите ID события для просмотра деталей: "))
                    organizer.view_event_details(event_id)
                except ValueError:
                    print("❌ Введите числовой ID!")

            elif choice == "8":  # События по типу
                display_type_menu()
                type_choice = input("\nВыберите тип: ").strip()

                if type_choice == "0":
                    continue

                try:
                    type_idx = int(type_choice) - 1
                    if 0 <= type_idx < len(Event.EVENT_TYPES):
                        event_type = list(Event.EVENT_TYPES.keys())[type_idx]
                        organizer.view_events(event_type)
                    else:
                        print("❌ Неверный выбор типа!")
                except ValueError:
                    print("❌ Введите число!")

            elif choice == "9":  # Сохранить данные
                organizer.save_events()

            else:
                print("❌ Неверный выбор! Пожалуйста, выберите от 0 до 9")

        except KeyboardInterrupt:
            print("\n\n⚠️  Программа прервана пользователем")
            save_before_exit = input("\nСохранить данные перед выходом? (да/нет): ").strip().lower()
            if save_before_exit == "да":
                organizer.save_events()
            break

        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")

        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()