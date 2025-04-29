from tortoise import Tortoise
from config import db_config
from nexios.logging import create_logger

logger = create_logger("app.utils.db")
async def init_db():
    """Initialize the database connection."""
    await Tortoise.init(
        config=db_config,
    )
    await Tortoise.generate_schemas()


    logger.info("Database connection established.")


async def close_db():
    """Close the database connection."""
    await Tortoise.close_connections()
    logger.info("Database connection closed.")