from nexios import get_application
from routes.index.route import index_router
from routes.auth.route import auth_router
from config import app_config
from utils.db import init_db, close_db

# Create the application
app = get_application(title="App", config=app_config)


app.mount_router(index_router)
app.mount_router(auth_router)

app.on_startup(init_db)
app.on_shutdown(close_db)