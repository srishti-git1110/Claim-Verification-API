import dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

dotenv.load_dotenv()
class APIConfig(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    claimbuster_api_key: str = Field(..., env="CLAIMBUSTER_API_KEY")
    serpapi_api_key: str = Field(..., env="SERPAPI_API_KEY")
    
config = APIConfig()