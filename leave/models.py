from django.db import models

# Create your models here.

class Leaves(models.Model):
    
    LEAVE_STATUS_CHOICES= [(0, 'Pending for approval'),
                           (1, 'Approved and update in progress '),
                           (2, 'Approved and updated'),
                           (3, 'Rejected'),
                           (4, 'Approved'),
                           (5, 'Delete approval pending'),
                           (6, 'Deleted and update in progress'),
                           (7, 'Deleted')
                           ]
    
    employee = models.ForeignKey("employee.CustomUser", on_delete=models.CASCADE)
    from_date = models.DateField()
    till_date = models.DateField()
    applied_date = models.DateField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now =True)
    reason = models.TextField(max_length=50)
    leave_status = models.PositiveIntegerField(default=0, choices=LEAVE_STATUS_CHOICES )
    leave_status_text = models.CharField(max_length=60, default="Pending for approval")

    def save(self, *args, **kwargs):
        self.leave_status_text = dict(Leaves.LEAVE_STATUS_CHOICES)[self.leave_status]
        super().save(*args, **kwargs)
