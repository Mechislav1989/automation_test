import os 
from dotenv import load_dotenv


load_dotenv()


def url_login() -> str:
    return os.getenv("URL_LOG")