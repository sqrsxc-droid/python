import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QSlider, QProgressBar,
                             QLabel, QGroupBox, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor


class CharacterCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.total_points = 200
        self.initUI()

    def initUI(self):
        # Настройка главного окна
        self.setWindowTitle('Создание игрового персонажа')
        self.setFixedSize(600, 600)

        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной макет
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Виджеты интерфейса
        self.create_widgets(main_layout)

        # Инициализация значений
        self.update_points()
        self.determine_class()

    def create_widgets(self, layout):
        # Заголовок
        title = QLabel('СОЗДАНИЕ ПЕРСОНАЖА')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 15px;")
        layout.addWidget(title)

        # Имя персонажа
        name_group = QGroupBox('Имя персонажа')
        name_group.setFont(QFont('Arial', 11, QFont.Bold))
        name_layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Введите имя персонажа...')
        self.name_input.setFont(QFont('Arial', 12))
        self.name_input.setMaxLength(20)
        self.name_input.textChanged.connect(self.on_name_changed)

        name_layout.addWidget(self.name_input)
        name_group.setLayout(name_layout)
        layout.addWidget(name_group)

        # Прогресс-бар очков
        points_group = QGroupBox('Очки характеристик')
        points_group.setFont(QFont('Arial', 11, QFont.Bold))
        points_layout = QVBoxLayout()

        # Метка с оставшимися очками
        self.points_label = QLabel(f'Осталось очков: {self.total_points}')
        self.points_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.points_label.setAlignment(Qt.AlignCenter)

        # Прогресс-бар
        self.points_progress = QProgressBar()
        self.points_progress.setRange(0, self.total_points)
        self.points_progress.setValue(self.total_points)
        self.points_progress.setTextVisible(True)
        self.points_progress.setFormat('%v / %m очков')
        self.points_progress.setFont(QFont('Arial', 10))

        points_layout.addWidget(self.points_label)
        points_layout.addWidget(self.points_progress)
        points_group.setLayout(points_layout)
        layout.addWidget(points_group)

        # Характеристики
        self.create_attribute_sliders(layout)

        # Класс персонажа
        self.create_class_display(layout)

        # Кнопки управления
        self.create_control_buttons(layout)

        layout.addStretch()

    def create_attribute_sliders(self, layout):
        """Создание слайдеров для характеристик"""
        attributes_group = QGroupBox('Характеристики персонажа')
        attributes_group.setFont(QFont('Arial', 11, QFont.Bold))
        attributes_layout = QVBoxLayout()

        # Сила
        strength_layout = QVBoxLayout()
        strength_header = QHBoxLayout()

        strength_label = QLabel('💪 СИЛА')
        strength_label.setFont(QFont('Arial', 11, QFont.Bold))
        strength_header.addWidget(strength_label)

        self.strength_value = QLabel('0')
        self.strength_value.setFont(QFont('Arial', 11, QFont.Bold))
        self.strength_value.setStyleSheet("color: #e74c3c;")
        strength_header.addStretch()
        strength_header.addWidget(self.strength_value)

        strength_layout.addLayout(strength_header)

        self.strength_slider = QSlider(Qt.Horizontal)
        self.strength_slider.setRange(0, 100)
        self.strength_slider.setValue(0)
        self.strength_slider.valueChanged.connect(self.on_strength_changed)
        strength_layout.addWidget(self.strength_slider)

        attributes_layout.addLayout(strength_layout)

        # Ловкость
        agility_layout = QVBoxLayout()
        agility_header = QHBoxLayout()

        agility_label = QLabel('🏹 ЛОВКОСТЬ')
        agility_label.setFont(QFont('Arial', 11, QFont.Bold))
        agility_header.addWidget(agility_label)

        self.agility_value = QLabel('0')
        self.agility_value.setFont(QFont('Arial', 11, QFont.Bold))
        self.agility_value.setStyleSheet("color: #27ae60;")
        agility_header.addStretch()
        agility_header.addWidget(self.agility_value)

        agility_layout.addLayout(agility_header)

        self.agility_slider = QSlider(Qt.Horizontal)
        self.agility_slider.setRange(0, 100)
        self.agility_slider.setValue(0)
        self.agility_slider.valueChanged.connect(self.on_agility_changed)
        agility_layout.addWidget(self.agility_slider)

        attributes_layout.addLayout(agility_layout)

        # Интеллект
        intelligence_layout = QVBoxLayout()
        intelligence_header = QHBoxLayout()

        intelligence_label = QLabel('🧠 ИНТЕЛЛЕКТ')
        intelligence_label.setFont(QFont('Arial', 11, QFont.Bold))
        intelligence_header.addWidget(intelligence_label)

        self.intelligence_value = QLabel('0')
        self.intelligence_value.setFont(QFont('Arial', 11, QFont.Bold))
        self.intelligence_value.setStyleSheet("color: #3498db;")
        intelligence_header.addStretch()
        intelligence_header.addWidget(self.intelligence_value)

        intelligence_layout.addLayout(intelligence_header)

        self.intelligence_slider = QSlider(Qt.Horizontal)
        self.intelligence_slider.setRange(0, 100)
        self.intelligence_slider.setValue(0)
        self.intelligence_slider.valueChanged.connect(self.on_intelligence_changed)
        intelligence_layout.addWidget(self.intelligence_slider)

        attributes_layout.addLayout(intelligence_layout)

        attributes_group.setLayout(attributes_layout)
        layout.addWidget(attributes_group)

    def create_class_display(self, layout):
        """Создание отображения класса персонажа"""
        class_group = QGroupBox('Класс персонажа')
        class_group.setFont(QFont('Arial', 11, QFont.Bold))
        class_layout = QVBoxLayout()

        # Иконка класса
        self.class_icon = QLabel('❓')
        self.class_icon.setFont(QFont('Arial', 48))
        self.class_icon.setAlignment(Qt.AlignCenter)

        # Название класса
        self.class_name = QLabel('Не определен')
        self.class_name.setFont(QFont('Arial', 14, QFont.Bold))
        self.class_name.setAlignment(Qt.AlignCenter)
        self.class_name.setStyleSheet("color: #9b59b6;")

        # Описание класса
        self.class_description = QLabel('Распределите очки характеристик, чтобы определить класс')
        self.class_description.setFont(QFont('Arial', 10))
        self.class_description.setAlignment(Qt.AlignCenter)
        self.class_description.setWordWrap(True)

        class_layout.addWidget(self.class_icon)
        class_layout.addWidget(self.class_name)
        class_layout.addWidget(self.class_description)
        class_group.setLayout(class_layout)
        layout.addWidget(class_group)

    def create_control_buttons(self, layout):
        """Создание кнопок управления"""
        buttons_layout = QHBoxLayout()

        # Кнопка сброса
        self.reset_button = QPushButton('🔄 Сбросить')
        self.reset_button.setFont(QFont('Arial', 11))
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.reset_button.clicked.connect(self.reset_character)
        buttons_layout.addWidget(self.reset_button)

        # Кнопка сохранения
        self.save_button = QPushButton('💾 Сохранить персонажа')
        self.save_button.setFont(QFont('Arial', 11, QFont.Bold))
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.save_button.clicked.connect(self.save_character)
        buttons_layout.addWidget(self.save_button)

        layout.addLayout(buttons_layout)

    def on_name_changed(self):
        """Обработчик изменения имени"""
        name = self.name_input.text().strip()
        if name:
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    def on_strength_changed(self):
        """Обработчик изменения силы"""
        value = self.strength_slider.value()
        self.strength_value.setText(str(value))
        self.update_points()
        self.update_sliders_state()
        self.determine_class()

    def on_agility_changed(self):
        """Обработчик изменения ловкости"""
        value = self.agility_slider.value()
        self.agility_value.setText(str(value))
        self.update_points()
        self.update_sliders_state()
        self.determine_class()

    def on_intelligence_changed(self):
        """Обработчик изменения интеллекта"""
        value = self.intelligence_slider.value()
        self.intelligence_value.setText(str(value))
        self.update_points()
        self.update_sliders_state()
        self.determine_class()

    def update_points(self):
        """Обновление оставшихся очков"""
        strength = self.strength_slider.value()
        agility = self.agility_slider.value()
        intelligence = self.intelligence_slider.value()

        used_points = strength + agility + intelligence
        remaining_points = self.total_points - used_points

        # Обновление метки
        self.points_label.setText(f'Осталось очков: {remaining_points}')

        # Обновление прогресс-бара
        self.points_progress.setValue(remaining_points)

        # Изменение цвета прогресс-бара в зависимости от оставшихся очков
        if remaining_points == 0:
            self.points_progress.setStyleSheet("""
                QProgressBar {
                    border: 2px solid #2c3e50;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #e74c3c;
                    border-radius: 3px;
                }
            """)
        elif remaining_points < 50:
            self.points_progress.setStyleSheet("""
                QProgressBar {
                    border: 2px solid #2c3e50;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #f39c12;
                    border-radius: 3px;
                }
            """)
        else:
            self.points_progress.setStyleSheet("""
                QProgressBar {
                    border: 2px solid #2c3e50;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #2ecc71;
                    border-radius: 3px;
                }
            """)

        return remaining_points

    def update_sliders_state(self):
        """Обновление состояния слайдеров в зависимости от оставшихся очков"""
        remaining_points = self.update_points()

        # Получаем текущие значения
        strength = self.strength_slider.value()
        agility = self.agility_slider.value()
        intelligence = self.intelligence_slider.value()

        # Блокируем слайдеры если очки закончились
        if remaining_points <= 0:
            # Сохраняем текущие значения перед блокировкой
            current_values = {
                'strength': strength,
                'agility': agility,
                'intelligence': intelligence
            }

            # Блокируем все слайдеры
            self.strength_slider.setEnabled(False)
            self.agility_slider.setEnabled(False)
            self.intelligence_slider.setEnabled(False)

            # Восстанавливаем значения после блокировки
            QTimer.singleShot(100, lambda: self.restore_slider_values(current_values))
        else:
            # Разблокируем все слайдеры
            self.strength_slider.setEnabled(True)
            self.agility_slider.setEnabled(True)
            self.intelligence_slider.setEnabled(True)

    def restore_slider_values(self, values):
        """Восстановление значений слайдеров после блокировки"""
        self.strength_slider.blockSignals(True)
        self.agility_slider.blockSignals(True)
        self.intelligence_slider.blockSignals(True)

        self.strength_slider.setValue(values['strength'])
        self.agility_slider.setValue(values['agility'])
        self.intelligence_slider.setValue(values['intelligence'])

        self.strength_slider.blockSignals(False)
        self.agility_slider.blockSignals(False)
        self.intelligence_slider.blockSignals(False)

    def determine_class(self):
        """Определение класса персонажа на основе характеристик"""
        strength = self.strength_slider.value()
        agility = self.agility_slider.value()
        intelligence = self.intelligence_slider.value()

        # Проверяем условия для каждого класса
        if strength > 70 and agility <= 70 and intelligence <= 70:
            class_info = {
                'icon': '⚔️',
                'name': 'ВОИН',
                'description': 'Могучий воин с выдающейся физической силой. Специализируется на ближнем бою и ношении тяжелых доспехов.'
            }
        elif agility > 70 and strength <= 70 and intelligence <= 70:
            class_info = {
                'icon': '🏹',
                'name': 'ЛУЧНИК',
                'description': 'Искусный стрелок с невероятной ловкостью. Мастер дальнего боя и скрытного передвижения.'
            }
        elif intelligence > 70 and strength <= 70 and agility <= 70:
            class_info = {
                'icon': '🔮',
                'name': 'МАГ',
                'description': 'Мудрый волшебник с выдающимся интеллектом. Владеет мощными заклинаниями и магическими искусствами.'
            }
        elif strength > 70 and agility > 70 and intelligence <= 70:
            class_info = {
                'icon': '⚔️🏹',
                'name': 'ВОИН-ЛУЧНИК',
                'description': 'Универсальный боец, сочетающий силу и ловкость. Эффективен как в ближнем, так и в дальнем бою.'
            }
        elif strength > 70 and intelligence > 70 and agility <= 70:
            class_info = {
                'icon': '⚔️🔮',
                'name': 'ВОИН-МАГ',
                'description': 'Рыцарь-чародей, объединяющий физическую мощь с магическими знаниями. Носит магические доспехи.'
            }
        elif agility > 70 and intelligence > 70 and strength <= 70:
            class_info = {
                'icon': '🏹🔮',
                'name': 'ЛУЧНИК-МАГ',
                'description': 'Волшебный стрелок, сочетающий ловкость с магией. Стреляет магическими стрелами.'
            }
        elif strength > 70 and agility > 70 and intelligence > 70:
            class_info = {
                'icon': '👑',
                'name': 'ЛЕГЕНДА',
                'description': 'Идеально сбалансированный герой, превосходящий во всех аспектах. Встречается крайне редко.'
            }
        elif strength == agility == intelligence:
            class_info = {
                'icon': '⚖️',
                'name': 'УНИВЕРСАЛ',
                'description': 'Сбалансированный персонаж без выраженных сильных сторон, но и без слабых мест.'
            }
        else:
            class_info = {
                'icon': '❓',
                'name': 'НЕ ОПРЕДЕЛЕН',
                'description': 'Продолжайте распределять очки характеристик, чтобы определить класс персонажа.'
            }

        # Обновление отображения
        self.class_icon.setText(class_info['icon'])
        self.class_name.setText(class_info['name'])
        self.class_description.setText(class_info['description'])

    def reset_character(self):
        """Сброс характеристик персонажа"""
        reply = QMessageBox.question(self, 'Сброс характеристик',
                                     'Вы уверены, что хотите сбросить все характеристики?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.strength_slider.setValue(0)
            self.agility_slider.setValue(0)
            self.intelligence_slider.setValue(0)

            self.name_input.clear()
            self.save_button.setEnabled(False)

            QMessageBox.information(self, 'Сброс выполнен',
                                    'Все характеристики сброшены. Начинайте заново!')

    def save_character(self):
        """Сохранение персонажа"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, 'Ошибка', 'Введите имя персонажа!')
            return

        strength = self.strength_slider.value()
        agility = self.agility_slider.value()
        intelligence = self.intelligence_slider.value()

        # Проверяем, что все очки распределены
        if (strength + agility + intelligence) < self.total_points:
            reply = QMessageBox.question(self, 'Не все очки распределены',
                                         f'У вас осталось {self.total_points - (strength + agility + intelligence)} нераспределенных очков.\n'
                                         'Сохранить персонажа в текущем состоянии?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

        # Создаем сообщение с информацией о персонаже
        character_info = f"""
        ╔══════════════════════════════════════╗
        ║         ПЕРСОНАЖ СОХРАНЕН!          ║
        ╚══════════════════════════════════════╝

        📛 Имя: {name}
        ⚔️  Класс: {self.class_name.text()}

        📊 ХАРАКТЕРИСТИКИ:
        💪 Сила: {strength}/100
        🏹 Ловкость: {agility}/100
        🧠 Интеллект: {intelligence}/100

        🎯 Очки: {strength + agility + intelligence}/{self.total_points}
        {self.class_description.text()}
        """

        QMessageBox.information(self, 'Персонаж сохранен', character_info)


def main():
    app = QApplication(sys.argv)

    # Установка стиля приложения
    app.setStyle('Fusion')

    # Установка цветовой палитры
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(44, 62, 80))
    app.setPalette(palette)

    creator = CharacterCreator()
    creator.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()