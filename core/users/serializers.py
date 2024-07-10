from rest_framework import serializers

from django.db.models import Count

from core.auth_.models import User
from core.main.models import SolutionResult

class UserProfileSerializer(serializers.ModelSerializer):
    solved_problems = serializers.SerializerMethodField()
    was_complited_problems = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "username", "email", "was_complited_problems", "solved_problems"]

    def get_solved_problems(self, obj):
        solved_problems = SolutionResult.objects.filter(user=obj)

        return UserProfileSolutionResultSerializer(solved_problems, many=True).data
    
    def get_was_complited_problems(self, obj):
        complited_problems = SolutionResult.objects.filter(user=obj).aggregate(count=Count("id"))
        return complited_problems["count"]
    

class UserProfileSolutionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionResult
        fields = ["id", "lead_time", "memory_used", "passed"]

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        problem = obj.problem
        representation['problem'] = {
            "id": problem.id,
            "title": problem.title
        }
        return representation