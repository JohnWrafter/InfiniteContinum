from django.db import models


class MemberInquiry(models.Model):
    class Focus(models.TextChoices):
        STRENGTH = "strength", "Build strength"
        ENDURANCE = "endurance", "Improve endurance"
        MOBILITY = "mobility", "Move with more ease"
        CONSISTENCY = "consistency", "Find my rhythm"

    name = models.CharField(max_length=100)
    email = models.EmailField()
    focus = models.CharField(max_length=20, choices=Focus.choices, default=Focus.STRENGTH)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} · {self.get_focus_display()}"