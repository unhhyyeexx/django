from csv import list_dialects
from django.contrib import admin
from .models import Music, Artist

# Register your models here.
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)

class MusicAdmin(admin.ModelAdmin):
    list_display = ('artist', 'title',)


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Music, MusicAdmin)
