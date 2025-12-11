"""
Работа со списками в Python
B1: Обработка списков
"""


def task_1():
    """Задача 1: Основные операции со списками"""
    print("\n" + "=" * 60)
    print("1. ОСНОВНЫЕ ОПЕРАЦИИ СО СПИСКАМИ")
    print("=" * 60)

    # 1. Создание списка с разными типами данных
    print("\n1. Создаем список с разными типами данных:")
    my_list = [10, 20, 30]  # три целых числа
    print(f"   После трех целых чисел: {my_list}")

    my_list.extend([3.14, 2.71, 1.618])  # три вещественных числа
    print(f"   После трех вещественных чисел: {my_list}")

    # Добавляем "заданное число" - пусть пользователь введет
    try:
        given_number = float(input("   Введите заданное число для добавления в список: "))
        my_list.append(given_number)
        print(f"   После добавления заданного числа: {my_list}")
    except ValueError:
        print("   Ошибка! Добавляем число 100 по умолчанию")
        my_list.append(100)
        print(f"   После добавления числа 100: {my_list}")

    my_list.extend(["Hello", "World", "Python", "Programming"])  # четыре строки
    print(f"   После четырех строк: {my_list}")

    # 2. Проверка вхождения элемента
    print("\n2. Проверка вхождения элемента:")
    search_item = input("   Введите элемент для поиска в списке: ")

    try:
        # Пробуем преобразовать в число, если возможно
        if '.' in search_item:
            search_item = float(search_item)
        else:
            search_item = int(search_item)
    except ValueError:
        pass  # Оставляем как строку

    if search_item in my_list:
        print(f"   Элемент '{search_item}' найден в списке!")
    else:
        print(f"   Элемент '{search_item}' не найден в списке.")

    # 3. Вставить на третье место число 20
    print("\n3. Вставляем число 20 на третье место (индекс 2):")
    my_list.insert(2, 20)
    print(f"   Список после вставки: {my_list}")

    # 4. Удалить последний элемент списка
    print("\n4. Удаляем последний элемент:")
    last_element = my_list.pop()
    print(f"   Удаленный элемент: '{last_element}'")
    print(f"   Список после удаления: {my_list}")

    # 5. Поменять местами первые два элемента
    print("\n5. Меняем местами первые два элемента:")
    print(f"   До замены: {my_list}")
    if len(my_list) >= 2:
        my_list[0], my_list[1] = my_list[1], my_list[0]
    print(f"   После замены: {my_list}")

    # 6. Создать новый список с последними тремя элементами
    print("\n6. Создаем новый список из последних трех элементов:")
    new_list = my_list[-3:] if len(my_list) >= 3 else my_list.copy()
    print(f"   Новый список: {new_list}")
    print(f"   Исходный список: {my_list}")

    # 7. Удалить из первого списка три первых элемента
    print("\n7. Удаляем три первых элемента из исходного списка:")
    if len(my_list) >= 3:
        deleted_elements = my_list[:3]
        del my_list[:3]
        print(f"   Удаленные элементы: {deleted_elements}")
    else:
        print(f"   В списке меньше 3 элементов, удаляем все")
        deleted_elements = my_list.copy()
        my_list.clear()
        print(f"   Удаленные элементы: {deleted_elements}")

    print(f"   Исходный список после удаления: {my_list}")

    # Итоговый результат
    print("\n" + "-" * 60)
    print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print(f"Исходный список (после всех операций): {my_list}")
    print(f"Новый список (последние 3 элемента): {new_list}")


