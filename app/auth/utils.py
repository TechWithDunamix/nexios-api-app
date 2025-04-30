from models.users import User


async def get_user_from_payload(**payload: dict) -> dict:
    return await User.get_or_none(id=payload["user_id"])