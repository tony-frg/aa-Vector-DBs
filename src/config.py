from pathlib import Path
from typing import Tuple, Type

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource

# Define paths for the .env and .yaml configuration files
PACKAGE_ROOT = Path(__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
ENV_FILE_PATH = ROOT / ".env"
YAML_FILE_PATH = ROOT / "config.yml"


class Settings(BaseSettings):
    """
    Configuration settings class for loading environment-specific settings from both .env and YAML files.

    Attributes:
        openai_api_key (str): API key for OpenAI, loaded from the .env file.
        openai_em (str): OpenAI Embedding Model, loaded from the .env file.
        chroma_host (str): Host address for Chroma, loaded from the YAML file.
        chroma_port (int): Port number for Chroma, loaded from the YAML file.
    """

    openai_api_key: str
    openai_embedding_model: str

    chroma_host: str
    chroma_port: int

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, yaml_file=YAML_FILE_PATH)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """
        Customizes the settings loading order to prioritize dotenv and YAML files.

        Parameters:
            settings_cls (Type[BaseSettings]): The settings class.
            init_settings (PydanticBaseSettingsSource): Initial source settings (if any).
            env_settings (PydanticBaseSettingsSource): Environment variable settings.
            dotenv_settings (PydanticBaseSettingsSource): .env file settings.
            file_secret_settings (PydanticBaseSettingsSource): File-based secret settings.

        Returns:
            Tuple[PydanticBaseSettingsSource, ...]: Tuple defining the source priority, with dotenv first,
            followed by YAML as a fallback.
        """
        return (
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
        )


# Initialize settings to load from specified sources
settings = Settings()
