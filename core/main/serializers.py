from rest_framework import serializers

from core.main.models import Problem


class ProblemSerializer(serializers.ModelSerializer):
    # id_problem = serializers.SerializerMethodField()
    class Meta:
        model = Problem
        fields = [
            "id", "author", "title", "subtitle", "description", "difficulty"
        ]

    # def get_id_problem(self, obj):
    #     return obj.pk