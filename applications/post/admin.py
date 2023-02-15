from django.contrib import admin
from django.db.models import Avg
from ..post.models import *

class ImageAdmin(admin.TabularInline):
    model = PostImage
    fields = ('image',)
    max_num = 4

class PostAdmin(admin.ModelAdmin):
    inlines = (ImageAdmin,)
    list_display = ('title', 'owner', 'post_count', 'rating')

    def post_count(self, obj):
        return obj.likes.filter(is_like=True).count()

    def rating(self, obj):
        return f"count --> {obj.ratings.all().count()} ---------- Avg --> {obj.ratings.all().aggregate(Avg('rating'))['rating__avg']}"

admin.site.register(Post, PostAdmin)
admin.site.register(PostImage)
admin.site.register(Comment)
