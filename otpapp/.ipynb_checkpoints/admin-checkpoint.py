from django.contrib import admin
from . import models


# class ClientAdmin(admin.ModelAdmin):
#     date_hierarchy = 'created'
#     list_display = ('client_name', 'created')
#     fields = ['client_name','updated']
# admin.site.register(models.Client,ClientAdmin)
admin.site.register(models.User)
admin.site.register(models.Jobs)
admin.site.register(models.SliderImage)

