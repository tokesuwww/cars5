import json
from tabulate import tabulate
import os

class Car:
    def __init__(self, brand, model, color, gearbox, engine, status, headlights, doors, windows):
        self.brand = brand
        self.model = model
        self.color = color
        self.gearbox = gearbox
        self.engine = engine
        self.status = status
        self.headlights = headlights
        self.doors = doors
        self.windows=windows

    def to_dict(self):
        return {
            "brand": self.brand,
            "model": self.model,
            "color": self.color,
            "gearbox": self.gearbox,
            "engine": self.engine,
            "status": self.status,
            "headlights": self.headlights,
            "doors": self.doors,
            "windows":self.windows
        }

class CarDatabase:
    def __init__(self, filename="cars.txt"):
        self.filename = filename
        self.load_cars()
        self.all_cars = self.cars.copy()

        # Data for dropdowns
        self.brands = ["Toyota", "Honda", "Ford", "BMW", "Mercedes-Benz"]
        self.models = {}
        self.models["Toyota"] = ["Corolla", "Camry", "RAV4", "Prius", "Yaris"]
        self.models["Honda"] = ["Civic", "Accord", "CR-V", "Pilot", "Fit"]
        self.models["Ford"] = ["Focus", "Mustang", "Explorer", "F-150", "Fusion"]
        self.models["BMW"] = ["3 Series", "5 Series", "X3", "X5", "M3"]
        self.models["Mercedes-Benz"] = ["C-Class", "E-Class", "S-Class", "GLC", "GLE"]
        self.colors = ["Красный", "Синий", "Зеленый", "Черный", "Белый"]
        self.gearboxes = ["Механика", "Автомат", "Робот"]
        self.engines = ["Бензиновый", "Дизельный", "Гибридный", "Электро"]
        self.statuses = ["Заведена", "Не заведена"]
        self.headlights = ["Включены", "Не включены"]
        self.doors = ["Закрыты", "Открыты"]
        self.windows = ["Закрыты", "Открыты"]

    def load_cars(self):
        try:
            with open(self.filename, "r") as f:
                self.cars = [Car(**car_data) for car_data in json.load(f)]
        except FileNotFoundError:
            self.cars = []

    def save_cars(self):
        with open(self.filename, "w") as f:
            json.dump([car.to_dict() for car in self.cars], f)

    def add_car(self, car):
        self.cars.append(car)
        self.all_cars.append(car)
        self.save_cars()

    def update_car(self, index, car):
        self.cars[index] = car
        self.all_cars[index] = car
        self.save_cars()

    def delete_car(self, index):
        del self.cars[index]
        del self.all_cars[index]
        self.save_cars()

    def find_cars(self, brand=None, model=None, color=None, gearbox=None, engine=None, status=None, headlights=None, doors=None,windows=None):
        results = []
        for car in self.cars:
            match = True
            if brand is not None and car.brand != brand:
                match = False
            if model is not None and car.model != model:
                match = False
            if color is not None and car.color != color:
                match = False
            if gearbox is not None and car.gearbox != gearbox:
                match = False
            if engine is not None and car.engine != engine:
                match = False
            if status is not None and car.status != status:
                match = False
            if headlights is not None and car.headlights != headlights:
                match = False
            if doors is not None and car.doors != doors:
                match = False
            if windows is not None and car.windows != windows:
                match = False
            if match:
                results.append(car)
        return results

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_cars(cars):
    headers = ["Марка", "Модель", "Цвет", "КПП", "Двигатель", "Статус", "Фары", "Двери","Окна"]
    table_data = [[
        car.brand, car.model, car.color, car.gearbox, car.engine, car.status, car.headlights, car.doors, car.windows
    ] for car in cars]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def get_input(options, prompt):
    print(prompt)
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    while True:
        try:
            choice = int(input("Выберите вариант: "))
            if choice == 0:
                return None
            elif 1 <= choice <= len(options):
                return options[choice-1]
            else:
                print("Неверный выбор. Попробуйте снова.")
        except ValueError:
            print("Неверный ввод. Попробуйте снова.")

def add_car(db):
    clear_console()
    brand = get_input(db.brands, "Выберите марку:")
    if brand is None:
        return

    model = get_input(db.models[brand], "Выберите модель:")
    if model is None:
        return

    color = get_input(db.colors, "Выберите цвет:")
    if color is None:
        return

    gearbox = get_input(db.gearboxes, "Выберите тип КПП:")
    if gearbox is None:
        return

    engine = get_input(db.engines, "Выберите тип двигателя:")
    if engine is None:
        return

    status = get_input(db.statuses, "Выберите статус:")
    if status is None:
        return

    headlights = get_input(db.headlights, "Выберите состояние фар:")
    if headlights is None:
        return

    doors = get_input(db.doors, "Выберите состояние дверей:")
    if doors is None:
        return

    windows = get_input(db.windows, "Выберите состояние окон:")
    if windows is None:
        return

    new_car = Car(brand, model, color, gearbox, engine, status, headlights, doors,windows)
    db.add_car(new_car)
    print("Машина добавлена!")

