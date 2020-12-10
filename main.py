from sys import exit
from PyQt5 import QtWidgets
from restaurant import terminal


def main():
    app = QtWidgets.QApplication([])
    terminal_1 = terminal.Terminal()
    terminal_1.show()
    exit(app.exec())

    # terminal_1 = terminal.Terminal()
    # # Пока терминал работает и пользователь хочет делать заказы.
    # while terminal_1.worked \
    #         and input("Хотите сделать заказ? [да/нет]").lower() == "да":
    #     # Создаем новый заказ.
    #     terminal_1.create_order()
    #
    #     # Пока заказ не будет обработан или пользователь его не отменит.
    #     while not terminal_1.order.confirmed:
    #         terminal_1.print_terminal_menu()
    #
    #         # Обрабатываем команду пользователя.
    #         action = input("Выберите действие: ")
    #         while not action.isdigit() or int(action) not in range(1, 5):
    #             action = input("Пожалуйста, выберите действие из списка: ")
    #
    #         add_dishes, my_order, to_pay, close_terminal = '1', '2', '3', '4'
    #         if action == add_dishes:
    #             terminal_1.add_dishes()
    #         elif action == my_order:
    #             terminal_1.edit_my_order()
    #         elif action == to_pay:
    #             terminal_1.pay_order()
    #         elif action == close_terminal:
    #             terminal_1.worked = False
    #             terminal_1.order.confirmed = True
    #
    #     # Здесь мы можем вернуть из терминала заказ, к примеру, для дальнейшей
    #     # работы с ним. Можно передать заказ на "кухню".
    #     # Из терминала заказ удаляем, т.к. он обработан и больше не нужен.
    #     terminal_1.delete_order()

    # print("Всего доброго!")


if __name__ == "__main__":
    main()
