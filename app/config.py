from nexios.config import MakeConfig

try:
    from dotenv import load_dotenv
    import os

    load_dotenv()
    env_config = {key: value for key, value in os.environ.items()}
except ImportError:
    env_config = {}

default_config = {
    "debug": True,
    "title": "App",
    "secret_key": env_config.get("SECRET_KEY"),
}

# Merge env config into default config
# Env config will override default if same keys exist
merged_config = {**default_config, **env_config}

app_config = MakeConfig(merged_config)


db_config = {
    "connections": {
        "default": app_config.DB_URL,
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # include aerich
            "default_connection": "default",
        }
    }
}
