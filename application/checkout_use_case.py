from dataclasses import dataclass
import logging

from application.base import UseCase
from infrastructure.browser_service import BrowserService


@dataclass
class CheckoutUseCase(UseCase[dict[str, str]]):
    _browser_service: BrowserService
    logger: logging.Logger
    
    @property
    def browser_service(self):
        return self._browser_service

    async def execute(self) -> dict[str, str]:
        """Simulate checkout with missing data and return validation results"""
        result = {'errors': [], 'screenshot': None}
        try: 
            # 1. Add product to cart
            await self.browser_service.click('[data-test="add-to-cart-sauce-labs-backpack"]')

            # 2. Go to cart
            await self.browser_service.click('.shopping_cart_link')

            # 3. Proceed to checkout
            await self.browser_service.click('[data-test="checkout"]')
            
            # 4. Fill in checkout information
            await self.browser_service.fill('[data-test="lastName"]', 'Doe')
            await self.browser_service.fill('[data-test="postalCode"]', '12345')
            
            # 5. Attempt to continue
            await self.browser_service.click('[data-test="continue"]')
            
            # 6. Validate errors
            errors = await self.browser_service.get_validation_errors()
            result['errors'] = errors
            
            # 7. Take screenshot
            screenshot_path = 'automation_screenshots/checkout_validation_error.png'
            await self.browser_service.take_screenshot(screenshot_path)
            result['screenshot'] = screenshot_path
            
            # 8. Reset state
            await self.browser_service.click('[data-test="cancel"]')
            await self.browser_service.click('#continue-shopping')
            await self.browser_service.page.wait_for_selector('#inventory_container', state='visible')
            
        except Exception as e:
            self.logger.error(f'Checkout attempt failed: {str(e)}')
            await self.browser_service.take_screenshot('automation_screenshots/checkout_attempt_failure.png')
            raise
        
        await self.browser_service.close()
        self.logger.info(f"Checkout validation completed with errors: {result['errors']}")
        return result