def task_2():
    """Задача 2: Операции со списком чисел"""
    print("\n" + "=" * 60)
    print("2. ОПЕРАЦИИ СО СПИСКОМ ЧИСЕЛ")
    print("=" * 60)

    # 1. Создать список с числами от 1 до n
    try:
        n = int(input("Введите число n: "))
        if n <= 0:
            print("Число должно быть положительным! Используем n=10")
            n = 10
    except ValueError:
        print("Ошибка! Используем n=10")
        n = 10

    numbers = list(range(1, n + 1))
    print(f"\n1. Создан список чисел от 1 до {n}:")
    print(f"   {numbers}")

    # 2. Вставить на третье место число 11
    print("\n2. Вставляем число 11 на третье место (индекс 2):")
    numbers.insert(2, 11)
    print(f"   {numbers}")

    # 3. Удалить из списка число 3
    print("\n3. Удаляем число 3 из списка:")
    if 3 in numbers:
        numbers.remove(3)
        print(f"   Число 3 удалено")
    else:
        print(f"   Число 3 не найдено в списке")
    print(f"   {numbers}")

    # 4. Добавить в начало списка число 22
    print("\n4. Добавляем число 22 в начало списка:")
    numbers.insert(0, 22)
    print(f"   {numbers}")

    # 5. Найти индекс числа 11
    print("\n5. Находим индекс числа 11:")
    if 11 in numbers:
        index_11 = numbers.index(11)
        print(f"   Число 11 находится на позиции {index_11}")
    else:
        print(f"   Число 11 не найдено в списке")

    # 6. Отсортировать список
    print("\n6. Сортируем список:")
    numbers.sort()
    print(f"   Отсортированный список: {numbers}")

    # 7. Найти в списке число 11 (после сортировки)
    print("\n7. Ищем число 11 в отсортированном списке:")
    if 11 in numbers:
        index_11_sorted = numbers.index(11)
        print(f"   Число 11 найдено на позиции {index_11_sorted}")
    else:
        print(f"   Число 11 не найдено")

    # 8. Удалить второй и предпоследний элементы
    print("\n8. Удаляем второй и предпоследний элементы:")
    if len(numbers) >= 3:
        # Удаляем предпоследний элемент
        prelast_index = len(numbers) - 2
        prelast_value = numbers.pop(prelast_index)
        print(f"   Удален предпоследний элемент: {prelast_value}")

    if len(numbers) >= 2:
        # Удаляем второй элемент (индекс 1 после первого удаления)
        second_index = 1
        second_value = numbers.pop(second_index)
        print(f"   Удален второй элемент: {second_value}")

    print(f"   Список после удалений: {numbers}")

    # Итоговый результат
    print("\n" + "-" * 60)
    print("ИТОГОВЫЙ РЕЗУЛЬТАТ:")
    print(f"Финальный список: {numbers}")
    print(f"Длина списка: {len(numbers)}")


def task_3():
    """Задача 3: Работа с узлами списка"""
    print("\n" + "=" * 60)
    print("3. РАБОТА С УЗЛАМИ СПИСКА")
    print("=" * 60)

    # 1. Создать список с числами от 1 до n
    try:
        n = int(input("Введите число n: "))
        if n <= 0:
            print("Число должно быть положительным! Используем n=10")
            n = 10
    except ValueError:
        print("Ошибка! Используем n=10")
        n = 10

    nodes = list(range(1, n + 1))
    print(f"\n1. Создан список (узлы) от 1 до {n}:")
    print(f"   {nodes}")

    # 2. Вставить на первое место число 55
    print("\n2. Вставляем число 55 на первое место:")
    nodes.insert(0, 55)
    print(f"   {nodes}")

    # 3. Вставить до и после последнего узла число 88
    print("\n3. Вставляем 88 до и после последнего узла:")

    # Вставляем 88 после последнего узла (в конец)
    nodes.append(88)
    print(f"   После добавления 88 в конец: {nodes}")

    # Вставляем 88 перед последним узлом
    # Теперь последний узел - это добавленная 88, а предпоследний - исходный последний
    if len(nodes) >= 2:
        # Вставляем 88 перед последним элементом (перед предпоследней 88)
        nodes.insert(-1, 88)
        print(f"   После вставки 88 перед последним узлом: {nodes}")
    else:
        print(f"   Список слишком короткий для этой операции")

    # 4. Удалить последний узел из списка
    print("\n4. Удаляем последний узел из списка:")
    if nodes:
        last_node = nodes.pop()
        print(f"   Удален последний узел: {last_node}")
        print(f"   Список после удаления: {nodes}")
    else:
        print(f"   Список пуст")

    # Итоговый результат
    print("\n" + "-" * 60)
    print("ИТОГОВЫЙ РЕЗУЛЬТАТ:")
    print(f"Финальный список: {nodes}")
    print(f"Длина списка: {len(nodes)}")


