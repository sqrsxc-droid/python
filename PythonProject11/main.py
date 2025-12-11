"""
Работа со стеком и очередью в Python
"""
from collections import deque


def task_1():
    """Задача 1: Базовая работа с очередью"""
    print("\n" + "=" * 50)
    print("1. БАЗОВАЯ РАБОТА С ОЧЕРЕДЬЮ")
    print("=" * 50)

    # Создать очередь из целых чисел
    queue = deque()

    # Добавить в очередь 5 элементов
    print("\nДобавляем 5 элементов в очередь...")
    for i in range(1, 6):
        queue.append(i)

    # Вывести очередь
    print(f"Текущая очередь: {list(queue)}")

    # Показать первый элемент очереди
    print(f"Первый элемент очереди: {queue[0]}")

    # Вывести очередь
    print(f"Очередь: {list(queue)}")

    # Извлечь первый элемент очереди
    extracted = queue.popleft()
    print(f"Извлеченный элемент: {extracted}")

    # Вывести очередь
    print(f"Очередь после извлечения: {list(queue)}")


def task_2():
    """Задача 2: Очередь с числами от 1 до n"""
    print("\n" + "=" * 50)
    print("2. ОЧЕРЕДЬ С ЧИСЛАМИ ОТ 1 ДО N")
    print("=" * 50)

    # Ввод n от пользователя
    try:
        n = int(input("Введите целое число n: "))
    except ValueError:
        print("Ошибка: введите целое число!")
        return

    # Создать очередь из целых чисел от 1 до n
    queue = deque(range(1, n + 1))

    # Вывести очередь
    print(f"\nСоздана очередь: {list(queue)}")

    # Извлечь из очереди по порядку каждый элемент
    print("\nИзвлечение элементов по порядку:")
    sum_elements = 0
    elements = []

    while queue:
        element = queue.popleft()
        elements.append(element)
        sum_elements += element
        print(f"  Извлечен элемент: {element}")

    print(f"\nВсе извлеченные элементы: {elements}")
    print(f"Сумма всех элементов: {sum_elements}")

    # Добавить в очередь число n^2
    n_squared = n ** 2
    queue.append(n_squared)
    print(f"\nДобавлено число n^2 = {n_squared}")
    print(f"Очередь после добавления: {list(queue)}")


def task_3():
    """Задача 3: Очередь из строк 'имя номер'"""
    print("\n" + "=" * 50)
    print("3. ОЧЕРЕДЬ ИЗ СТРОК 'ИМЯ НОМЕР'")
    print("=" * 50)

    # Создать очередь из строк
    queue = deque()

    # Добавить строки вида "имя номер"
    names = ["Иван", "Мария", "Петр", "Анна", "Сергей"]

    print("\nДобавляем строки в очередь...")
    for i, name in enumerate(names, 1):
        queue.append(f"{name} {i}")

    # Вывести очередь
    print(f"Создана очередь: {list(queue)}")

    # Извлечь из очереди по порядку каждый элемент
    print("\nИзвлечение элементов по порядку:")
    while queue:
        element = queue.popleft()
        print(f"  Извлечен: {element}")


def task_4():
    """Задача 4: Базовая работа со стеком"""
    print("\n" + "=" * 50)
    print("4. БАЗОВАЯ РАБОТА СО СТЕКОМ")
    print("=" * 50)

    # Создать стек из целых чисел
    stack = []

    # Добавить в стек 6 элементов
    print("\nДобавляем 6 элементов в стек...")
    for i in range(1, 7):
        stack.append(i)

    # Вывести стек
    print(f"Текущий стек: {stack}")

    # Извлечь верхний элемент стека
    extracted = stack.pop()
    print(f"\nИзвлечен верхний элемент стека: {extracted}")

    # Вывести стек
    print(f"Стек после извлечения: {stack}")

    # Показать первый элемент стека (верхний)
    if stack:
        print(f"\nВерхний элемент стека: {stack[-1]}")

    # Вывести стек
    print(f"Стек: {stack}")

    # Извлечь еще один элемент
    if stack:
        extracted2 = stack.pop()
        print(f"\nИзвлечен еще один элемент: {extracted2}")
        print(f"Стек после извлечения: {stack}")


