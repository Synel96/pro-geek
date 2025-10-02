from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline
from .models import RegistrationCode, BlogPost, BlogSection, SectionImage, SectionVideo, News, Event

@admin.register(RegistrationCode)
class RegistrationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used', 'created_at', 'used_at')
    search_fields = ('code',)
    list_filter = ('is_used',)
    ordering = ('-created_at',)
    fields = ('code',)
    readonly_fields = ('is_used', 'created_at', 'used_at')
    help_texts = {
        'code': 'Új regisztrációs kód hozzáadása: csak a kódot kell megadni.'
    }
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['code'].help_text = self.help_texts['code']
        return form

class SectionImageInline(NestedStackedInline):
    model = SectionImage
    extra = 1
    fields = ('image',)
    help_texts = {
        'image': 'Kép feltöltése a szekcióhoz.'
    }
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field, text in self.help_texts.items():
            if field in formset.form.base_fields:
                formset.form.base_fields[field].help_text = text
        return formset

class SectionVideoInline(NestedStackedInline):
    model = SectionVideo
    extra = 1
    fields = ('video',)
    help_texts = {
        'video': 'Videó feltöltése a szekcióhoz.'
    }
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field, text in self.help_texts.items():
            if field in formset.form.base_fields:
                formset.form.base_fields[field].help_text = text
        return formset

class BlogSectionInline(NestedStackedInline):
    model = BlogSection
    extra = 1
    inlines = [SectionImageInline, SectionVideoInline]
    fields = ('title', 'content')
    help_texts = {
        'title': 'A szekció címe.',
        'content': 'A szekció szöveges tartalma.'
    }
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for field, text in self.help_texts.items():
            if field in formset.form.base_fields:
                formset.form.base_fields[field].help_text = text
        return formset

@admin.register(BlogPost)
class BlogPostAdmin(NestedModelAdmin):
    inlines = [BlogSectionInline]
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    ordering = ('-created_at',)
    fields = ('title', 'author', 'preview_image')
    help_texts = {
        'title': 'A blogbejegyzés címe.',
        'author': 'A szerző (felhasználó) kiválasztása.',
        'preview_image': 'Előnézeti kép a blogbejegyzéshez.'
    }
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field, text in self.help_texts.items():
            if field in form.base_fields:
                form.base_fields[field].help_text = text
        return form

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author')
    ordering = ('-created_at',)
    fields = ('title', 'author', 'content', 'preview_image')
    help_texts = {
        'title': 'A hír címe. Pl.: "Új esemény a klubban"',
        'author': 'A szerző neve. Pl.: "Kiss Péter"',
        'content': 'A hír szövege, max. 450 karakter. Pl.: "A klubban új esemény indul..."',
        'preview_image': 'Előnézeti kép a hírhez. Csak képfájl tölthető fel.'
    }
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field, text in self.help_texts.items():
            if field in form.base_fields:
                form.base_fields[field].help_text = text
        return form

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'host', 'event_type', 'date', 'reward', 'location')
    search_fields = ('event_title', 'host', 'event_type', 'location')
    ordering = ('-date',)
    fields = ('event_title', 'host', 'event_type', 'date', 'reward', 'location', 'campfire_link')
    help_texts = {
        'event_title': 'Az esemény címe. Pl.: "Community Day Classic", "Go Fest"',
        'host': 'A hostoló Ambassador neve. Pl.: "Kiss Gábor (Ambassador)"',
        'event_type': 'Az esemény típusa. Pl.: "Raid Day", "Spotlight Hour"',
        'date': 'Az esemény dátuma. Pl.: "2025-10-15"',
        'reward': 'Jutalom jár-e az eseményhez. Pipáld ki, ha igen.',
        'location': 'Az esemény helyszíne. Pl.: "Budapest, Fő utca 1."',
        'campfire_link': 'Link a Campfire eseményhez (opcionális). Pl.: "https://campfire.com/event/123"'
    }
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field, text in self.help_texts.items():
            if field in form.base_fields:
                form.base_fields[field].help_text = text
        return form
