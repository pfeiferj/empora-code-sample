from pydantic import (
    BaseSettings,
    Field,
)


class Settings(BaseSettings):
    """
    Base settings class for the application. Allows loading of configuration from environment variables.
    """

    smarty_api_key: str = Field(..., env="SMARTY_API_KEY")
    """
    The api secret key to use in requests to the smarty api.
    """

    smarty_api_id: str = Field(..., env="SMARTY_API_ID")
    """
    The api id to use in requests to the smarty api.
    """

    smarty_api_license: str = Field(default="us-core-cloud", env="SMARTY_API_LICENSE")
    """
    The api token to use in requests to the smarty api.
    """

    smarty_api_base_route: str = Field(default="https://us-street.api.smartystreets.com", env="SMARTY_API_BASE_ROUTE")
    """
    The server domain to use for requests to the smarty api.
    """

    class Config:
        # Allow loading environment variables from a file
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance of the settings class so we don't reparse variables
settings = (
    Settings()
)  # pyright: ignore[reportGeneralTypeIssues] Pydantic internally applies the logic for getting the fields
