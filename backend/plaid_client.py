from plaid import ApiClient, Configuration, Environment
from plaid.api import plaid_api
from backend.config import settings


def get_plaid_client():
    """Initialize and return Plaid API client."""
    env = settings.PLAID_ENV.lower()
    host = {
        "sandbox": Environment.Sandbox,
        "production": Environment.Production,
    }.get(env, Environment.Sandbox)

    plaid_config = Configuration(
        host=host,
        api_key={
            "clientId": settings.PLAID_CLIENT_ID,
            "secret": settings.PLAID_SECRET,
        },
    )
    return plaid_api.PlaidApi(ApiClient(plaid_config))


plaid_client = get_plaid_client()
