from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, birthdate=None, profile_picture=None):
        if not email:
            raise ValueError("Email field must be set")
        
        email = self.normalize_email(email)
        
        if not username:
            raise ValueError("The Username field must be set")
        
        user = self.model(
            username=username,
            email=email,
            birthdate=birthdate,
            profile_picture=profile_picture,
        )
        
        user.set_password(password)
        user.save(using=self._db)  
        return user

    def create_superuser(self, username, email, password=None, birthdate=None, profile_picture=None):
        

        if not password:
            raise ValueError("Superusers must have a password")

        return self.create_user(username, email, password, birthdate, profile_picture)
