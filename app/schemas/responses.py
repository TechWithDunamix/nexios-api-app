import voltar as v
from .object import Object
ERROR_400 = Object({
    "errors" : v.Object({
        "message": v.String(),
    })
}).pydantic_model("Error400")


SUCCESS_200 = Object({
    "message": v.String(),
}).pydantic_model("Success200")

SUCCESS_201 = Object({
    "message": v.String(),
}).pydantic_model("Success201")