def task_4_demo():
    """Дополнительная демонстрация методов списков"""
    print("\n" + "=" * 60)
    print("4. ДОПОЛНИТЕЛЬНАЯ ДЕМОНСТРАЦИЯ МЕТОДОВ СПИСКОВ")
    print("=" * 60)

    # Создаем демонстрационный список
    demo_list = [1, 2, 3, 4, 5]
    print(f"Исходный список: {demo_list}")

    print("\nМетоды списков в Python:")
    print("-" * 40)

    # 1. append() - добавить в конец
    demo_list.append(6)
    print(f"1. append(6): {demo_list}")

    # 2. extend() - расширить другим списком
    demo_list.extend([7, 8])
    print(f"2. extend([7, 8]): {demo_list}")

    # 3. insert() - вставить по индексу
    demo_list.insert(2, 99)
    print(f"3. insert(2, 99): {demo_list}")

    # 4. remove() - удалить по значению
    demo_list.remove(99)
    print(f"4. remove(99): {demo_list}")

    # 5. pop() - удалить по индексу (последний по умолчанию)
    popped = demo_list.pop()
    print(f"5. pop(): удален {popped}, список: {demo_list}")

    # 6. index() - найти индекс элемента
    idx = demo_list.index(4)
    print(f"6. index(4): элемент 4 на позиции {idx}")

    # 7. count() - подсчитать количество
    demo_list.append(3)
    cnt = demo_list.count(3)
    print(f"7. count(3): число 3 встречается {cnt} раз")

    # 8. sort() - отсортировать
    demo_list.sort()
    print(f"8. sort(): {demo_list}")

    # 9. reverse() - обратить порядок
    demo_list.reverse()
    print(f"9. reverse(): {demo_list}")

    # 10. copy() - создать копию
    copy_list = demo_list.copy()
    print(f"10. copy(): создана копия: {copy_list}")

    # 11. clear() - очистить
    demo_list.clear()
    print(f"11. clear(): исходный список очищен: {demo_list}")
    print(f"    копия сохранилась: {copy_list}")


def main():
    """Главное меню программы"""
    print("=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА: РАБОТА СО СПИСКАМИ В PYTHON")
    print("B1: Основные операции со списками")
    print("=" * 70)

    tasks = {
        '1': ("Основные операции со списками (задача 1)", task_1),
        '2': ("Операции со списком чисел (задача 2)", task_2),
        '3': ("Работа с узлами списка (задача 3)", task_3),
        '4': ("Демонстрация методов списков", task_4_demo),
        '0': ("Выход", None)
    }

    while True:
        print("\n" + "-" * 40)
        print("ВЫБЕРИТЕ ЗАДАЧУ:")
        for key, (description, _) in tasks.items():
            print(f"  {key}. {description}")

        choice = input("\nВаш выбор (0-4): ").strip()

        if choice == '0':
            print("\nПрограмма завершена. До свидания!")
            break

        if choice in tasks and tasks[choice][1]:
            tasks[choice][1]()
        else:
            print("Неверный выбор! Пожалуйста, введите число от 0 до 4.")

        input("\nНажмите Enter для продолжения...")


def run_all_tasks():
    """Запустить все задачи последовательно"""
    print("ЗАПУСК ВСЕХ ЗАДАЧ ПОСЛЕДОВАТЕЛЬНО")
    print("=" * 60)

    task_1()
    input("\nНажмите Enter для перехода к задаче 2...")

    task_2()
    input("\nНажмите Enter для перехода к задаче 3...")

    task_3()
    input("\nНажмите Enter для перехода к демонстрации...")

    task_4_demo()

    print("\n" + "=" * 60)
    print("ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ!")


if __name__ == "__main__":
    print("=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА: РАБОТА СО СПИСКАМИ В PYTHON")
    print("=" * 70)

    while True:
        print("\n" + "-" * 40)
        print("РЕЖИМЫ РАБОТЫ:")
        print("  1. Меню с выбором задачи")
        print("  2. Запустить все задачи последовательно")
        print("  0. Выход")

        mode = input("\nВыберите режим (0-2): ").strip()

        if mode == '1':
            main()
            break
        elif mode == '2':
            run_all_tasks()
            break
        elif mode == '0':
            print("\nПрограмма завершена. До свидания!")
            break
        else:
            print("Неверный выбор! Пожалуйста, введите 0, 1 или 2.")