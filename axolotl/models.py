class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    url = models.URLField()
    home_address = models.TextField()
    phone_number = models.PhoneNumberField()