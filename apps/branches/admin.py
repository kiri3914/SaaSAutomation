from .models import Country, Branch, Direction
from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportModelAdmin


@register(Direction)
class DirectionAdmin(ModelAdmin):
    list_display = ('title', 'description')
    icon_name = 'directions'


@register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ('name',)
    icon_name = 'location_city'


@register(Branch)
class BranchAdmin(ImportExportModelAdmin):
    list_display = (
        'country',
        'city',
        'address',
        'opening_date',
        'instagram',
        'currency',
    )
    icon_name = 'location_on'
