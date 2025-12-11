"""
Работа с массивами (списками) в Python
B 1: Задачи по обработке массивов
"""
import random


def task_1():
    """Задача 1: Обработка массива X из N целых чисел"""
    print("\n" + "=" * 50)
    print("1. ОБРАБОТКА МАССИВА X ИЗ N ЦЕЛЫХ ЧИСЕЛ")
    print("=" * 50)

    # Ввод размера массива
    try:
        N = int(input("Введите размер массива N: "))
        if N <= 0:
            print("Размер массива должен быть положительным!")
            return
    except ValueError:
        print("Ошибка: введите целое число!")
        return

    # Создание массива
    print("\nСпособы создания массива:")
    print("1. Ввести элементы вручную")
    print("2. Сгенерировать случайные числа")

    choice = input("Выберите способ (1 или 2): ").strip()

    X = []
    if choice == '1':
        print(f"\nВведите {N} целых чисел:")
        for i in range(N):
            while True:
                try:
                    element = int(input(f"  X[{i}] = "))
                    X.append(element)
                    break
                except ValueError:
                    print("  Ошибка: введите целое число!")
    elif choice == '2':
        min_val = int(input("Минимальное значение: "))
        max_val = int(input("Максимальное значение: "))
        X = [random.randint(min_val, max_val) for _ in range(N)]
        print(f"\nСгенерированный массив: {X}")
    else:
        print("Неверный выбор, используется генерация по умолчанию (-10 до 10)")
        X = [random.randint(-10, 10) for _ in range(N)]
        print(f"Сгенерированный массив: {X}")

    # а) Вычисления
    print("\n" + "-" * 50)
    print("а) ВЫЧИСЛЕНИЯ:")

    # Количество положительных элементов
    positive_count = sum(1 for num in X if num > 0)
    print(f"  1. Количество положительных элементов: {positive_count}")

    # Сумма первых пяти элементов
    first_five_sum = sum(X[:5]) if len(X) >= 5 else sum(X)
    print(f"  2. Сумма первых пяти элементов: {first_five_sum}")

    # Минимум из четных элементов, стоящих на четных местах (индексы 0, 2, 4...)
    even_positions_even_values = []
    for i in range(0, len(X), 2):  # i = 0, 2, 4...
        if X[i] % 2 == 0:  # Элемент четный
            even_positions_even_values.append(X[i])

    if even_positions_even_values:
        min_even = min(even_positions_even_values)
        print(f"  3. Минимум из четных элементов на четных позициях: {min_even}")
        print(f"     (четные элементы на четных позициях: {even_positions_even_values})")
    else:
        print(f"  3. Нет четных элементов на четных позициях")

    # b) Все нечетные отрицательные элементы увеличить в 2 раза
    print("\n" + "-" * 50)
    print("b) УВЕЛИЧЕНИЕ НЕЧЕТНЫХ ОТРИЦАТЕЛЬНЫХ ЭЛЕМЕНТОВ В 2 РАЗА:")

    X_modified = X.copy()
    for i in range(len(X_modified)):
        if X_modified[i] < 0 and X_modified[i] % 2 != 0:  # Нечетный отрицательный
            X_modified[i] *= 2

    print(f"  Исходный массив:    {X}")
    print(f"  Модифицированный:   {X_modified}")

    # c) Упорядочить по убыванию четные элементы
    print("\n" + "-" * 50)
    print("c) СОРТИРОВКА ЧЕТНЫХ ЭЛЕМЕНТОВ ПО УБЫВАНИЮ:")

    # Создаем копию массива
    X_sorted_even = X.copy()

    # Находим все четные элементы и их индексы
    even_elements = []
    even_indices = []

    for i in range(len(X_sorted_even)):
        if X_sorted_even[i] % 2 == 0:
            even_elements.append(X_sorted_even[i])
            even_indices.append(i)

    # Сортируем четные элементы по убыванию
    even_elements.sort(reverse=True)

    # Заменяем четные элементы на отсортированные
    for idx, value in zip(even_indices, even_elements):
        X_sorted_even[idx] = value

    print(f"  Исходный массив:        {X}")
    print(f"  С четными по убыванию:  {X_sorted_even}")

    print("\n" + "-" * 50)
    print("ИТОГ по задаче 1:")
    print(f"Исходный массив X: {X}")
    print(f"Модифицированный (п.б): {X_modified}")
    print(f"С четными по убыванию (п.в): {X_sorted_even}")


