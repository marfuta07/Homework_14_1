class LoggingMixin:
    """
    Миксин для логирования создания объектов.
    Печатает информацию о классе и параметрах при инициализации.
    """

    def __init__(self, *args, **kwargs):

        # Получаем имя класса
        class_name = self.__class__.__name__

        # Формируем список аргументов
        args_repr = [repr(arg) for arg in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        all_args = args_repr + kwargs_repr
        # Создаём строку с параметрами
        params_str = ", ".join(all_args)
        # Печатаем информацию о создании
        print(f"{class_name}({params_str})")
        # Вызываем следующий конструктор в цепочке наследования
        super().__init__(*args, **kwargs)

    def __repr__(self):
        """
        Возвращает строковое представление объекта, которое можно использовать
        для воссоздания объекта.
        """
        args_repr = [repr(getattr(self, attr)) for attr in self.__dict__ if not attr.startswith('_')]
        return f"{self.__class__.__name__}({', '.join(args_repr)})"
