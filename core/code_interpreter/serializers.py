from rest_framework import serializers

from core.main.models import SolutionResult

class SolutionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionResult
        fields = ["id", "problem", "user", "lead_time", "memory_used", "user_code", "passed", "executed_at"]

    def create(self, validated_data):
        instance, created = SolutionResult.objects.update_or_create(
            problem=validated_data.get('problem'),
            user=validated_data.get('user'),
            defaults={
                'executed_at': validated_data.get('executed_at'),
                'lead_time': validated_data.get('lead_time'),
                'memory_used': validated_data.get('memory_used'),
                'user_code': validated_data.get('user_code'),
                'passed': validated_data.get('passed')
            }
        )
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        problem = instance.problem
        representation["problem"] = {
            "id_problem": problem.id,
            "title": problem.title
        }
        return representation