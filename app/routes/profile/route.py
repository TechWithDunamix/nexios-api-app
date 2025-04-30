from nexios.routing import Router
from nexios.http import Request, Response
from nexios.auth.decorator import auth
from models.users import User
profile_router = Router(prefix="/profile", tags=["profile"])

@profile_router.get("/me", 
                    summary="Get user profile", 
                    description="Get user profile",
                    security=[{"bearerAuth": ["jwt"]}],
                    responses={200: User.me_schema()})
@auth(["jwt"])
async def get_user_profile(request: Request, response: Response) -> Response:
    return response.json(request.user.get_user_data())