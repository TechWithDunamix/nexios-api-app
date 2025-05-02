from nexios.routing import Router
from nexios.http import Request, Response
from nexios.auth.decorator import auth
from models.posts import Post
from schemas.responses import ERROR_400, SUCCESS_200, SUCCESS_201
from schemas.posts import CreatePostSchema, PostResponseSchema,PostsListResponseSchema,NOT_FOUND_404,FORBIDDEN_403,UpdatePostSchema
from tortoise.exceptions import DoesNotExist 
from uuid import UUID
import voltar as v
posts_router = Router(prefix="/posts", tags=["posts"])



# Convert post to dict for response
def post_to_dict(post):
    return {
        "id": str(post.id),
        "title": post.title,
        "content": post.content,
        "author_id": str(post.author_id),
        "created_at": str(post.created_at),
        "updated_at": str(post.updated_at)
    }

@posts_router.post("/",
                  request_model=CreatePostSchema.pydantic_model("CreatePost"),
                  summary="Create a new post",
                  description="Create a new post in the system",
                  responses={
                      400: ERROR_400,
                      201: SUCCESS_201,
                  },
                  security=[{"bearerAuth": ["jwt"]}])
@auth(["jwt"])
async def create_post(request: Request, response: Response) -> Response:
    """Create a new post in the system.
    
    Args:
        request (Request): The request object containing user and post data.
        response (Response): The response object.
        
    Returns:
        Response: The response object with success message.
    """
    data = await request.json
    try:
        post_data = await CreatePostSchema.validate_async(data)
    except v.ValidationError as e:
        return response.json({"error": e.error_dict}, status_code=400)
    
    # Create the post with current user as author
    await Post.create(
        title=post_data["title"],
        content=post_data["content"],
        author=request.user
    )
    
    return response.json({"message": "Post created successfully"}, status_code=201)


@posts_router.get("/",
                 summary="List all posts",
                 description="Get a list of all posts in the system",
                 responses={
                     200: PostsListResponseSchema,
                 })
async def list_posts(request: Request, response: Response) -> Response:
    """Get a list of all posts in the system.
    
    Args:
        request (Request): The request object.
        response (Response): The response object.
        
    Returns:
        Response: The response object with posts list.
    """
    # Get all posts with related author information
    posts = await Post.all().prefetch_related('author')
    
    # Convert posts to dict format
    posts_list = [post_to_dict(post) for post in posts]
    
    return response.json({"posts": posts_list})


@posts_router.get("/{post_id}",
                 summary="Get a specific post",
                 description="Get details of a specific post by ID",
                 responses={
                     200: PostResponseSchema.pydantic_model("PostResponse"),
                     404: NOT_FOUND_404,
                 })
async def get_post(request: Request, response: Response, post_id: str) -> Response:
    """Get a specific post by ID.
    
    Args:
        request (Request): The request object.
        response (Response): The response object.
        post_id (str): The ID of the post to retrieve.
        
    Returns:
        Response: The response object with post data.
    """
    try:
        # Validate UUID format
        post_uuid = UUID(post_id)
        
        # Get the post
        post = await Post.get(id=post_uuid)
        
        return response.json(post_to_dict(post))
    except ValueError:
        # Invalid UUID format
        return response.json({"error": "Invalid post ID format"}, status_code=400)
    except DoesNotExist:
        # Post not found
        return response.json({"error": "Post not found"}, status_code=404)


@posts_router.patch("/{post_id}",
                   request_model=UpdatePostSchema.pydantic_model("UpdatePost"),
                   summary="Update a post",
                   description="Update an existing post",
                   responses={
                       200: PostResponseSchema.pydantic_model("PostResponse"),
                       400: ERROR_400,
                       403: FORBIDDEN_403,
                       404: NOT_FOUND_404,
                   },
                   security=[{"bearerAuth": ["jwt"]}])
@auth(["jwt"])
async def update_post(request: Request, response: Response, post_id: str) -> Response:
    """Update an existing post.
    
    Args:
        request (Request): The request object containing the update data.
        response (Response): The response object.
        post_id (str): The ID of the post to update.
        
    Returns:
        Response: The response object with updated post data.
    """
    try:
        # Validate UUID format
        post_uuid = UUID(post_id)
        
        # Get the post
        post = await Post.get(id=post_uuid).prefetch_related('author')
        
        # Check if the user is the author
        if post.author.id != request.user.id:
            return response.json(
                {"error": "You don't have permission to update this post"}, 
                status_code=403
            )
        
        # Validate input data
        data = await request.json
        try:
            update_data = await UpdatePostSchema.validate_async(data)
        except v.ValidationError as e:
            return response.json({"error": e.error_dict}, status_code=400)
        
        # Update the post fields
        if "title" in update_data:
            post.title = update_data["title"]
        if "content" in update_data:
            post.content = update_data["content"]
        
        # Save the updated post
        await post.save()
        
        return response.json(post_to_dict(post))
    except ValueError:
        # Invalid UUID format
        return response.json({"error": "Invalid post ID format"}, status_code=400)
    except DoesNotExist:
        # Post not found
        return response.json({"error": "Post not found"}, status_code=404)


@posts_router.delete("/{post_id}",
                    summary="Delete a post",
                    description="Delete an existing post",
                    responses={
                        200: SUCCESS_200,
                        403: FORBIDDEN_403,
                        404: NOT_FOUND_404,
                    },
                    security=[{"bearerAuth": ["jwt"]}])
@auth(["jwt"])
async def delete_post(request: Request, response: Response, post_id: str) -> Response:
    """Delete an existing post.
    
    Args:
        request (Request): The request object.
        response (Response): The response object.
        post_id (str): The ID of the post to delete.
        
    Returns:
        Response: The response object with success message.
    """
    try:
        # Validate UUID format
        post_uuid = UUID(post_id)
        
        # Get the post
        post = await Post.get(id=post_uuid).prefetch_related('author')
        
        # Check if the user is the author
        if post.author.id != request.user.id:
            return response.json(
                {"error": "You don't have permission to delete this post"}, 
                status_code=403
            )
        
        # Delete the post
        await post.delete()
        
        return response.json({"message": "Post deleted successfully"})
    except ValueError:
        # Invalid UUID format
        return response.json({"error": "Invalid post ID format"}, status_code=400)
    except DoesNotExist:
        # Post not found
        return response.json({"error": "Post not found"}, status_code=404)
