from django.contrib.admin import register, ModelAdmin, TabularInline
from .models import Client, ClientStatus, TrailLesson


@register(Client)
class ClientAdmin(ModelAdmin):
    list_display = (
        'name',
        'phone',
        'whatsapp',
        'trail_lesson',
        'status',
        'comment',
        'create_at',
        'recruiter'
    )
    icon_name = 'person_add'


class ClientInlineAdmin(TabularInline):
    fk_name = 'trail_lesson'
    model = Client
    extra = 1


@register(TrailLesson)
class TrailLessonAdmin(ModelAdmin):
    list_display = ['title', 'date']
    search_fields = ['title', 'date']
    list_filter = ['date']
    inlines = [ClientInlineAdmin, ]

    icon_name = 'add_to_queue'


@register(ClientStatus)
class ClientStatusAdmin(ModelAdmin):
    list_display = ('title',)
    icon_name = 'check_circle'
