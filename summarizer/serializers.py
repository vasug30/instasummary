from rest_framework import serializers
from .models import Summarize


class summarizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Summarize
        fields = ('url', 'summarized')



