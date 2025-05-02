import voltar as v
from schemas.object import Object


CreatePostSchema = Object({
    "title": v.String().max(255),
    "content": v.String()
})

# Schema for updating a post
UpdatePostSchema = Object({
    "title": v.String().max(255).optional(),
    "content": v.String().optional()
})

# Schema for post responses
PostResponseSchema = Object({
    "id": v.String(),
    "title": v.String(),
    "content": v.String(),
    "author_id": v.String(),
    "created_at": v.String(),
    "updated_at": v.String()
})

# Schema for not found error
NOT_FOUND_404 = Object({
    "error": v.String().default("Post not found")
}).pydantic_model("NotFound")

# Schema for forbidden error
FORBIDDEN_403 = Object({
    "error": v.String().default("You don't have permission to perform this action")
}).pydantic_model("Forbidden")
# Schema for listing posts
PostsListResponseSchema = Object({
    "posts": v.Array(PostResponseSchema)
}).pydantic_model("PostsList")
