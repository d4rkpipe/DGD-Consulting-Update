from modeltranslation.translator import register, TranslationOptions
from .models import Category, BlogPost


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(BlogPost)
class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'excerpt', 'content')
