from .base import BaseModel
from tortoise import fields  as f
from utils.auth import hash_password,check_password
from nexios.auth.base import BaseUser
import voltar as v
from schemas.object import Object
class User(BaseModel, BaseUser):

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
    
    @property
    def is_authenticated(self) -> bool:
        """Check if the user is authenticated."""
        return True  # In this case, we assume the user is always authenticated.
    @property
    def is_active(self) -> bool:
        """Check if the user is active."""
        return True  # In this case, we assume the user is always active.
    

    @property
    def user_id(self) -> int:
        """Get the user ID."""
        return self.id
    

    @classmethod
    def me_schema(cls) -> Object:
        return Object({
            "email" : v.String().email(),
            "username" : v.String().min(3).max(20).pattern(r"^[a-zA-Z0-9_]+$"),
            "first_name" : v.String().optional().default("John"),
            "last_name" : v.String().optional().default("Doe"),
            "bio" : v.String().optional().default("i am Human"),
            "profile_picture" : v.String().optional().default("https://example.com/profile.jpg"),
        }).pydantic_model("MyProfile")
    

    def get_user_data(self) -> dict:
        return {
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bio": self.bio,
            "profile_picture": self.profile_picture,
        }