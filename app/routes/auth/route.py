from nexios.routing import Router
from nexios.http import Request, Response
from schemas.auth import CreateUserSchema, LoginUserSchema

from schemas.responses import ERROR_400, SUCCESS_200, SUCCESS_201
import voltar as v
from voltar.pydantic_converter import convert_object
from schemas.object import Object
from models.users import User
from nexios.auth.backends.jwt import create_jwt
from datetime import datetime, timedelta
from pytz import UTC
auth_router = Router(prefix="/auth", tags=["auth"])



@auth_router.post("/signup",
                  request_model=CreateUserSchema.pydantic_model("CreateUser"),
                  summary="Create a new user",description="Create a new user in the system",
                  responses={
                      400: ERROR_400,
                      201: SUCCESS_201,
                      409: Object({
                          "error": v.String().default("User already exists")
                      }).pydantic_model("UserAlreadyExists"),
                  })
async def create_user(request: Request, response:Response) -> Response:
   
      """Create a new user in the system.
   
      Args:
         request (Request): The request object.
         response (Response): The response object.
   
      Returns:
         Response: The response object.
      """
      data = await request.json
      try:
         user_data = await CreateUserSchema.validate_async(data)
      except v.ValidationError as e:
         return response.json({"error": e.error_dict}, status_code=400)
      
      check_user = await User.get_or_none(email=user_data["email"])
      if check_user:
         return response.json({"error": "User already exists"}, status_code=409)
      await User.create_user(
        **user_data
      )
      return response.json({"message": "User created successfully"}, status_code=201)



@auth_router.post("/login",
                  request_model=LoginUserSchema.pydantic_model("LoginUser"),
                  summary="Login a user",description="Login a user in the system",
                  responses={
                      400: ERROR_400,
                      200: Object({
                          "message": v.String(),
                          "access_token": v.String(),
                          "refresh_token": v.String()
                      }).pydantic_model("LoginUserResponse"),
                  })
async def login_user(request: Request, response:Response) -> Response:
   
      """Login a user in the system.
   
      Args:
         request (Request): The request object.
         response (Response): The response object.
   
      Returns:
         Response: The response object.
      """
      data = await request.json
      try:
         user_data = await LoginUserSchema.validate_async(data)
      except v.ValidationError as e:
         return response.json({"error": e.error_dict}, status_code=400)
      

      user = await User.get_or_none(email=user_data["email"])
      if not user or not  user.check_password(user_data["password"]):
         return response.json({"error": "Invalid email or password"}, status_code=400)
      
      user.check_password(user_data["password"])
      access_token = create_jwt(
         {"user_id":str(user.id), 
          "email": user.email,
            "exp": datetime.now(UTC) + timedelta(minutes=30), # 30 minutes expiration time
          }
      )
      refresh_token = create_jwt(
         {"user_id":str(user.id), 
          "email": user.email,
            "exp": datetime.now(UTC) + timedelta(days=7), # 7 days expiration time
          }
      )
      return response.json({
          "message": "User logged in successfully",
          "access_token": access_token, "refresh_token": refresh_token}, status_code=200)