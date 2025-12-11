import random
from collections import deque


class TreeNode:
    """Узел бинарного дерева"""

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.value)


class BinaryTree:
    """Класс бинарного дерева"""

    def __init__(self):
        self.root = None

    def insert(self, value):
        """Вставка элемента в бинарное дерево"""
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        """Рекурсивная вставка элемента"""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def delete(self, value):
        """Удаление элемента из дерева"""
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        """Рекурсивное удаление элемента"""
        if node is None:
            return node

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Узел найден
            # Узел с одним или без детей
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Узел с двумя детьми
            # Находим минимальный элемент в правом поддереве
            min_node = self._find_min(node.right)
            node.value = min_node.value
            node.right = self._delete_recursive(node.right, min_node.value)

        return node

    def _find_min(self, node):
        """Нахождение минимального элемента в поддереве"""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def contains(self, value):
        """Проверка наличия элемента в дереве"""
        return self._contains_recursive(self.root, value)

    def _contains_recursive(self, node, value):
        if node is None:
            return False

        if node.value == value:
            return True
        elif value < node.value:
            return self._contains_recursive(node.left, value)
        else:
            return self._contains_recursive(node.right, value)

    # Обходы дерева
    def inorder(self):
        """Центрированный обход (левый-корень-правый)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder(self):
        """Прямой обход (корень-левый-правый)"""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder(self):
        """Обратный обход (левый-правый-корень)"""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def level_order(self):
        """Обход по уровням (ширина)"""
        if not self.root:
            return []

        result = []
        queue = deque([self.root])

        while queue:
            node = queue.popleft()
            result.append(node.value)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    def print_tree(self):
        """Визуальный вывод дерева"""
        if not self.root:
            print("Дерево пустое")
            return

        lines = self._build_tree_string(self.root, 0, '')[0]
        print("\n" + "=" * 50)
        print("ВИЗУАЛЬНОЕ ПРЕДСТАВЛЕНИЕ ДЕРЕВА:")
        print("=" * 50)
        for line in lines:
            print(line)

    def _build_tree_string(self, node, level, prefix):
        """Рекурсивное построение строк для визуализации дерева"""
        if node is None:
            return [], 0, 0, 0

        left_lines, left_pos, left_width, left_height = self._build_tree_string(
            node.left, level + 1, 'L--- '
        )
        right_lines, right_pos, right_width, right_height = self._build_tree_string(
            node.right, level + 1, 'R--- '
        )

        value_str = str(node.value)
        value_width = len(value_str)

        # Определяем позиции
        left_middle = left_width // 2
        right_middle = right_width // 2

        # Создаем строку для текущего узла
        lines = []

        # Строка со значением
        if left_lines or right_lines:
            line = ' ' * left_pos + value_str + ' ' * (right_width - right_pos)
        else:
            line = value_str

        lines.append(line)

        # Строки с соединениями
        if left_lines or right_lines:
            if left_lines:
                lines.extend(left_lines)
            if right_lines:
                lines.extend(right_lines)

        return lines, left_middle, left_width + value_width + right_width, max(left_height, right_height) + 1

    def max_depth(self):
        """Максимальная глубина дерева (задача 4)"""
        return self._max_depth_recursive(self.root)

    def _max_depth_recursive(self, node):
        if node is None:
            return 0
        left_depth = self._max_depth_recursive(node.left)
        right_depth = self._max_depth_recursive(node.right)
        return max(left_depth, right_depth) + 1

    def count_full_nodes(self):
        """Количество узлов с обоими потомками (задача 5)"""
        return self._count_full_nodes_recursive(self.root)

    def _count_full_nodes_recursive(self, node):
        if node is None:
            return 0

        count = 0
        if node.left and node.right:
            count = 1

        count += self._count_full_nodes_recursive(node.left)
        count += self._count_full_nodes_recursive(node.right)

        return count

    def is_symmetric(self):
        """Проверка на симметричность (задача 6)"""
        if self.root is None:
            return True
        return self._is_mirror(self.root.left, self.root.right)

    def _is_mirror(self, left, right):
        if left is None and right is None:
            return True
        if left is None or right is None:
            return False
        if left.value != right.value:
            return False
        return (self._is_mirror(left.left, right.right) and
                self._is_mirror(left.right, right.left))


# Задача 1: Дерево со случайными числами
def task1():
    print("=" * 60)
    print("ЗАДАНИЕ 1: Дерево с 7 случайными числами")
    print("=" * 60)

    tree = BinaryTree()
    random_numbers = random.sample(range(1, 101), 7)

    print(f"Добавляем случайные числа: {random_numbers}")
    for num in random_numbers:
        tree.insert(num)

    tree.print_tree()

    print("\nРазличные способы обхода:")
    print(f"Прямой обход (preorder): {tree.preorder()}")
    print(f"Центрированный обход (inorder): {tree.inorder()}")
    print(f"Обратный обход (postorder): {tree.postorder()}")
    print(f"Обход по уровням: {tree.level_order()}")


# Задача 2: Удаление элемента из дерева
def task2():
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 2: Удаление элемента из дерева")
    print("=" * 60)

    tree = BinaryTree()
    elements = [50, 30, 70, 20, 40, 60, 80]

    print(f"Добавляем элементы: {elements}")
    for elem in elements:
        tree.insert(elem)

    print("\nДерево по уровням до удаления:")
    print(f"Уровни: {tree.level_order()}")
    tree.print_tree()

    # Запрос элемента для удаления
    try:
        to_delete = int(input("\nВведите элемент для удаления: "))
        if tree.contains(to_delete):
            tree.delete(to_delete)
            print(f"\nЭлемент {to_delete} удален.")
            print("\nДерево по уровням после удаления:")
            print(f"Уровни: {tree.level_order()}")
            tree.print_tree()
        else:
            print(f"Элемент {to_delete} не найден в дереве.")
    except ValueError:
        print("Ошибка: введите целое число.")


# Задача 3: Создание конкретного дерева
def task3():
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 3: Создание заданного дерева")
    print("=" * 60)

    # Создаем дерево вручную, чтобы получить нужную структуру
    tree = BinaryTree()

    # Создаем узлы
    root = TreeNode(50)

    # Первый уровень
    node30 = TreeNode(30)
    node60 = TreeNode(60)
    root.left = node30
    root.right = node60

    # Второй уровень
    node30.left = TreeNode(20)
    node30.right = TreeNode(40)
    node60.left = TreeNode(50)  # Дубликат значения
    node60.right = TreeNode(70)

    tree.root = root

    print("Структура дерева:")
    print("       50")
    print("     /    \\")
    print("   30      60")
    print("  /  \\    /  \\")
    print("20   40  50   70")

    print("\nВизуальное представление:")
    tree.print_tree()

    print("\nОбход по уровням:")
    print(tree.level_order())


# Задача 4: Максимальная глубина дерева
def task4():
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 4: Максимальная глубина дерева")
    print("=" * 60)

    # Создаем тестовое дерево
    tree = BinaryTree()
    test_values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

    for val in test_values:
        tree.insert(val)

    print("Тестовое дерево:")
    tree.print_tree()

    max_depth = tree.max_depth()
    print(f"\nМаксимальная глубина дерева: {max_depth}")

    # Демонстрация глубины листьев
    print("\nГлубины некоторых листьев:")
    print("Корень 50 имеет глубину 1")
    print(f"Лист 10 имеет глубину 4 (50->30->20->10)")
    print(f"Лист 45 имеет глубину 4 (50->30->40->45)")


# Задача 5: Узлы с обоими потомками
def task5():
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 5: Узлы с обоими потомками")
    print("=" * 60)

    # Создаем тестовое дерево
    tree = BinaryTree()
    test_values = [50, 30, 70, 20, 40, 60, 80, 10, 35, 55, 75]

    for val in test_values:
        tree.insert(val)

    print("Тестовое дерево:")
    tree.print_tree()

    full_nodes_count = tree.count_full_nodes()
    print(f"\nКоличество узлов с обоими потомками: {full_nodes_count}")

    # Покажем какие именно узлы полные
    print("\nПолные узлы (имеют и левого, и правого потомка):")

    def print_full_nodes(node):
        if node:
            if node.left and node.right:
                print(f"Узел {node.value}")
            print_full_nodes(node.left)
            print_full_nodes(node.right)

    print_full_nodes(tree.root)


# Задача 6: Проверка на симметричность
def task6():
    print("\n" + "=" * 60)
    print("ЗАДАНИЕ 6: Проверка дерева на симметричность")
    print("=" * 60)

    # Создаем симметричное дерево
    sym_tree = BinaryTree()
    sym_root = TreeNode(1)
    sym_root.left = TreeNode(2)
    sym_root.right = TreeNode(2)
    sym_root.left.left = TreeNode(3)
    sym_root.left.right = TreeNode(4)
    sym_root.right.left = TreeNode(4)
    sym_root.right.right = TreeNode(3)
    sym_tree.root = sym_root

    print("Симметричное дерево:")
    print("       1")
    print("     /   \\")
    print("   2       2")
    print("  / \\     / \\")
    print(" 3   4   4   3")

    print("\nВизуальное представление:")
    sym_tree.print_tree()
    print(f"\nДерево симметрично: {sym_tree.is_symmetric()}")

    # Создаем несимметричное дерево
    asym_tree = BinaryTree()
    asym_root = TreeNode(1)
    asym_root.left = TreeNode(2)
    asym_root.right = TreeNode(2)
    asym_root.left.right = TreeNode(3)
    asym_root.right.right = TreeNode(3)
    asym_tree.root = asym_root

    print("\n\nНесимметричное дерево:")
    print("     1")
    print("   /   \\")
    print("  2     2")
    print("   \\     \\")
    print("    3     3")

    print("\nВизуальное представление:")
    asym_tree.print_tree()
    print(f"\nДерево симметрично: {asym_tree.is_symmetric()}")


def main():
    """Главная функция запуска всех заданий"""
    print("ЛАБОРАТОРНАЯ РАБОТА ПО БИНАРНЫМ ДЕРЕВЬЯМ")
    print("=" * 60)

    # Запуск всех заданий
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()

    print("\n" + "=" * 60)
    print("ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ!")
    print("=" * 60)


if __name__ == "__main__":
    main()