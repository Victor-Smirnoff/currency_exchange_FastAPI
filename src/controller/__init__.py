__all__ = (
    "currencies_router",
    "exchange_rates_router",
    "exchange_router",
)

from src.controller.currencies_controller import router as currencies_router
from src.controller.exchange_rates_controller import router as exchange_rates_router
from src.controller.exchange_controller import router as exchange_router
