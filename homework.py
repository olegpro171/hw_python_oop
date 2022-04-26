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

    MESSAGE_STRING: str = ("Тип тренировки: {training_type}; "
                           "Длительность: {duration:.3f} ч.; "
                           "Дистанция: {distance:.3f} км; "
                           "Ср. скорость: {speed:.3f} км/ч; "
                           "Потрачено ккал: {calories:.3f}.")

    def get_message(self) -> str:
        """
        Функция для получения строкового
        представления объекта InfoMessage.
        """
        return self.MESSAGE_STRING.format(**asdict(self))


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
        raise NotImplementedError('Метод ''get_spent_calories'''
                                  'реализован только у наследников')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CAL_RUN_SPEED_COEF: float = 18
    CAL_RUN_SPEED_PARAM: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Вернуть результат расчета затраченных калорий."""
        return ((self.CAL_RUN_SPEED_COEF * self.get_mean_speed()
                 - self.CAL_RUN_SPEED_PARAM)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CAL_WALKING_WEIGHT_COEF: float = 0.035
    CAL_WLK_SPEED_POW: float = 2
    CAL_WLK_SPEEDHEIGHT_COEF: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Вернуть результат расчета затраченных калорий."""
        return ((self.CAL_WALKING_WEIGHT_COEF * self.weight
                 + (self.get_mean_speed() ** self.CAL_WLK_SPEED_POW
                    // self.height) * self.CAL_WLK_SPEEDHEIGHT_COEF
                 * self.weight) * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CAL_SWM_SPEED_PARAM: float = 1.1
    CAL_SWM_WEIGHT_COEF: float = 2

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
        return ((self.get_mean_speed() + self.CAL_SWM_SPEED_PARAM)
                * self.CAL_SWM_WEIGHT_COEF * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    _TRAINING_DICT: Dict[str, Type['Training']] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    """Прочитать данные полученные от датчиков."""
    if workout_type not in _TRAINING_DICT:
        raise KeyError('Передан неверный код тренировки.')
    return _TRAINING_DICT[workout_type](*data)


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
