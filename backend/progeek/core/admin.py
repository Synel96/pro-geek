from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline
from .models import RegistrationCode, BlogPost, BlogSection, SectionImage, SectionVideo

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
