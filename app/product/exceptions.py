from app.core.exceptions import NotFound


class ProductNotFound(NotFound):
    """
    Продукт не найден
    """


class CharacteristicNotFound(NotFound):
    """
    Характеристика не найдена
    """

class ReviewNotFound(NotFound):
    """
    Отзыв не найден
    """