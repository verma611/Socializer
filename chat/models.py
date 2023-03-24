from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Friend(models.Model):
    from_user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friends_of', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.from_user} - {self.to_user}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'from_user': self.from_user.username,
            'to_user': self.to_user.username,
        }
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_user', 'to_user'], name='unique_friend')
        ]



class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content}"

    def clean(self):
        
        if not Friend.objects.filter(from_user=self.sender, to_user=self.receiver).exists() and not Friend.objects.filter(from_user=self.receiver, to_user=self.sender).exists():
            raise ValidationError("Sender and receiver must be friends")