def task_2():
    """Задача 2: Удалить первый отрицательный элемент массива P()"""
    print("\n" + "=" * 50)
    print("2. УДАЛЕНИЕ ПЕРВОГО ОТРИЦАТЕЛЬНОГО ЭЛЕМЕНТА")
    print("=" * 50)

    # Создание массива
    P = []
    while True:
        try:
            n = int(input("Введите размер массива P: "))
            if n > 0:
                break
            print("Размер должен быть положительным!")
        except ValueError:
            print("Ошибка: введите целое число!")

    print("\nЗаполнение массива P:")
    for i in range(n):
        while True:
            try:
                val = int(input(f"  P[{i}] = "))
                P.append(val)
                break
            except ValueError:
                print("  Ошибка: введите целое число!")

    print(f"\nИсходный массив P: {P}")

    # Поиск первого отрицательного элемента
    negative_index = -1
    for i in range(len(P)):
        if P[i] < 0:
            negative_index = i
            break

    if negative_index != -1:
        deleted_value = P.pop(negative_index)
        print(f"Удален первый отрицательный элемент: P[{negative_index}] = {deleted_value}")
        print(f"Массив P после удаления: {P}")
    else:
        print("В массиве P нет отрицательных элементов")
        print(f"Массив P остается без изменений: {P}")


def task_3():
    """Задача 3: Удалить из массива A(M) все положительные элементы"""
    print("\n" + "=" * 50)
    print("3. УДАЛЕНИЕ ВСЕХ ПОЛОЖИТЕЛЬНЫХ ЭЛЕМЕНТОВ ИЗ МАССИВА")
    print("=" * 50)

    # Создание массива
    M = int(input("Введите размер массива M: "))

    A = []
    print(f"\nВведите {M} элементов массива A:")
    for i in range(M):
        while True:
            try:
                val = int(input(f"  A[{i}] = "))
                A.append(val)
                break
            except ValueError:
                print("  Ошибка: введите целое число!")

    print(f"\nИсходный массив A({M}): {A}")

    # Удаление всех положительных элементов
    # Вариант 1: Создание нового массива без положительных элементов
    A_filtered = [num for num in A if num <= 0]

    # Вариант 2: Удаление на месте (менее эффективно)
    # i = 0
    # while i < len(A):
    #     if A[i] > 0:
    #         A.pop(i)
    #     else:
    #         i += 1

    removed_count = len(A) - len(A_filtered)

    print(f"\nУдалено положительных элементов: {removed_count}")

    if removed_count > 0:
        positive_elements = [num for num in A if num > 0]
        print(f"Удаленные элементы: {positive_elements}")

    print(f"Массив A после удаления положительных элементов: {A_filtered}")
    print(f"Новый размер массива: {len(A_filtered)}")


def task_4():
    """Задача 4: Вставить 100 перед каждым элементом массива A(M), кратным 5"""
    print("\n" + "=" * 50)
    print("4. ВСТАВКА 100 ПЕРЕД КАЖДЫМ ЭЛЕМЕНТОМ, КРАТНЫМ 5")
    print("=" * 50)

    # Создание массива
    try:
        M = int(input("Введите размер массива M: "))
        if M <= 0:
            print("Размер массива должен быть положительным!")
            return
    except ValueError:
        print("Ошибка: введите целое число!")
        return

    A = []
    print(f"\nВведите {M} элементов массива A:")
    for i in range(M):
        while True:
            try:
                val = int(input(f"  A[{i}] = "))
                A.append(val)
                break
            except ValueError:
                print("  Ошибка: введите целое число!")

    print(f"\nИсходный массив A({M}): {A}")

    # Поиск элементов, кратных 5, и вставка 100 перед ними
    # Работаем с конца, чтобы индексы не сдвигались
    result = []

    for num in A:
        if num % 5 == 0:  # Если элемент кратен 5
            result.append(100)  # Вставляем 100
        result.append(num)  # Добавляем сам элемент

    # Альтернативный способ с использованием индексов (менее эффективно):
    # i = 0
    # while i < len(A):
    #     if A[i] % 5 == 0:
    #         A.insert(i, 100)
    #         i += 2  # Пропускаем вставленный элемент и элемент, кратный 5
    #     else:
    #         i += 1

    multiples_of_5 = [num for num in A if num % 5 == 0]

    print(f"\nЭлементы, кратные 5: {multiples_of_5}")
    print(f"Количество элементов, кратных 5: {len(multiples_of_5)}")

    if multiples_of_5:
        print(f"Вставлено чисел 100: {len(multiples_of_5)}")
    else:
        print("В массиве нет элементов, кратных 5")

    print(f"\nМассив A после вставки 100: {result}")
    print(f"Новый размер массива: {len(result)}")


