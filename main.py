import asyncio

from application.checkout_use_case import CheckoutUseCase
from application.extract_products_use_case import ExtractProductsUseCase
from application.login_use_case import LoginUseCase
from settings.containers import get_container


async def main():
    container = get_container()
    # Use case execution
    # Login to the application
    login_uc = container.resolve(LoginUseCase)
    users = await login_uc.get_users_credentials()
    await login_uc.execute(users)

    # Extract products after login
    extract_uc = container.resolve(ExtractProductsUseCase)
    await extract_uc.execute()

    # Checkout after extracting products
    checkout_uc = container.resolve(CheckoutUseCase)
    await checkout_uc.execute()


if __name__ == "__main__":
    asyncio.run(main())