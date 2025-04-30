from nexios import get_application
from routes.index.route import index_router
from routes.auth.route import auth_router
from routes.profile.route import profile_router
from config import app_config
from utils.db import init_db, close_db
from auth.middleware import middleware as auth_middleware
app = get_application(title="App", config=app_config)


app.mount_router(index_router)
app.mount_router(auth_router)
app.mount_router(profile_router)

app.on_startup(init_db)
app.on_shutdown(close_db)
app.add_middleware(auth_middleware)