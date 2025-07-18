from dataclasses import dataclass
from dotenv import dotenv_values


@dataclass
class Config:
    """
    Stores configuration loaded from a .env file or dict.

    Includes both Discord and MySQL settings.
    """
    # Discord settings
    discord_token: str
    discord_prefix: str
    discord_owner_id: int
    discord_join_message: str
    discord_activity_name: str
    discord_activity_type: str
    discord_status_type: str

    # MySQL settings
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = ""
    mysql_database: str = "tipbot_db"

    @classmethod
    def from_dict(cls, **kwargs) -> "Config":
        """ Create a Config object from a dictionary. """
        kwargs_overwrite = {}

        for k, v in kwargs.items():
            new_key = k.lower()

            # Auto-cast known int fields
            if new_key in ("discord_owner_id", "mysql_port"):
                try:
                    kwargs_overwrite[new_key] = int(v)
                except ValueError:
                    raise ValueError(f"Invalid int for {new_key}: {v}")
            else:
                kwargs_overwrite[new_key] = v

        return Config(**kwargs_overwrite)

    @classmethod
    def from_env(cls, filename: str = ".env") -> "Config":
        """ Create a Config object from a .env file. """
        return cls.from_dict(**dotenv_values(filename))
