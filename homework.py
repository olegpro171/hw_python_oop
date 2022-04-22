class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        result_string = (f"Тип тренировки: {self.training_type}; " +
                         f"Длительность: {self.duration} ч.; " +
                         f"Дистанция: {self.distance} км; " +
                         f"Ср. скорость: {self.speed} км/ч; " +
                         f"Потрачено ккал: {self.calories}.")
        return result_string


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.M_IN_KM = 1000
        self.LEN_STEP: float = 0.65

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
        result = InfoMessage(None, self.duration, distance, speed, calories)
        return result



class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)
        self.LEN_STEP: float = 0.65

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        result = ((coeff_calorie_1 * mean_speed - coeff_calorie_2) *
                  self.weight / self.M_IN_KM * self.duration)
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
        coeffs = (0.035, 2, 0.029)
        mean_speed = self.get_mean_speed()
        result = ((coeffs[0] * self.weight +
                   (mean_speed ** coeffs[1] // self.height) * coeffs[2] *
                   self.duration))
        return result



class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP: float = 0.65

    def get_mean_speed(self) -> float:
        result = (self.length_pool * self.count_pool /
                  self.M_IN_KM / self.duration)
        return result

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        coeffs = (1.1, 2)
        result = (mean_speed + coeffs[0]) * coeffs[1] * self.weight
        return result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    pass


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
