from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True)
    membership_start_date = models.DateTimeField(default=timezone.now)
    membership_expiry_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Calculate membership expiry date based on start date and plan duration
        if self.membership_plan and hasattr(self.membership_plan, 'duration_months'):
            self.membership_expiry_date = self.membership_start_date + timedelta(days=30 * self.membership_plan.duration_months)
        super().save(*args, **kwargs)

    def is_subscription_active(self):
        """
        Check if the user's subscription is active.
        """
        return self.membership_expiry_date >= timezone.now()
    
    def is_subscription_expired(self):
        # Check if the subscription has been expired for more than 3 days
        return self.membership_expiry_date < timezone.now() - timedelta(days=3)

    def __str__(self):
        return f"Profile of {self.user.username}"
    