def edit_car(db):
    clear_console()
    display_cars(db.cars)
    if len(db.cars) == 0:
        print("Нет машин в базе данных.")
        return

    while True:
        try:
            index = int(input("Введите индекс машины для редактирования (от 1 до {}): ".format(len(db.cars)))) - 1
            if 0 <= index < len(db.cars):
                break
            else:
                print("Неверный индекс. Попробуйте снова.")
        except ValueError:
            print("Неверный ввод. Попробуйте снова.")

    car = db.cars[index]

    print("Какую характеристику хотите изменить?")
    print("1. Марка")
    print("2. Модель")
    print("3. Цвет")
    print("4. КПП")
    print("5. Двигатель")
    print("6. Статус")
    print("7. Фары")
    print("8. Двери")
    print("9. Окна")
    print("0. Выход в меню")

    while True:
        try:
            choice = int(input("Выберите вариант: "))
            if choice == 0:
                return
            elif 1 <= choice <= 9:
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
        except ValueError:
            print("Неверный ввод. Попробуйте снова.")

    if choice == 1:
        car.brand = get_input(db.brands, "Выберите марку:")
        if car.brand is None:
            return
    elif choice == 2:
        car.model = get_input(db.models[car.brand], "Выберите модель:")
        if car.model is None:
            return
    elif choice == 3:
        car.color = get_input(db.colors, "Выберите цвет:")
        if car.color is None:
            return
    elif choice == 4:
        car.gearbox = get_input(db.gearboxes, "Выберите тип КПП:")
        if car.gearbox is None:
            return
    elif choice == 5:
        car.engine = get_input(db.engines, "Выберите тип двигателя:")
        if car.engine is None:
            return
    elif choice == 6:
        car.status = get_input(db.statuses, "Выберите статус:")
        if car.status is None:
            return
    elif choice == 7:
        car.headlights = get_input(db.headlights, "Выберите состояние фар:")
        if car.headlights is None:
            return
    elif choice == 8:
        car.doors = get_input(db.doors, "Выберите состояние дверей:")
        if car.doors is None:
            return
    elif choice == 9:
        car.windows = get_input(db.windows, "Выберите состояние окон:")
        if car.doors is None:
            return

    db.update_car(index, car)
    print("Информация о машине обновлена!")

def search_cars(db):
    clear_console()
    search_criteria = {}
    while True:
        print("По каким параметрам хотите искать? (Введите 'Готово', чтобы завершить выбор)")
        print("1. Марка")
        print("2. Модель")
        print("3. Цвет")
        print("4. КПП")
        print("5. Двигатель")
        print("6. Статус")
        print("7. Фары")
        print("8. Двери")
        print("9. Окна")
        print("0. Выход в меню")

        while True:
            try:
                choice = int(input("Выберите вариант: "))
                if choice == 0:
                    return
                elif 1 <= choice <= 9:
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
            except ValueError:
                print("Неверный ввод. Попробуйте снова.")

        if choice == 1:
            search_criteria["brand"] = get_input(db.brands, "Выберите марку:")
            if search_criteria["brand"] is None:
                return
        elif choice == 2:
            search_criteria["model"] = get_input(db.models.get(search_criteria.get("brand", None), []), "Выберите модель:")
            if search_criteria["model"] is None:
                return
        elif choice == 3:
            search_criteria["color"] = get_input(db.colors, "Выберите цвет:")
            if search_criteria["color"] is None:
                return
        elif choice == 4:
            search_criteria["gearbox"] = get_input(db.gearboxes, "Выберите тип КПП:")
            if search_criteria["gearbox"] is None:
                return
        elif choice == 5:
            search_criteria["engine"] = get_input(db.engines, "Выберите тип двигателя:")
            if search_criteria["engine"] is None:
                return
        elif choice == 6:
            search_criteria["status"] = get_input(db.statuses, "Выберите статус:")
            if search_criteria["status"] is None:
                return
        elif choice == 7:
            search_criteria["headlights"] = get_input(db.headlights, "Выберите состояние фар:")
            if search_criteria["headlights"] is None:
                return
        elif choice == 8:
            search_criteria["doors"] = get_input(db.doors, "Выберите состояние дверей:")
            if search_criteria["doors"] is None:
                return
        elif choice == 9:
            search_criteria["windows"] = get_input(db.windows, "Выберите состояние окон:")
            if search_criteria["windows"] is None:
                return
        elif choice == 0:
            return

        if input("Хотите добавить ещё параметры поиска? (да/нет): ").lower() != "да":
            break

    found_cars = db.find_cars(**search_criteria)  
    db.cars = found_cars
    display_cars(found_cars)

def delete_car(db):
    clear_console()
    display_cars(db.cars)
    if len(db.cars) == 0:
        print("Нет машин в базе данных.")
        return

    while True:
        try:
            index = int(input("Введите индекс машины для удаления (от 1 до {}): ".format(len(db.cars)))) - 1
            if 0 <= index < len(db.cars):
                break
            else:
                print("Неверный индекс. Попробуйте снова.")
        except ValueError:
            print("Неверный ввод. Попробуйте снова.")

    db.delete_car(index)
    print("Машина удалена!")


if __name__ == "__main__":
    db = CarDatabase()
    while True:
        clear_console()
        db.load_cars()
        display_cars(db.cars)
        print("1. Добавить машину")
        print("2. Изменить машину")
        print("3. Поиск машин")
        print("4. Удалить машину")
        print("6. Выход")

        while True:
            try:
                choice = int(input("Выберите действие: "))
                if choice == 0:
                    break
                elif 1 <= choice <= 6:
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
            except ValueError:
                print("Неверный ввод. Попробуйте снова.")

        if choice == 1:
            add_car(db)
        elif choice == 2:
            edit_car(db)
        elif choice == 3:
            search_cars(db)
        elif choice == 4:
            delete_car(db)
        elif choice == 6:
            break