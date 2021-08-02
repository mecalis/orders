from django import forms

from .models import BlogPost
from datetime import datetime

class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)



class BlogPostModelForm(forms.ModelForm):
    # publish_part_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), )
    # publish_part_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), )
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'slug', 'content']

        # widgets = {
        #         'publish_date': forms.DateTimeInput(attrs={'type': 'date'}, format='%Y-%m-%d %H:%M')
        #     }
        labels = {
            'title': 'cím',
            'image': 'kép',
            'slug': 'slug',
            'content': 'leírás',
            # 'publish_part_date': 'megjelenés napja',
            # 'publish_part_time': 'megjelenés ideje',
        }
        help_texts = {
            'slug': 'A böngészőben megjelenő url, általában a cím kötőjelekkel elválasztva. Szóközt nem tartalmazhat! pl.: Cím: ma használt cím => Slug: ma-hasznalt-cim',
        }

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = BlogPost.objects.filter(title__iexact=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk) # id=instance.id
        if qs.exists():
            raise forms.ValidationError("Ez a cím már használva volt, kérlek válassz másikat.")
        return title

#
# class BlogPostModelForm(forms.ModelForm):
#     publish_part_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}), )
#     publish_part_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}), )
#
#     class Meta:
#         model = BlogPost
#         fields = ['title', 'image', 'slug', 'content', 'publish_date']
#
#         widgets = {
#                 'publish_date': forms.DateTimeInput(attrs={'type': 'datetime'}, format='%Y-%m-%d %H:%M')
#             }
#         labels = {
#             'title': 'cím',
#             'image': 'kép',
#             'slug': 'slug',
#             'content': 'leírás',
#             'publish_date': 'megjelenés ideje',
#         }
#         help_texts = {
#             'slug': 'A böngészőben megjelenő url, általában a cím kötőjelekkel elválasztva. pl.: ma-hasznalt-cim',
#         }
#
#     def clean_title(self, *args, **kwargs):
#         instance = self.instance
#         title = self.cleaned_data.get('title')
#         qs = BlogPost.objects.filter(title__iexact=title)
#         if instance is not None:
#             qs = qs.exclude(pk=instance.pk) # id=instance.id
#         if qs.exists():
#             raise forms.ValidationError("Ez a cím már használva volt, kérlek válassz másikat.")
#         return title