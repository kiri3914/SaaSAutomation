from django.db import models


class Direction(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return self.title


class Country(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Branch(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='branch_country')
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    opening_date = models.DateField()
    instagram = models.URLField(max_length=255, blank=True, null=True)
    whatsapp = models.CharField(max_length=255, blank=True, null=True)
    list_direction = models.ManyToManyField(Direction, related_name='directions_branch')
    currency = models.CharField(max_length=10, default='KZT')
    chat_id = models.CharField(max_length=25, null=True)
    is_active = models.BooleanField(default=True)

    # Банковские данные для квитанции
    organization = models.CharField(max_length=255, null=True, blank=True, verbose_name='Наименование организации')
    bik = models.CharField(max_length=12, null=True, blank=True, verbose_name='БИК')
    bin = models.CharField(max_length=12, null=True, blank=True, verbose_name='БИН')
    account = models.CharField(max_length=20, null=True, blank=True, verbose_name='Счет')
    director_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Директор')
    stamp = models.ImageField(upload_to='stamps/', null=True, blank=True, verbose_name='Печать')
    
    @property
    def name(self):
        return f"{self.country.name} - {self.city} - {self.address}"

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return f"{self.country.name} - {self.city} - {self.address}"
