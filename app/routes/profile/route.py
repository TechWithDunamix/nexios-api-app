from nexios.routing import Router
from nexios.http import Request, Response
from nexios.auth.decorator import auth
from models.users import User
import voltar as v
from schemas.object import Object
from schemas.responses import ERROR_400, SUCCESS_200
profile_router = Router(prefix="/profile", tags=["profile"])

# Schema for updating user profile
UpdateProfileSchema = Object({
    "first_name": v.String().max(50).optional(),
    "last_name": v.String().max(50).optional(),
    "bio": v.String().optional(),
    "profile_picture": v.String().max(255).optional()
})

@profile_router.get("/me", 
                    summary="Get user profile", 
                    description="Get user profile",
                    security=[{"bearerAuth": ["jwt"]}],
                    responses={200: User.me_schema()})
@auth(["jwt"])
async def get_user_profile(request: Request, response: Response) -> Response:
    return response.json(request.user.get_user_data())

@profile_router.patch("/me", 
                    summary="Update user profile", 
                    description="Update user profile information",
                    security=[{"bearerAuth": ["jwt"]}],
                    request_model=UpdateProfileSchema.pydantic_model("UpdateProfile"),
                    responses={
                        200: User.me_schema(),
                        400: ERROR_400
                    })
@auth(["jwt"])
async def update_user_profile(request: Request, response: Response) -> Response:
    """Update the authenticated user's profile information.
    
    Args:
        request (Request): The request object containing the user and update data.
        response (Response): The response object.
        
    Returns:
        Response: The response object with updated user data.
    """
    data = await request.json
    try:
        update_data = await UpdateProfileSchema.validate_async(data)
    except v.ValidationError as e:
        return response.json({"errors": {"message": e.error_dict}}, status_code=400)
    
    user = request.user
    
    # Update user fields that are provided in the request
    for field, value in update_data.items():
        setattr(user, field, value)
    
    # Save the updated user
    await user.save()
    
    # Return the updated user data
    return response.json(user.get_user_data())
