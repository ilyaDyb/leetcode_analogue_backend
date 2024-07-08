from rest_framework import serializers

from core.main.models import Problem, TestCase


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            "id", "author", "title", "type", "subtitle", "description", "difficulty", "fst_line"
        ]

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = [
            "input_data", "expected_output"
        ]        

    # def create(self, validated_data: dict, id_problem: int):
    #     problem = Problem.objects.get(id=id_problem)
    #     test_case = TestCase.objects.create(problem=problem, **validated_data)
    #     return test_case
    