def task_5():
    """Задача 5: Стек с числами от 1 до n"""
    print("\n" + "=" * 50)
    print("5. СТЕК С ЧИСЛАМИ ОТ 1 ДО N")
    print("=" * 50)

    # Ввод n от пользователя
    try:
        n = int(input("Введите целое число n: "))
    except ValueError:
        print("Ошибка: введите целое число!")
        return

    # Создать стек из целых чисел от 1 до n
    stack = list(range(1, n + 1))

    # Вывести стек
    print(f"\nСоздан стек: {stack}")

    # Извлечь из стека по порядку каждый элемент
    print("\nИзвлечение элементов из стека:")
    product = 1
    elements = []

    while stack:
        element = stack.pop()
        elements.append(element)
        product *= element
        print(f"  Извлечен элемент: {element}")

    print(f"\nВсе извлеченные элементы (в порядке извлечения): {elements}")
    print(f"Произведение всех элементов: {product}")

    # Добавить в стек число n^3
    n_cubed = n ** 3
    stack.append(n_cubed)
    print(f"\nДобавлено число n^3 = {n_cubed}")
    print(f"Стек после добавления: {stack}")


def task_6():
    """Задача 6: Слова в обратном порядке с использованием стека"""
    print("\n" + "=" * 50)
    print("6. СЛОВА В ОБРАТНОМ ПОРЯДКЕ С ПОМОЩЬЮ СТЕКА")
    print("=" * 50)

    # Ввод текста от пользователя
    text = input("Введите текст: ").strip()

    if not text:
        print("Вы не ввели текст!")
        return

    # Разделить текст на слова
    words = text.split()

    # Создать стек
    word_stack = []

    # Добавить слова в стек
    print(f"\nИсходный текст: '{text}'")
    print(f"Количество слов: {len(words)}")
    print("\nДобавляем слова в стек...")

    for word in words:
        word_stack.append(word)
        print(f"  Добавлено в стек: '{word}'")

    print(f"\nСтек слов: {word_stack}")

    # Извлечь слова из стека (в обратном порядке)
    reversed_words = []

    print("\nИзвлекаем слова из стека...")
    while word_stack:
        word = word_stack.pop()
        reversed_words.append(word)
        print(f"  Извлечено из стека: '{word}'")

    # Собрать обратный текст
    reversed_text = " ".join(reversed_words)

    print("\n" + "-" * 50)
    print(f"Исходный текст: {text}")
    print(f"Текст в обратном порядке: {reversed_text}")


def main_menu():
    """Главное меню программы"""
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА: РАБОТА СО СТЕКОМ И ОЧЕРЕДЬЮ")
    print("=" * 60)

    tasks = {
        '1': ("Базовая работа с очередью", task_1),
        '2': ("Очередь с числами от 1 до n", task_2),
        '3': ("Очередь из строк 'имя номер'", task_3),
        '4': ("Базовая работа со стеком", task_4),
        '5': ("Стек с числами от 1 до n", task_5),
        '6': ("Слова в обратном порядке", task_6),
        '0': ("Выход", None)
    }

    while True:
        print("\n" + "-" * 40)
        print("ВЫБЕРИТЕ ЗАДАЧУ ДЛЯ ВЫПОЛНЕНИЯ:")
        for key, (description, _) in tasks.items():
            print(f"  {key}. {description}")

        choice = input("\nВаш выбор (0-6): ").strip()

        if choice == '0':
            print("\nПрограмма завершена. До свидания!")
            break

        if choice in tasks and tasks[choice][1]:
            tasks[choice][1]()
        else:
            print("Неверный выбор! Пожалуйста, введите число от 0 до 6.")

        input("\nНажмите Enter для продолжения...")


def run_all_tasks():
    """Запустить все задачи последовательно"""
    print("ЗАПУСК ВСЕХ ЗАДАЧ ПОСЛЕДОВАТЕЛЬНО")
    print("=" * 50)

    # Запуск всех задач
    task_1()
    input("\nНажмите Enter для перехода к задаче 2...")

    task_2()
    input("\nНажмите Enter для перехода к задаче 3...")

    task_3()
    input("\nНажмите Enter для перехода к задаче 4...")

    task_4()
    input("\nНажмите Enter для перехода к задаче 5...")

    task_5()
    input("\nНажмите Enter для перехода к задаче 6...")

    task_6()

    print("\n" + "=" * 50)
    print("ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ!")


def main():
    """Главная функция программы"""
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА: РАБОТА СО СТЕКОМ И ОЧЕРЕДЬЮ")
    print("=" * 60)

    while True:
        print("\n" + "-" * 40)
        print("РЕЖИМЫ РАБОТЫ:")
        print("  1. Меню с выбором задачи")
        print("  2. Запустить все задачи последовательно")
        print("  0. Выход")

        mode = input("\nВыберите режим (0-2): ").strip()

        if mode == '1':
            main_menu()
            break
        elif mode == '2':
            run_all_tasks()
            break
        elif mode == '0':
            print("\nПрограмма завершена. До свидания!")
            break
        else:
            print("Неверный выбор! Пожалуйста, введите 0, 1 или 2.")


if __name__ == "__main__":
    main()