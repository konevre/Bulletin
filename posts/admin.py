from django.contrib import admin
from .models import Post, Response, Newsletter


class ResponseInline(admin.TabularInline):
    model = Response


class PostAdmin(admin.ModelAdmin):
    inlines = [ResponseInline, ]


admin.site.register(Post, PostAdmin)
admin.site.register(Response)
admin.site.register(Newsletter)
