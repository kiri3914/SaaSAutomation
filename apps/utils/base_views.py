from rest_framework.viewsets import ModelViewSet


class BaseQuerysetView(ModelViewSet):
    """
    Класс BaseQuerysetView является представлением Django, который расширяет функциональность ModelViewSet
    для фильтрации данных по филиалам.

    Свойство queryset_filter используется для определения ключа и значения для фильтрации данных.
    Этот метод должен быть переопределен в подклассе BaseQuerysetView, чтобы определить, какой ключ будет
    использоваться для фильтрации данных. Значение ключа будет равно self.request.user.branch.

    Метод get_queryset фильтрует данные в зависимости от аутентификации пользователя и наличия прав доступа.
    Если пользователь аутентифицирован и не является суперпользователем, метод get_queryset фильтрует данные
    по значению queryset_filter, которое было определено в queryset_filter.
    Если пользователь не аутентифицирован, метод get_queryset возвращает пустой лист.

    Этот класс может быть полезен, если вам нужно отфильтровать данные в зависимости от филиала, в котором работает пользователь.
    """

    # переопределите related_name_filter в подклассе
    related_name_filter = 'branch'

    def get_filter_kwargs(self):
        # формируем kwargs для запроса
        return {self.related_name_filter: self.request.user.branch}

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return super().get_queryset()
            if not self.request.user.branch:
                return self.queryset.model.objects.none()
            return self.queryset.model.objects.filter(**self.get_filter_kwargs())
        return self.queryset.model.objects.none()
