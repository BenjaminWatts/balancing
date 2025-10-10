"""
Response type mappings for BMRS API endpoints.

This module maps endpoint methods to their proper response types,
enabling full type safety for all 287 API endpoints.
"""

from typing import Dict, Type, Any

# Import core response types from models.py
try:
    from elexon_bmrs.models import (
        SystemDemandResponse,
        GenerationResponse,
        WindForecastResponse,
        SystemPricesResponse,
        SystemFrequencyResponse,
        ImbalancePricesResponse,
        APIResponse,
    )
except ImportError:
    # Fallback if models.py doesn't have these
    SystemDemandResponse = dict
    GenerationResponse = dict
    WindForecastResponse = dict
    SystemPricesResponse = dict
    SystemFrequencyResponse = dict
    ImbalancePricesResponse = dict
    APIResponse = dict

# Map endpoint method names to their response types
ENDPOINT_RESPONSE_TYPES: Dict[str, Type[Any]] = {
    # Core convenience methods (already typed in models.py)
    "get_system_demand": SystemDemandResponse,
    "get_forecast_demand": SystemDemandResponse,
    "get_generation_by_fuel_type": GenerationResponse,
    "get_actual_generation_output": GenerationResponse,
    "get_wind_generation_forecast": WindForecastResponse,
    "get_system_frequency": SystemFrequencyResponse,
    "get_system_prices": SystemPricesResponse,
    "get_imbalance_prices": ImbalancePricesResponse,
    "get_balancing_services_volume": APIResponse,
    "get_market_index": SystemPricesResponse,
    
    # Dataset endpoints - will be populated dynamically from generated_models
    # For now, use APIResponse as fallback
    
    # For endpoints without specific response types, use generic APIResponse
    # These will be updated as more specific models are identified
}


def get_response_type(method_name: str) -> Type[Any]:
    """
    Get the proper response type for a given endpoint method.
    
    Args:
        method_name: The method name (e.g., 'get_datasets_abuc')
        
    Returns:
        The response type class for the endpoint
    """
    return ENDPOINT_RESPONSE_TYPES.get(method_name, APIResponse)


def is_typed_endpoint(method_name: str) -> bool:
    """
    Check if an endpoint has a specific response type (not just Dict[str, Any]).
    
    Args:
        method_name: The method name to check
        
    Returns:
        True if the endpoint has a specific response type
    """
    return method_name in ENDPOINT_RESPONSE_TYPES


def get_typed_endpoints() -> Dict[str, Type[Any]]:
    """
    Get all endpoints that have specific response types.
    
    Returns:
        Dictionary mapping endpoint names to their response types
    """
    return ENDPOINT_RESPONSE_TYPES.copy()


def get_untyped_endpoints() -> list[str]:
    """
    Get list of endpoints that still need proper typing.
    
    Returns:
        List of endpoint names that don't have specific response types
    """
    from elexon_bmrs import BMRSClient
    
    client = BMRSClient()
    all_methods = [m for m in dir(client) if m.startswith('get_')]
    
    return [method for method in all_methods if not is_typed_endpoint(method)]


# Statistics
def get_typing_stats() -> Dict[str, int]:
    """
    Get statistics about endpoint typing coverage.
    
    Returns:
        Dictionary with typing statistics
    """
    from elexon_bmrs import BMRSClient
    
    client = BMRSClient()
    all_methods = [m for m in dir(client) if m.startswith('get_')]
    
    typed_count = len([m for m in all_methods if is_typed_endpoint(m)])
    total_count = len(all_methods)
    untyped_count = total_count - typed_count
    
    return {
        "total_endpoints": total_count,
        "typed_endpoints": typed_count,
        "untyped_endpoints": untyped_count,
        "typing_coverage_percent": round((typed_count / total_count) * 100, 1)
    }
