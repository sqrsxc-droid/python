import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QPushButton, QTextEdit,
                             QRadioButton, QLabel, QButtonGroup, QMessageBox)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont, QKeySequence


class CurrencyConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Настройка главного окна
        self.setWindowTitle('Конвертер валют')
        self.setFixedSize(500, 500)

        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной макет
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Курсы валют
        self.usd_to_rub_rate = 90.0
        self.rub_to_usd_rate = 1.0 / self.usd_to_rub_rate  # 0.011111...

        # Виджеты интерфейса
        self.create_widgets(main_layout)

        # Подключение сигналов
        self.connect_signals()

        # Установка фокуса
        self.amount_input.setFocus()

    def create_widgets(self, layout):
        # Заголовок
        title = QLabel('Конвертер валют USD ↔ RUB')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Информация о курсе
        rate_info = QLabel(f'Курс: 1 USD = {self.usd_to_rub_rate:.2f} RUB | 1 RUB = {self.rub_to_usd_rate:.4f} USD')
        rate_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(rate_info)

        # Поле ввода суммы
        amount_layout = QVBoxLayout()
        amount_label = QLabel('Введите сумму:')
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('Введите сумму для конвертации...')
        self.amount_input.setFont(QFont('Arial', 12))
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        layout.addLayout(amount_layout)

        # Радиокнопки для выбора направления
        radio_layout = QHBoxLayout()

        self.usd_to_rub_radio = QRadioButton('USD → RUB')
        self.usd_to_rub_radio.setChecked(True)  # Выбрано по умолчанию
        self.usd_to_rub_radio.setFont(QFont('Arial', 11))

        self.rub_to_usd_radio = QRadioButton('RUB → USD')
        self.rub_to_usd_radio.setFont(QFont('Arial', 11))

        # Группа радиокнопок
        self.direction_group = QButtonGroup()
        self.direction_group.addButton(self.usd_to_rub_radio)
        self.direction_group.addButton(self.rub_to_usd_radio)

        radio_layout.addWidget(self.usd_to_rub_radio)
        radio_layout.addWidget(self.rub_to_usd_radio)
        radio_layout.addStretch()
        layout.addLayout(radio_layout)

        # Кнопка конвертации
        self.convert_button = QPushButton('Конвертировать')
        self.convert_button.setFont(QFont('Arial', 12, QFont.Bold))
        self.convert_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        layout.addWidget(self.convert_button)

        # Поле результата
        result_layout = QVBoxLayout()
        result_label = QLabel('Результат:')
        self.result_display = QLineEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFont(QFont('Arial', 12))
        self.result_display.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 5px;
            }
        """)
        result_layout.addWidget(result_label)
        result_layout.addWidget(self.result_display)
        layout.addLayout(result_layout)

        # История операций
        history_layout = QVBoxLayout()
        history_label = QLabel('История операций:')
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setFont(QFont('Courier New', 10))
        self.history_text.setMaximumHeight(200)

        # Добавляем начальное сообщение в историю
        self.history_text.append(f"{'=' * 50}")
        self.history_text.append("Начало работы конвертера")
        self.history_text.append(f"{'=' * 50}")

        history_layout.addWidget(history_label)
        history_layout.addWidget(self.history_text)
        layout.addLayout(history_layout)

        # Кнопка очистки истории
        clear_button = QPushButton('Очистить историю')
        clear_button.setFont(QFont('Arial', 10))
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        clear_button.clicked.connect(self.clear_history)
        layout.addWidget(clear_button)

        layout.addStretch()

    def connect_signals(self):
        # Кнопка конвертации
        self.convert_button.clicked.connect(self.convert_currency)

        # Enter в поле ввода
        self.amount_input.returnPressed.connect(self.convert_currency)

        # Изменение направления конвертации
        self.direction_group.buttonClicked.connect(self.on_direction_changed)

        # Горячие клавиши
        self.amount_input.returnPressed.connect(self.convert_currency)

    def convert_currency(self):
        """Конвертация валюты"""
        try:
            # Получение суммы из поля ввода
            amount_text = self.amount_input.text().strip()

            if not amount_text:
                QMessageBox.warning(self, 'Ошибка', 'Введите сумму для конвертации!')
                return

            # Проверка корректности ввода
            amount = float(amount_text)
            if amount <= 0:
                QMessageBox.warning(self, 'Ошибка', 'Сумма должна быть положительной!')
                return

            # Определение направления конвертации
            if self.usd_to_rub_radio.isChecked():
                result = amount * self.usd_to_rub_rate
                operation = f"{amount:.2f} USD → {result:.2f} RUB"
                self.result_display.setText(f"{result:.2f} RUB")
            else:
                result = amount * self.rub_to_usd_rate
                operation = f"{amount:.2f} RUB → {result:.4f} USD"
                self.result_display.setText(f"{result:.4f} USD")

            # Добавление операции в историю
            self.add_to_history(operation)

            # Автоматическая очистка поля ввода
            self.amount_input.clear()
            self.amount_input.setFocus()

        except ValueError:
            QMessageBox.critical(self, 'Ошибка', 'Введите корректное число!')
            self.amount_input.clear()
            self.amount_input.setFocus()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Произошла ошибка: {str(e)}')

    def on_direction_changed(self):
        """Обработчик изменения направления конвертации"""
        # Очистка поля ввода при смене направления
        self.amount_input.clear()
        self.result_display.clear()

        # Установка фокуса на поле ввода
        self.amount_input.setFocus()

        # Добавление сообщения в историю
        if self.usd_to_rub_radio.isChecked():
            self.add_to_history("Направление изменено: USD → RUB")
        else:
            self.add_to_history("Направление изменено: RUB → USD")

    def add_to_history(self, operation):
        """Добавление операции в историю"""
        timestamp = QDateTime.currentDateTime().toString("dd.MM.yyyy HH:mm:ss")
        history_entry = f"[{timestamp}] {operation}"

        # Добавляем в начало истории (сверху)
        current_text = self.history_text.toPlainText()
        if len(current_text.split('\n')) > 30:  # Ограничиваем историю
            lines = current_text.split('\n')
            self.history_text.setPlainText('\n'.join(lines[:-5]))

        # Вставляем новую запись после разделителя
        current_text = self.history_text.toPlainText()
        lines = current_text.split('\n')
        if len(lines) > 3 and '=' in lines[2]:
            # Вставляем после разделителя
            new_text = '\n'.join(lines[:3]) + '\n' + history_entry + '\n' + '\n'.join(lines[3:])
            self.history_text.setPlainText(new_text)
        else:
            self.history_text.append(history_entry)

        # Прокрутка к началу
        cursor = self.history_text.textCursor()
        cursor.movePosition(cursor.Start)
        self.history_text.setTextCursor(cursor)

    def clear_history(self):
        """Очистка истории операций"""
        reply = QMessageBox.question(self, 'Очистка истории',
                                     'Вы уверены, что хотите очистить историю операций?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.history_text.clear()
            self.history_text.append(f"{'=' * 50}")
            self.history_text.append("История очищена")
            self.history_text.append(f"{QDateTime.currentDateTime().toString('dd.MM.yyyy HH:mm:ss')}")
            self.history_text.append(f"{'=' * 50}")

            # Добавляем сообщение в результат
            self.result_display.setText("История очищена")
            QMessageBox.information(self, 'Успех', 'История операций очищена!')


def main():
    app = QApplication(sys.argv)

    # Установка стиля приложения
    app.setStyle('Fusion')

    # Установка шрифта по умолчанию
    font = QFont('Arial', 10)
    app.setFont(font)

    converter = CurrencyConverter()
    converter.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()