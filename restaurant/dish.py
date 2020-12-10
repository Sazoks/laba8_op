class Dish:
    """
    Класс блюда.
    Содержит имя блюда, его цену и ингредиенты, из которых состоит.
    """
    def __init__(self, name: str, price: int, ingredients: list):
        """Инициализатор класса"""
        self.__name = name
        self.__price = price
        self.__ingredients = ingredients

    @property
    def name(self):
        """Геттер для получения имени"""
        return self.__name

    @property
    def price(self):
        """Геттер для получения цены"""
        return self.__price

    @property
    def ingredients(self):
        """Геттер для получения ингердиентов"""
        return self.__ingredients

    def cooking(self):
        """Имитация готовки"""
        print(f"Готовится: {self.__name}")

    def print_info_dish(self):
        """Вывод информации о блюде"""
        print("\t Название:", self.__name)
        print("\t Цена:", self.__price)
        print("\t Ингредиенты:", *self.__ingredients)
