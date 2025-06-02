from django.db import models

# For storing spam messages
class SpamMessage(models.Model):
    content = models.TextField()
    is_spam = models.BooleanField(default=False)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]

# For storing suspicious URLs
class SpamURL(models.Model):
    url = models.URLField()
    is_spam = models.BooleanField(default=False)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

# For storing fraudulent phone numbers
class SpamPhoneNumber(models.Model):
    phone_number = models.CharField(max_length=20)
    is_spam = models.BooleanField(default=False)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number
