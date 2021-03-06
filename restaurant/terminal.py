from . import order
from . import terminal_gui

import pickle
from sys import path
from typing import List
from os.path import dirname
from PyQt5 import QtWidgets


# Необходимо для корректной загрузки меню из файла.
path.append(dirname(__file__))


class Terminal(QtWidgets.QMainWindow):
    """Класс для обработки ввода пользователя и создания заказа"""
    def __init__(self):
        self.__worked = True
        # Загружаем из файла в терминал меню блюд.
        with open("restaurant/dishes.pickle", 'r+b') as file:
            try:
                self.__menu = pickle.load(file)
            except pickle.PickleError:
                print("Ошибка загрузки меню.")
                self.__worked = False
                return

        # Создаем заказ.
        self.__order = order.Order()

        # Инициализируем GUI-интерфейс.
        super(Terminal, self).__init__()
        self.__init_gui()

    @property
    def worked(self):
        """Геттер для проверки состояния терминала"""
        return self.__worked

    def __init_gui(self):
        """Метод инициализации интерфейса."""
        self.ui = terminal_gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Терминал")

        # Настройка таблиц.
        self.__set_settings_table(table=self.ui.table_menu,
                                  headers=["Название", "Цена"])
        self.__set_settings_table(table=self.ui.table_order,
                                  headers=["Название", "Цена", "Количество"])
        # Стоит обновить таблицу меню после изменения self.__menu.
        self.__update_menu_table()

        # Подключение слотов для обработки сигналов.
        self.ui.add_dish_btn.clicked.connect(self.__slot_add_dish)
        self.ui.del_dish_btn.clicked.connect(self.__slot_delete_dish)
        self.ui.ingredients_btn.clicked.connect(self.__slot_show_ingredients)
        self.ui.pay_order_btn.clicked.connect(self.__slot_pay_order)

    @staticmethod
    def __set_settings_table(table: QtWidgets.QTableWidget,
                             headers: List[str], rows: int = 0):
        """Метод для настройки таблиц."""
        # Количество столбцов и строк.
        table.setColumnCount(len(headers))
        table.setRowCount(rows)
        # Устанавливаем заголовки.
        table.setHorizontalHeaderLabels(headers)
        # При нажатии выделяем всю строку.
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # Разрешаем выделение только одного элемента.
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # Запрещаем редактирование ячеек.
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Растягиваем все элементы равномерно.
        for i in range(table.columnCount()):
            table.horizontalHeader().setSectionResizeMode(i, QtWidgets.
                                                          QHeaderView.Stretch)

    @staticmethod
    def __get_chosen_dish(table):
        """Получаем номер выбранного блюда."""
        select_model = table.selectionModel()
        if select_model.hasSelection():
            selected_row = list(set(index.row() for index in select_model.
                                    selectedIndexes()))[0]
            return selected_row

        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText("Выберите блюдо.")
        msg.exec()

    @staticmethod
    def __append_dish_to_table(table: QtWidgets.QTableWidget, *args):
        """Вставка блюда в таблицу."""
        rows = table.rowCount()
        table.setRowCount(rows+1)

        for index, value in enumerate(args):
            new_item = QtWidgets.QTableWidgetItem()
            new_item.setText(str(value))
            table.setItem(rows, index, new_item)

    def __update_menu_table(self):
        """Заполнение таблицы меню блюдами из меню."""
        table = self.ui.table_menu
        table.setRowCount(0)
        # Выводим меню.
        for index_row, dish in enumerate(self.__menu):
            self.__append_dish_to_table(table, dish.name, str(dish.price))

    def __update_order_table(self):
        """Метод для обновления таблицы заказов."""
        table = self.ui.table_order
        table.setRowCount(0)
        for index_row, dish_info in enumerate(self.__order.dishes.values()):
            self.__append_dish_to_table(table, dish_info[0].name,
                                        str(dish_info[0].price),
                                        str(dish_info[1]))
        # Обновляем цену.
        self.ui.total_price_label.setText("Итого: " + str(self.__order.
                                                          total_price) + 'p')

    def __slot_show_ingredients(self):
        """Метод для вывода ингредиентов блюда."""
        index_dish = self.__get_chosen_dish(self.ui.table_menu)
        if index_dish is not None:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle(self.__menu[index_dish].name + ": состав")
            msg.setText('\n'.join(self.__menu[index_dish].ingredients))
            msg.exec()

    def __slot_add_dish(self):
        """Добавляем блюда в заказ, которые пользователь выбрал из меню."""
        index_dish = self.__get_chosen_dish(self.ui.table_menu)
        if index_dish is not None:
            self.__order.add_dish(self.__menu[index_dish])
            self.__update_order_table()

    def __slot_delete_dish(self):
        """Когда пользователь хочет посмотреть или редактировать заказ."""
        index_dish = self.__get_chosen_dish(self.ui.table_order)
        if index_dish is not None:
            self.__order.remove_dish(index_dish)
            self.__update_order_table()

    def __slot_pay_order(self):
        """Подтверждение и последующая опалата заказа."""
        if self.__order.total_price == 0:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Ваш заказ пуст.")
            msg.exec()
            return

        amount, confirmed = QtWidgets.QInputDialog.getInt(self, "Оплата",
                                                          "К оплате " + str(self.__order.total_price),
                                                          QtWidgets.QLineEdit.Normal)
        if confirmed:
            msg = QtWidgets.QMessageBox()
            if amount >= self.__order.total_price:
                msg.setWindowTitle("Заказ оплачен")
                msg.setText(f"Ваша сдача: {amount - self.__order.total_price}"
                            "\nПриятного аппетита!")

                # Очищаем заказ и обновляем GUI.
                self.__order.clear_order()
                self.__update_order_table()
            else:
                msg.setWindowTitle("Отмена оплаты")
                msg.setText("Недостаточно средств.")
            msg.exec()
