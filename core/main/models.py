from django.db import models

from core.auth_.models import User

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]
    TYPE_CHOICES = [
        ("Algorithm", "Algorithm"),
        ("SQL", "SQL"),
    ]
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="user_problems")
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="Algorithm")
    subtitle = models.CharField(max_length=150)
    description = models.TextField()
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES)
    fst_line = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.pk}. {self.title}"
    
class TestCase(models.Model):
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE, related_name="testcases")
    input_data = models.CharField(max_length=100, help_text="Input data for test case")
    expected_output = models.CharField(max_length=100, help_text="Outnput data for test case")

    def __str__(self):
        return f"Test case for {self.problem}"


class SolutionResult(models.Model):
    problem = models.ForeignKey(to=Problem, related_name='results', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    lead_time = models.IntegerField(help_text="Execution time in milliseconds")
    memory_used = models.DecimalField(max_digits=5, decimal_places=2, help_text="Memory used in MB")
    user_code = models.CharField(max_length=2000)
    passed = models.BooleanField()
    executed_at = models.DateTimeField(auto_now_add=True)
