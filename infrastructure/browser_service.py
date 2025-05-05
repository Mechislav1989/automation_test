import asyncio
from dataclasses import dataclass, field
from itertools import zip_longest
import logging
import random
from typing import Any, Optional
from playwright.async_api import async_playwright, Page, Browser, BrowserContext, ElementHandle

from domain.entities.product import Product
from domain.entities.user import User
from infrastructure.handle_errors import handle_errors
from infrastructure.logger import configure_logger
from settings.configs.browser_config import BrowserConfig


@dataclass
class BrowserServiceState:
    current_url: str = ""
    page_count: int = 0
    error_count: int = 0
    
    def reset(self):
        self.current_url = ""
        self.page_count = 0
        self.error_count = 0


@dataclass
class BrowserService:
    config: BrowserConfig
    logger: logging.Logger
    state: BrowserServiceState = field(default_factory=BrowserServiceState)
    _playwright: Optional[Any] = field(default=None, init=False, repr=False)
    _browser: Optional[Browser] = field(default=None, init=False, repr=False)
    _context: Optional[BrowserContext] = field(default=None, init=False, repr=False)
    page: Optional[Page] = field(default=None, init=False, repr=False)

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.state.error_count += 1
            await self.take_screenshot(f"automation_screenshots/error_{self.state.error_count}.png")
        # await self.close()

    async def initialize(self) -> None:
        if not self.page or self.page.is_closed():
            self._playwright = await async_playwright().start()
            
            launch_options = {
                "headless": self.config.headless,
                "proxy": {"server": self.config.proxy} if self.config.proxy else None,
                "timeout": self.config.timeout
            }
            
            if self.config.browser_type == "firefox" and self.config.stealth_mode:
                launch_options.update({
                    "firefox_user_prefs": {
                        "privacy.resistFingerprinting": True,
                        "privacy.trackingprotection.enabled": True
                    }
                })
            
            self._browser = await getattr(self._playwright, self.config.browser_type).launch(**launch_options)
            self._context = await self._browser.new_context(
                user_agent=self.config.user_agent,
                extra_http_headers=self.config.custom_headers,
            )
            self.page = await self._context.new_page()
            await self._apply_stealth()
            self.state.page_count += 1


    async def _apply_stealth(self):
        if self.config.stealth_mode:
            await self.page.add_init_script("""
                () => {
                    delete navigator.__proto__.webdriver;
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => false,
                        configurable: true
                    });
                    window.chrome = {
                        runtime: {},
                        app: {
                            isInstalled: false,
                            InstallState: 'disabled',
                            RunningState: 'stopped'
                        }
                    };
                    const originalQuery = navigator.permissions.query;
                    navigator.permissions.query = (parameters) => (
                        parameters.name === 'notifications' ? 
                        Promise.resolve({ state: 'denied' }) :
                        originalQuery(parameters)
                    );
                }
            """)
            if self.config.browser_type == "firefox":
                await self.page.add_init_script(
                    """
                    WebGLRenderingContext.prototype.getParameter = function(parameter) {
                        if (parameter === 37445) return 'Intel Inc.'; // UNMASKED_VENDOR_WEBGL
                        if (parameter === 37446) return 'Intel Iris OpenGL Engine'; // UNMASKED_RENDERER_WEBGL
                        return Reflect.apply(WebGLRenderingContext.prototype.getParameter, this, [parameter]);
                    };
                    """
                )

    @handle_errors(log_message="Navigation failed")
    async def go_to(self, url: str) -> None:
        await self.page.goto(url)
        self.state.current_url = url
        

    @handle_errors(log_message="Failed to fill input")
    async def fill(self, selector: str, value: str) -> None:
        await self.page.fill(selector, value)
        await self.page.wait_for_timeout(random.randint(100, 500))
        
    @handle_errors(log_message="Failed to click element")
    async def click(self, selector: str) -> None:
        await self.page.click(selector)
        await self.page.wait_for_timeout(random.randint(200, 800))    

    async def paginate(self, selector: str) -> None:
        #TODO implement pagination logic
        ...
    
    @handle_errors(log_message="Failed to get element text")
    async def get_element_text(self, page: Page, selector: str) -> str:
        element = await page.query_selector(selector)
        text = await element.inner_text() if element else ""
        return text.replace('$', '').strip() if text else ""
    
    @handle_errors(log_message="Failed to get element attribute")
    async def get_element_attr(self, page: Page, selector: str, attribute: str) -> str:
        element = await page.query_selector(selector)
        return await element.get_attribute(attribute) if element else ""

    async def get_users_credentials(self) -> list[User] | None:
        usernames_elements = await self.page.query_selector_all('.login_credentials')
        password_element = await self.page.query_selector_all('.login_password')
        usernames = [
            user.strip() for user in await self.extract_elements(usernames_elements) if 'Accepted' not in user and user
        ]
        password = [
            passw.strip() for passw in await self.extract_elements(password_element) if 'all users' not in passw
        ]

        if not usernames or not password:
            self.logger.error(f'Username or password elements not found on the page: {self.page.url}')
            return None

        users = [
            User(i[0] if i[0] else '', i[1] if i[1] else '')
            for i in zip_longest(usernames, password, fillvalue=password[0])
        ]
        # users.sort(key=lambda x: x.username)
        random.shuffle(users)
        self.logger.info(f"Found {len(users)} users on the page: {self.page.url}")
        return users

    async def extract_elements(self, elements: list[ElementHandle]) -> list[str]:
        texts = await asyncio.gather(*(i.inner_text() for i in elements))
        return [text.split('\n') for text in texts][0]

    async def extract_products(self) -> list[Product]:
        items = await self.page.query_selector_all('div.inventory_item')
        # https://www.saucedemo.com/inventory-item.html?id=4
        self.logger.info(f"Found {len(items)} items on the page: {self.page.url}")
        return [
            Product(
                await self.get_element_text(item, '[data-test="inventory-item-name"]'),
                await self.get_element_text(item, '.inventory_item_price'),
            )
            for item in items
        ]

    async def get_validation_errors(self) -> list[str]:
        elements = await self.page.query_selector_all(".error-message-container")
        return [await element.inner_text() for element in elements]

    async def take_screenshot(self, path: str) -> None:
        await self.page.screenshot(path=path)

    async def _capture_error_evidence(self):
        try:
            await self.take_screenshot(
                f"automation_screenshots/error_{self.state.error_count}.png"
            )
            await self.page.screenshot(
                path=f"automation_screenshots/fullpage_{self.state.error_count}.png",
                full_page=True
            )
        except Exception as capture_error:
            self.logger.error(f"Failed to capture evidence: {str(capture_error)}")

    @property
    def current_url(self) -> str:
        return self.page.url

    async def close(self) -> None:
        await self._context.close()
        await self._browser.close()
        await self._playwright.stop()
