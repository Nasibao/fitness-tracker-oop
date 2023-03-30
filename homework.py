class InfoMessage:
    """Информационное сообщение о тренировке."""

    MESSAGE: str = (
        "Тип тренировки: {training_type}; "
        "Длительность: {duration:.3f} ч.; "
        "Дистанция: {distance:.3f} км; "
        "Ср. скорость: {speed:.3f} км/ч; "
        "Потрачено ккал: {calories:.3f}."
    )

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.duration = duration

    def get_message(self) -> str:
        return self.MESSAGE.format(
            training_type=self.training_type,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories,
            duration=self.duration,
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    TRAINING_TYPE: str = ""
    MINUTES_IN_HOUR: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return info_message


class Running(Training):
    """Тренировка: бег."""

    CF_RUN_1: int = 18
    CF_RUN_2: int = 20

    def get_spent_calories(self) -> float:
        cal = self.CF_RUN_1 * self.get_mean_speed() - self.CF_RUN_2
        t = self.duration * self.MINUTES_IN_HOUR
        calories = (cal * self.weight / self.M_IN_KM) * t

        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CF_WALK_1: float = 0.035
    CF_WALK_2: float = 2
    CF_WALK_3: float = 0.029

    def __init__(
        self, action: int, duration: float, weight: float, height: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories_1 = self.CF_WALK_1 * self.weight
        calories_2 = self.get_mean_speed() ** 2 // self.height
        calories_3 = calories_2 * self.CF_WALK_3 * self.weight
        calories = (calories_1 + calories_3) * self.duration * 60
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    CF_SW_1 = 1.1
    CF_SW_2 = 2
    LEN_STEP = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed_1 = self.length_pool * self.count_pool
        self.speed = speed_1 / super().M_IN_KM / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        calories_1 = self.get_mean_speed() + self.CF_SW_1
        calories = calories_1 * self.CF_SW_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict: dict[str, Training] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }

    return type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
