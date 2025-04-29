import voltar as v
from .object import Object
CreateUserSchema = Object({
    "username": v.String().lowercase().min(3).max(20).pattern(r"^[a-zA-Z0-9_]+$"),
    "email":v.String().lowercase().email(),
    "password": v.String().min(8).max(100).pattern(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"),
    "bio": v.String().max(255).optional(),
    "first_name": v.String().max(50).optional(),
    "last_name": v.String().max(50).optional(),
    "profile_picture": v.String().optional()

})


LoginUserSchema = Object({
    "email":v.String().lowercase().email().optional(),
    "password": v.String().min(8).max(100).pattern(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"),
})