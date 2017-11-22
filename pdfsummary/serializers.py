from rest_framework import serializers


class summarizeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('text', 'summarized')



