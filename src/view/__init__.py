__all__ = (
    "currencies_router",
    "exchange_rates_router",
    "exchange_router",
)

from src.view.currencies_views import router as currencies_router
from src.view.exchange_rates_views import router as exchange_rates_router
from src.view.exchange_view import router as exchange_router
