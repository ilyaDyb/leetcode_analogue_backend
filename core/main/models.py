from django.db import models

from core.users.models import User

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="user_problems")
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=150)
    description = models.TextField()
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return f"{self.pk}. {self.title}"
    
class TestCase(models.Model):
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)
    input_data = models.CharField(max_length=100, help_text="Input data for test case")
    expected_output = models.CharField(max_length=100, help_text="Outnput data for test case")

    def __str__(self):
        return f"Test case for {self.problem}"
    
class Solution(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="solutions")
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE, related_name="solutions")
    code = models.TextField(help_text="Code of solution")
    status = models.CharField(max_length=50, default='pending', help_text="(pending, accepted, rejected)")
    passed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date of sending solution")

    class Meta:
        unique_together = ['problem', 'user']

    def __str__(self):
        return f"Solution for {self.problem.title} by {self.user.username}"
    
class SolutionResult(models.Model):
    solution = models.ForeignKey(Solution, related_name='results', on_delete=models.CASCADE)
    test_case = models.ForeignKey(TestCase, related_name='results', on_delete=models.CASCADE)
    lead_time = models.IntegerField(help_text="Execution time in milliseconds")
    memory_used = models.DecimalField(max_digits=10, decimal_places=2, help_text="Memory used in MB")
    actual_output = models.TextField()
    passed = models.BooleanField()
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.solution.problem.title} by {self.solution.user.username}"