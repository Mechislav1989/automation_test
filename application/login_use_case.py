from dataclasses import dataclass
import logging
import time

from application.base import UseCase
from domain.entities.user import User
from infrastructure.browser_service import BrowserService
from settings.configs.general import url_login


@dataclass
class LoginUseCase(UseCase[None]):
    _browser_service: BrowserService
    logger: logging.Logger
    
    @property
    def browser_service(self):
        return self._browser_service        

    async def execute(self,users: list[User]) -> None:
        self.logger.info(f"Found {len(users)} users to test. Logging in...{users}")

        for user in users:
            result = await self._attempt_login(self.browser_service, user)
            if result:
                return 

    async def get_users_credentials(self, url: str = url_login()) -> list[User] | None:
        async with self.browser_service as browser:
            await browser.go_to(url)
            return await browser.get_users_credentials()

    async def _attempt_login(self, browser: BrowserService, user: User) -> bool:
        try:
            await self._fill_credentials(user)
            await self._submit_login()

            if await self._is_login_successful():
                self._log_success(browser, user)
                return True
            else:
                self._log_failure(browser, user)
                return False

        except Exception as e:
            self._critical_error(e)
            return False

    async def _fill_credentials(self, user: User):
        await self.browser_service.fill('#user-name', user.username)
        await self.browser_service.fill('#password', user.password)

    async def _submit_login(self):
        await self.browser_service.click('[data-test="login-button"]')

    async def _is_login_successful(self) -> bool:
        return "inventory" in self.browser_service.current_url

    async def _log_success(self, browser: BrowserService, user: User) -> None:
        self.logger.info(f"User {user.username} logged in successfully.")
        await browser.take_screenshot(f"automation_screenshots/success_{user.username}.png")

    async def _log_failure(self, browser: BrowserService, user: User) -> None:
        self.logger.warning(f"User {user.username} failed to log in.")
        await browser.take_screenshot(f"automation_screenshots/failed_{user.username}.png")

    def _critical_error(self, error: Exception) -> None:
        self.logger.critical(f"Login failed: {str(error)}")
