import dish
import pickle


def main():
    is_run = 'y'
    dishes = list()
    while is_run == 'y':
        name_dish = input("Enter the name dish:")
        price = int(input("Enter the price dish:"))
        ingredients = []

        add_more = 'y'
        while add_more == 'y':
            name_ingredient = input("Enter the name ingredient:")
            ingredients.append(name_ingredient)
            add_more = input("Continue to add ingredients? [y/N]")

        temp_dish = dish.Dish(name_dish, price, ingredients)
        dishes.append(temp_dish)
        is_run = input("Continue to create dishes? [y/N]")

    with open("dishes.pickle", 'w+b') as file:
        pickle.dump(dishes, file)


if __name__ == "__main__":
    main()
