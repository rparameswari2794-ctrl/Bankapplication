from django.db import models

ACCOUNT_CHOICES = [
    ('Savings', 'Savings'),
    ('Current', 'Current'),
]

INCOME_CHOICES = [
    ('Below 1 Lakh', 'Below 1 Lakh'),
    ('1-5 Lakh', '1-5 Lakh'),
    ('Above 5 Lakh', 'Above 5 Lakh'),
]

class BankApplication(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    address_line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICES)
    occupation = models.CharField(max_length=50)
    income_range = models.CharField(max_length=20, choices=INCOME_CHOICES)
    nominee_name = models.CharField(max_length=50)
    nomination_relation = models.CharField(max_length=50)
    nominee_dob = models.DateField()
    pan_number = models.CharField(max_length=10)
    aadhaar_number = models.CharField(max_length=12)
    voter_id = models.CharField(max_length=15, blank=True, null=True)
    driving_license = models.CharField(max_length=20, blank=True, null=True)
    
    # File uploads
    pan_card_image = models.FileField(upload_to='documents/')
    aadhaar_front_image = models.FileField(upload_to='documents/')
    passport_photo = models.ImageField(upload_to='photos/')
    
    agree_terms = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"