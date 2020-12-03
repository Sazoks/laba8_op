from . import order
from sys import path
from os.path import dirname
import pickle


# Необходимо для корректной загрузки меню из файла.
path.append(dirname(__file__))


class Terminal:
    """Класс для обработки ввода пользователя и создания заказа"""
    def __init__(self):
        """Конструктор класса"""
        self.__order = None
        self.__worked = True
        # Загружаем из файла в терминал меню блюд.
        with open("restaurant/dishes.pickle", 'r+b') as file:
            try:
                self.__menu = pickle.load(file)
            except pickle.PickleError:
                print("Ошибка загрузки меню.")
                self.__worked = False

    # public
    @property
    def worked(self):
        """Геттер для проверки состояния терминала"""
        return self.__worked

    @worked.setter
    def worked(self, new_status: bool):
        """Сеттер для установки состояния терминала"""
        self.__worked = new_status

    @property
    def order(self):
        """Получить текущий заказ"""
        return self.__order

    def create_order(self):
        """Создать новый заказ"""
        self.__order = order.Order()

    def delete_order(self):
        """Удалить текущий заказ"""
        self.__order = None

    def add_dishes(self):
        """Добавляем блюда в заказ, которые пользователь выбрал из меню"""
        self.__print_dishes_menu()
        print("Для добавления блюда введите его номер.\n"
              "Для возвращений в меню терминала введите 0.\n")

        adding_dish = input("Какое блюдо хотите добавить: ")
        while adding_dish != '0':
            if not adding_dish.isdigit() or \
                    int(adding_dish) - 1 not in range(len(self.__menu)):
                print("Пожалуйста, выберите блюдо из меню.")
            else:
                # add_dish принимает сам объект блюда, т.к. дальше
                # необходима вся информация о нем (о блюде).
                self.__menu[int(adding_dish) - 1].cooking()
                self.__order.add_dish(self.__menu[int(adding_dish) - 1])
            adding_dish = input("Какое блюдо хотите добавить: ")

    def edit_my_order(self):
        """Когда пользователь хочет посмотреть или редактировать заказ"""
        self.__order.show_order()
        print("Для удаления блюда введие его номер.\n"
              "Для возврата в меню терминала введите 0.\n"
              "Для отмены всего заказа введите Отмена.")

        deleted_dish = input("Удалить блюдо: ")
        while deleted_dish != '0' and deleted_dish.lower() != 'отмена':
            if not deleted_dish.isdigit() or \
                    int(deleted_dish) - 1 not in range(len(self.__order.dishes)):
                print("Пожалуйста, выберите блюдо из вашего списка.")
            else:
                # remove_dish принимает индекс из меню уже заказанных блюд.
                self.__order.remove_dish(int(deleted_dish) - 1)

            deleted_dish = input("Удалить блюдо: ")
            if deleted_dish.lower() == 'отмена':
                self.__order.clear_order()

    def pay_order(self):
        """Подтверждение и последующая опалата заказа"""
        # Пока пользователь не подтвердит заказ, возвращаем его обратно в меню,
        # пока он не одумается.
        confirmed = input(f"К оплате {self.__order.total_price}\n"
                          f"Подтвердить заказ? [да/нет]: ")
        if confirmed.lower() != "да":
            return

        # Запрашиваем деньги.
        amount = input("Внесите деньги за счет: ")
        while not amount.replace('.', '').isdigit() or \
                float(amount) < self.__order.total_price:
            amount = input("Внесите достаточную сумму: ")
        amount = float(amount)

        # Меняем статус заказа на обработанный и выводим инфу.
        self.__order.confirmed = True
        print("Заказа оплачен.\n"
              f"К оплате: {self.__order.total_price}\n"
              f"Внесенная сумма: {amount}\n"
              f"Сдача клиента: {round(amount - self.__order.total_price)}")

    # private
    def __print_dishes_menu(self):
        print("\n-------------- М Е Н Ю --------------")
        for number, dish in enumerate(self.__menu):
            print(f"{number + 1})", end='')
            dish.print_info_dish()
        print("---------------------------------------")

    # static
    @staticmethod
    def print_terminal_menu():
        print("\n---------- Т Е Р М И Н А Л ----------")
        print("1) Меню\n"
              "2) Мой заказ\n"
              "3) Оплатить\n"
              "4) Выход")
        print("-------------------------------------")
