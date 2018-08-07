import re

from django import forms

from transliterate import translit
from transliterate.exceptions import LanguageDetectionError

from task import models


def transliterate(text):
    pieces = str(re.sub('[\W]+', ' ', text)).lower().split(' ')
    result = []

    for piece in pieces:
        try:
            result.append(translit(piece, reversed=True))
        except LanguageDetectionError:
            result.append(piece)
    return '-'.join([r for r in result if r])


class PublicationForm(forms.ModelForm):
    def clean_slug(self):
        return transliterate(self.cleaned_data['name'])


class GroupForm(PublicationForm):
    class Meta:
        model = models.Group
        fields = '__all__'


class ElementForm(PublicationForm):
    class Meta:
        model = models.Element
        fields = '__all__'

