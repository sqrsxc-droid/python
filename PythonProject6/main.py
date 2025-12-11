class Node:
    """Узел двунаправленного списка"""

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __str__(self):
        return str(self.data)


class DoublyLinkedList:
    """Двунаправленный список"""

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __str__(self):
        """Строковое представление списка"""
        if self.is_empty():
            return "[]"

        result = "["
        current = self.head
        while current:
            result += str(current.data)
            if current.next:
                result += " <-> "
            current = current.next
        result += "]"
        return result

    def __len__(self):
        """Возвращает длину списка"""
        return self.length

    def is_empty(self):
        """Проверка на пустоту списка"""
        return self.head is None

    def append(self, data):
        """Добавление элемента в конец списка"""
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.length += 1

    def prepend(self, data):
        """Добавление элемента в начало списка"""
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.length += 1

    def insert(self, index, data):
        """Вставка элемента в произвольную позицию"""
        if index < 0 or index > self.length:
            raise IndexError("Index out of range")

        if index == 0:
            self.prepend(data)
            return

        if index == self.length:
            self.append(data)
            return

        new_node = Node(data)
        current = self._get_node(index)

        new_node.prev = current.prev
        new_node.next = current
        current.prev.next = new_node
        current.prev = new_node

        self.length += 1

    def _get_node(self, index):
        """Получение узла по индексу (вспомогательный метод)"""
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")

        if index < self.length // 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self.length - 1 - index):
                current = current.prev

        return current

    def get(self, index):
        """Получение элемента по индексу"""
        node = self._get_node(index)
        return node.data

    def remove(self, index):
        """Удаление элемента по индексу"""
        if index < 0 or index >= self.length:
            raise IndexError("Index out of range")

        node_to_remove = self._get_node(index)

        if self.length == 1:
            self.head = None
            self.tail = None
        elif index == 0:
            self.head = node_to_remove.next
            self.head.prev = None
        elif index == self.length - 1:
            self.tail = node_to_remove.prev
            self.tail.next = None
        else:
            node_to_remove.prev.next = node_to_remove.next
            node_to_remove.next.prev = node_to_remove.prev

        self.length -= 1
        return node_to_remove.data

    def index_of(self, data):
        """Поиск индекса элемента (первого вхождения)"""
        current = self.head
        index = 0

        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1

        return -1

    def contains(self, data):
        """Проверка наличия элемента в списке"""
        return self.index_of(data) != -1

    def clear(self):
        """Очистка списка"""
        self.head = None
        self.tail = None
        self.length = 0

    def reverse(self):
        """Разворот списка"""
        if self.length <= 1:
            return

        current = self.head
        while current:
            temp = current.next
            current.next = current.prev
            current.prev = temp

            current = temp


        self.head, self.tail = self.tail, self.head

    def to_list(self):
        """Преобразование в обычный список Python"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def from_list(self, data_list):
        """Создание списка из обычного списка Python"""
        self.clear()
        for item in data_list:
            self.append(item)

    def __iter__(self):
        """Итератор для списка"""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def iterate_backward(self):
        """Итерация в обратном порядке"""
        current = self.tail
        while current:
            yield current.data
            current = current.prev


# Демонстрация работы класса
def demo_doubly_linked_list():
    """Демонстрация работы двунаправленного списка"""

    print("=== ДЕМОНСТРАЦИЯ РАБОТЫ ДВУНАПРАВЛЕННОГО СПИСКА ===")

    dll = DoublyLinkedList()

    print("\n1. Добавление элементов:")
    dll.append(10)
    dll.append(20)
    dll.append(30)
    dll.prepend(5)
    print(f"Список: {dll}")
    print(f"Длина списка: {len(dll)}")

    print("\n2. Вставка элемента на позицию 2:")
    dll.insert(2, 15)
    print(f"Список: {dll}")

    print("\n3. Получение элементов:")
    print(f"Элемент с индексом 0: {dll.get(0)}")
    print(f"Элемент с индексом 2: {dll.get(2)}")
    print(f"Элемент с индексом 4: {dll.get(4)}")

    print("\n4. Поиск элементов:")
    print(f"Индекс элемента 15: {dll.index_of(15)}")
    print(f"Индекс элемента 30: {dll.index_of(30)}")
    print(f"Индекс элемента 100: {dll.index_of(100)}")

    print("\n5. Проверка наличия элементов:")
    print(f"Содержит 20: {dll.contains(20)}")
    print(f"Содержит 50: {dll.contains(50)}")

    print("\n6. Удаление элементов:")
    print(f"Удаляем элемент с индексом 1: {dll.remove(1)}")
    print(f"Список после удаления: {dll}")

    print(f"Удаляем первый элемент: {dll.remove(0)}")
    print(f"Список после удаления: {dll}")


    print("\n7. Итерация по списку:")
    print("Прямой порядок:", end=" ")
    for item in dll:
        print(item, end=" ")
    print()

    print("Обратный порядок:", end=" ")
    for item in dll.iterate_backward():
        print(item, end=" ")
    print()

    print("\n8. Разворот списка:")
    dll.reverse()
    print(f"Список после разворота: {dll}")

    print("\n9. Преобразование в обычный список:")
    python_list = dll.to_list()
    print(f"Обычный список: {python_list}")

    print("\n10. Очистка списка:")
    dll.clear()
    print(f"Список после очистки: {dll}")
    print(f"Длина списка: {len(dll)}")
    print(f"Пустой ли список: {dll.is_empty()}")


def different_data_types_demo():
    """Демонстрация работы с разными типами данных"""

    print("\n" + "=" * 60)
    print("РАБОТА С РАЗНЫМИ ТИПАМИ ДАННЫХ:")
    print("=" * 60)

    mixed_list = DoublyLinkedList()


    mixed_list.append(42)
    mixed_list.append("Hello, World!")
    mixed_list.append(3.14)
    mixed_list.append([1, 2, 3])
    mixed_list.append({"name": "John"})
    mixed_list.append(True)

    print(f"Список с разными типами данных: {mixed_list}")

    # Доступ к элементам
    print(f"\nЭлементы списка:")
    for i, item in enumerate(mixed_list):
        print(f"  [{i}]: {item} (тип: {type(item).__name__})")

    print(f"\nДоступ к конкретным элементам:")
    print(f"  mixed_list.get(1): {mixed_list.get(1)}")
    print(f"  mixed_list.get(4): {mixed_list.get(4)}")


class StackUsingDLL:
    """Стек на основе двунаправленного списка"""

    def __init__(self):
        self.dll = DoublyLinkedList()

    def push(self, data):
        """Добавление элемента в стек"""
        self.dll.append(data)

    def pop(self):
        """Извлечение элемента из стека"""
        if self.dll.is_empty():
            raise IndexError("Stack is empty")
        return self.dll.remove(len(self.dll) - 1)

    def peek(self):
        """Просмотр верхнего элемента без извлечения"""
        if self.dll.is_empty():
            raise IndexError("Stack is empty")
        return self.dll.get(len(self.dll) - 1)

    def is_empty(self):
        return self.dll.is_empty()

    def __len__(self):
        return len(self.dll)

    def __str__(self):
        return str(self.dll)


class QueueUsingDLL:
    """Очередь на основе двунаправленного списка"""

    def __init__(self):
        self.dll = DoublyLinkedList()

    def enqueue(self, data):
        """Добавление элемента в очередь"""
        self.dll.append(data)

    def dequeue(self):
        """Извлечение элемента из очереди"""
        if self.dll.is_empty():
            raise IndexError("Queue is empty")
        return self.dll.remove(0)

    def front(self):
        """Просмотр первого элемента без извлечения"""
        if self.dll.is_empty():
            raise IndexError("Queue is empty")
        return self.dll.get(0)

    def is_empty(self):
        return self.dll.is_empty()

    def __len__(self):
        return len(self.dll)

    def __str__(self):
        return str(self.dll)


if __name__ == "__main__":
    demo_doubly_linked_list()

    different_data_types_demo()

    print("\n" + "=" * 60)
    print("РЕАЛИЗАЦИЯ СТЕКА И ОЧЕРЕДИ НА ОСНОВЕ ДВУНАПРАВЛЕННОГО СПИСКА")
    print("=" * 60)

    # Демонстрация стека
    print("\nСтек:")
    stack = StackUsingDLL()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"Стек после добавления 1, 2, 3: {stack}")
    print(f"Верхний элемент: {stack.peek()}")
    print(f"Извлекаем: {stack.pop()}")
    print(f"Стек после извлечения: {stack}")

    print("\nОчередь:")
    queue = QueueUsingDLL()
    queue.enqueue("A")
    queue.enqueue("B")
    queue.enqueue("C")
    print(f"Очередь после добавления A, B, C: {queue}")
    print(f"Первый элемент: {queue.front()}")
    print(f"Извлекаем: {queue.dequeue()}")
    print(f"Очередь после извлечения: {queue}")