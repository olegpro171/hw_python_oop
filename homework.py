class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """
        Функция для получения строкового
        представления объекта InfoMessage.
        """
        duration_rounded = "%.3f" % self.duration
        distance_rounded = "%.3f" % self.distance
        speed_rounded = "%.3f" % self.speed
        calories_rounded = "%.3f" % self.calories
        result_string = (f"Тип тренировки: {self.training_type}; "
                         f"Длительность: {duration_rounded} ч.; "
                         f"Дистанция: {distance_rounded} км; "
                         f"Ср. скорость: {speed_rounded} км/ч; "
                         f"Потрачено ккал: {calories_rounded}.")
        return result_string


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result = self.action * self.LEN_STEP / self.M_IN_KM
        return result

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        time = self.duration
        return distance / time

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        training_type = type(self).__name__
        result = InfoMessage(training_type,
                             self.duration,
                             distance,
                             speed,
                             calories)
        return result


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Вернуть результат расчета затраченных калорий."""
        mean_speed = self.get_mean_speed()
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        result = ((coeff_calorie_1 * mean_speed - coeff_calorie_2)
                  * self.weight / self.M_IN_KM * (self.duration * 60))
        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Вернуть результат расчета затраченных калорий."""
        coeffs = (0.035, 2, 0.029)
        mean_speed = self.get_mean_speed()
        result = ((coeffs[0] * self.weight
                  + (mean_speed ** coeffs[1] // self.height) * coeffs[2]
                  * self.weight) * (self.duration * 60))
        return result


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Вернуть результат расчета средней скорости."""
        result = (self.length_pool * self.count_pool
                  / self.M_IN_KM / self.duration)
        return result

    def get_spent_calories(self) -> float:
        """Вернуть результат расчета затраченных калорий."""
        mean_speed = self.get_mean_speed()
        coeffs = (1.1, 2)
        result = (mean_speed + coeffs[0]) * coeffs[1] * self.weight
        return result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    result_object = training_dict[workout_type](*data)
    return result_object


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
