from .base import BaseModel
from tortoise import fields  as f
from utils.auth import hash_password,check_password
class User(BaseModel):

    username = f.CharField(max_length=50, unique=True)
    email = f.CharField(max_length=100, unique=True)
    password = f.CharField(max_length=255)
    first_name = f.CharField(max_length=50, null=True)
    last_name = f.CharField(max_length=50, null=True)
    bio = f.TextField(null=True)
    profile_picture = f.CharField(max_length=255, null=True)
    def __str__(self):
        return self.username
    

    def set_password(self, password: str) -> None:
        """Set the password for the user, hashing it before storing."""
        self.password = hash_password(password)

    def check_password(self, password: str) -> bool:
        """Check the provided password against the stored hashed password."""
        return check_password(password, self.password)
    
    
    @classmethod
    async def create_user(cls, username: str, email: str, password: str, **kwargs) -> "User":
        """Create a new user with the given username, email, and password."""
        user = cls(username=username, email=email, **kwargs)
        user.set_password(password)
        await user.save()
        return user
    