def task_5_demo():
    """Дополнительная демонстрация всех операций"""
    print("\n" + "=" * 50)
    print("5. ДЕМОНСТРАЦИЯ ВСЕХ ОПЕРАЦИЙ НА ПРИМЕРЕ")
    print("=" * 50)

    # Создаем демонстрационный массив
    demo_array = [12, -3, 8, 0, -7, 15, 4, -2, 10, 6]

    print(f"Демонстрационный массив: {demo_array}")
    print(f"Длина массива: {len(demo_array)}")
    print()

    # 1. а) Количество положительных элементов
    positive = [x for x in demo_array if x > 0]
    print(f"1.а) Положительные элементы: {positive}")
    print(f"    Количество: {len(positive)}")

    # 1. а) Сумма первых пяти элементов
    first_five = demo_array[:5]
    print(f"\n    Первые пять элементов: {first_five}")
    print(f"    Сумма: {sum(first_five)}")

    # 1. а) Минимум из четных элементов на четных позициях
    even_at_even = []
    for i in range(0, len(demo_array), 2):
        if demo_array[i] % 2 == 0:
            even_at_even.append(demo_array[i])
    print(f"\n    Четные элементы на четных позициях (индексы 0,2,4...): {even_at_even}")
    if even_at_even:
        print(f"    Минимум: {min(even_at_even)}")

    # 1. b) Увеличение нечетных отрицательных в 2 раза
    modified = demo_array.copy()
    for i in range(len(modified)):
        if modified[i] < 0 and modified[i] % 2 != 0:
            modified[i] *= 2
    print(f"\n1.b) После удвоения нечетных отрицательных: {modified}")

    # 1. c) Сортировка четных элементов по убыванию
    sorted_even = demo_array.copy()
    evens = []
    even_indices = []
    for i in range(len(sorted_even)):
        if sorted_even[i] % 2 == 0:
            evens.append(sorted_even[i])
            even_indices.append(i)
    evens.sort(reverse=True)
    for idx, val in zip(even_indices, evens):
        sorted_even[idx] = val
    print(f"1.c) С четными по убыванию: {sorted_even}")

    # 2. Удаление первого отрицательного
    array2 = demo_array.copy()
    for i in range(len(array2)):
        if array2[i] < 0:
            del array2[i]
            break
    print(f"\n2) После удаления первого отрицательного: {array2}")

    # 3. Удаление всех положительных
    array3 = demo_array.copy()
    array3 = [x for x in array3 if x <= 0]
    print(f"3) После удаления всех положительных: {array3}")

    # 4. Вставка 100 перед элементами, кратными 5
    array4 = demo_array.copy()
    result4 = []
    for num in array4:
        if num % 5 == 0:
            result4.append(100)
        result4.append(num)
    print(f"4) После вставки 100 перед элементами, кратными 5: {result4}")


def main():
    """Главное меню программы"""
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА: РАБОТА С МАССИВАМИ")
    print("B 1: Обработка одномерных массивов")
    print("=" * 60)

    tasks = {
        '1': ("Обработка массива X (подзадачи а, b, c)", task_1),
        '2': ("Удалить первый отрицательный элемент", task_2),
        '3': ("Удалить все положительные элементы", task_3),
        '4': ("Вставить 100 перед элементами, кратными 5", task_4),
        '5': ("Демонстрация всех операций", task_5_demo),
        '0': ("Выход", None)
    }

    while True:
        print("\n" + "-" * 40)
        print("ВЫБЕРИТЕ ЗАДАЧУ:")
        for key, (description, _) in tasks.items():
            print(f"  {key}. {description}")

        choice = input("\nВаш выбор (0-5): ").strip()

        if choice == '0':
            print("\nПрограмма завершена. До свидания!")
            break

        if choice in tasks and tasks[choice][1]:
            tasks[choice][1]()
        else:
            print("Неверный выбор! Пожалуйста, введите число от 0 до 5.")

        input("\nНажмите Enter для продолжения...")


def run_all_tasks():
    """Запустить все задачи последовательно"""
    print("ЗАПУСК ВСЕХ ЗАДАЧ ПОСЛЕДОВАТЕЛЬНО")
    print("=" * 50)

    task_1()
    input("\nНажмите Enter для перехода к задаче 2...")

    task_2()
    input("\nНажмите Enter для перехода к задаче 3...")

    task_3()
    input("\nНажмите Enter для перехода к задаче 4...")

    task_5_demo()

    print("\n" + "=" * 50)
    print("ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ!")


if __name__ == "__main__":
    print("=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА: РАБОТА С МАССИВАМИ")
    print("=" * 60)

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