from dataclasses import dataclass
from fake_useragent import UserAgent


@dataclass
class BrowserConfig:
    proxy: str = None
    custom_headers: dict = None
    user_agent: str = None
    browser_type: str = "firefox"
    headless: bool = False
    stealth_mode: bool = True
    timeout: int = 30000

    def __post_init__(self):
        self.user_agent = self.user_agent or UserAgent().random
        self.custom_headers = self.custom_headers or {
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Dest": "document"
        }
