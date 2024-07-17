from rest_framework import serializers

from django.db.models import Count, F, Window
from django.db.models.functions import RowNumber

from core.auth_.models import User
from core.main.models import SolutionResult

class UserProfileSerializer(serializers.ModelSerializer):
    solved_problems = serializers.SerializerMethodField()
    was_complited_problems = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "was_complited_problems", "solved_problems", "rank"]

    def get_solved_problems(self, obj):
        solved_problems = SolutionResult.objects.filter(user=obj).order_by("-executed_at")

        return UserProfileSolutionResultSerializer(solved_problems, many=True).data
    
    def get_was_complited_problems(self, obj):
        complited_problems = SolutionResult.objects.filter(user=obj).aggregate(count=Count("id"))
        return complited_problems["count"]
    
    def get_rank(self, obj):
        user_with_rank = User.objects.annotate(
            solved_problems=Count("results"),
            position=Window(
                expression=RowNumber(),
                order_by=F('solved_problems').desc()
            )
        ).get(pk=obj.id)
        return user_with_rank.position
    

class UserProfileSolutionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionResult
        fields = ["id", "executed_at", "lead_time", "memory_used", "passed"]

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        problem = obj.problem
        representation['problem'] = {
            "id": problem.id,
            "title": problem.title,
        }
        return representation
    

class TopUserSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField()
    solved_problems = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["position", "id", "username", "solved_problems"]