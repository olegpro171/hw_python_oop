from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """
        Функция для получения строкового
        представления объекта InfoMessage.
        """
        result_string = ("Тип тренировки: {}; "
                         "Длительность: {:.3f} ч.; "
                         "Дистанция: {:.3f} км; "
                         "Ср. скорость: {:.3f} км/ч; "
                         "Потрачено ккал: {:.3f}.".format
                         (*asdict(self).values()))
        return result_string


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CAL_COEFF_RUNNING_1: float = 18
    CAL_COEFF_RUNNING_2: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Вернуть результат расчета затраченных калорий."""
        return ((self.CAL_COEFF_RUNNING_1 * self.get_mean_speed()
                 - self.CAL_COEFF_RUNNING_2)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CAL_COEFF_WALKING_1: float = 0.035
    CAL_COEFF_WALKING_2: float = 2
    CAL_COEFF_WALKING_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Вернуть результат расчета затраченных калорий."""
        return ((self.CAL_COEFF_WALKING_1 * self.weight
                 + (self.get_mean_speed() ** self.CAL_COEFF_WALKING_2
                    // self.height) * self.CAL_COEFF_WALKING_3 * self.weight)
                * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CAL_COEFF_SWIMMING_1: float = 1.1
    CAL_COEFF_SWIMMING_2: float = 2

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
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Вернуть результат расчета затраченных калорий."""
        return ((self.get_mean_speed() + self.CAL_COEFF_SWIMMING_1)
                * self.CAL_COEFF_SWIMMING_2 * self.weight)


TRAINING_DICT: Dict[str, Type[Swimming | Running | SportsWalking]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in TRAINING_DICT.keys():
        raise ValueError('Передан неверный код тренировки.')
    result_object = TRAINING_DICT[workout_type](*data)
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
