import functools
import logging
from typing import Callable, Any, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования работы функции.

    :param filename: Имя файла для записи логов. Если не указано, логи выводятся в консоль.
    """
    # Настройка логирования
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if filename:
        handler = logging.FileHandler(filename)
    else:
        handler = logging.StreamHandler()  # Логируем в консоль

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                logger.info(f"Вызов функции '{func.__name__}' с аргументами: {args}, {kwargs}")
                result = func(*args, **kwargs)
                logger.info(f"Функция '{func.__name__}' завершена успешно, результат: {result}")
                return result
            except Exception as e:
                logger.error(f"Функция '{func.__name__}' вызвана с ошибкой: {str(e)}. Inputs: {args}, {kwargs}")
                raise  # Повторно выбрасываем исключение

        return wrapper

    return decorator
