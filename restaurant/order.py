from . import dish


class Order:
    """
    Класс для составления заказа пользователя.
    Содержит список заказанных блюд, состояние заказа и общую цену.
    """
    def __init__(self):
        """Инициализатор класса"""
        # Как выглядит __dishes:
        # {"name_dish": [object_dish, count_dish]}
        # Ключем выступает название блюда, а значением - список
        # из двух элементов: сам объект со всей необходимой инфой
        # и количество заказанных блюд этого типа.
        self.__dishes = dict()
        self.__total_count = 0
        self.__total_price = 0
        self.__confirmed = False

    @property
    def total_price(self):
        """Геттер для получения общей цены"""
        return self.__total_price

    @property
    def dishes(self):
        """Геттер для получения списка заказанных блюд"""
        return self.__dishes

    def add_dish(self, m_dish: dish.Dish):
        """Добавление блюда в заказ"""
        # Добавляем в словарь по ключу новое блюдо.
        # Если блюдо было, увеличиваем его кол-во на 1.
        name_dish = m_dish.name
        if name_dish not in self.__dishes.keys():
            self.__dishes[name_dish] = [m_dish, 1]
        else:
            self.__dishes[name_dish][1] += 1
        self.__total_price += m_dish.price
        self.__total_count += 1

    def remove_dish(self, index_dish: int):
        """Удаление блюда из заказа"""
        # Можно было бы просить юзера ввести название блюда, но это не удобно.
        # Конвертируем индекс блюда в его ключ. Пользователь вводите индекс,
        # ориентируясь на список своих заказанных блюд.
        index_to_key = list(self.__dishes.keys())[index_dish]
        self.__total_price -= self.__dishes[index_to_key][0].price
        self.__total_count -= 1
        if self.__dishes[index_to_key][1] == 1:
            self.__dishes.pop(index_to_key)
        else:
            self.__dishes[index_to_key][1] -= 1

    def clear_order(self):
        """Обнуление заказа"""
        self.__dishes.clear()
        self.__total_count = 0
        self.__total_price = 0
