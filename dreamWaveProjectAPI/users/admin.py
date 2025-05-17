from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'password')  # Admin panelinde görünecek sütunlar
    search_fields = ('id', 'username')  # Arama özelliği
    list_filter = ('id', 'username')  # Filtreleme seçenekleri
