from rest_framework import serializers

from core.main.models import Problem, TestCase


class ProblemSerializer(serializers.ModelSerializer):
    count_solutions = serializers.SerializerMethodField()
    
    class Meta:
        model = Problem
        fields = [
            "id", "author", "title", "type", "subtitle", "description", "difficulty", "count_solutions", "fst_line"
        ]
    def get_count_solutions(self, obj):
        return obj.get_count_solutions_of_problem()
    
    def to_representation(self, instance: Problem):
        representation = super().to_representation(instance)
        rates = instance.get_rates()
        representation["rates"] = {
            "likes": rates["likes"],
            "dislikes": rates["dislikes"],
        }
        return representation

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = [
            "problem", "input_data", "expected_output"
        ]   

    # def create(self, validated_data: dict, id_problem: int):
    #     problem = Problem.objects.get(id=id_problem)
    #     test_case = TestCase.objects.create(problem=problem, **validated_data)
    #     return test_case
    