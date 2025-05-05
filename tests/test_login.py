from application.login_use_case import LoginUseCase
import pytest

from domain.entities.user import User
from settings.configs.general import url_login


@pytest.mark.asyncio
async def test_successful_login(container):
    login_uc = container.resolve(LoginUseCase)
    async with login_uc.browser_service as browser:
        await browser.go_to(url_login())   
        users = [User(username="standard_user", password="secret_sauce")]
        await login_uc.execute(users)
        
        page = login_uc.browser_service.page
        await page.wait_for_selector("#inventory_container")
        content = await page.content()
        
        assert "inventory" in page.url
        assert "Sauce Labs Backpack" in content


@pytest.mark.asyncio
async def test_failed_login(container):
    login_uc = container.resolve(LoginUseCase)
    async with login_uc.browser_service as browser:
        await browser.go_to(url_login())
        users = [User(username="invalid_user", password="wrong_password")]
        await login_uc.execute(users)

        page = login_uc.browser_service.page
        error = await page.content()

        assert "Epic sadface: Username and password do not match any user in this service" in error