"""
Typed wrapper for BMRSClient that provides proper response types for all endpoints.

This module creates a fully typed client by wrapping the generated methods
with proper return type annotations based on the endpoint response models.
"""

from typing import Any, Dict, List, Optional, Type, Union, get_type_hints
from datetime import date, datetime
import inspect

from elexon_bmrs.client import BMRSClient
from elexon_bmrs.response_types import get_response_type, get_typed_endpoints


class TypedBMRSClient(BMRSClient):
    """
    Fully typed BMRS client with proper response types for all endpoints.
    
    This client extends BMRSClient to provide type-safe responses for all 287 endpoints.
    Each method returns the appropriate Pydantic model instead of Dict[str, Any].
    
    Example:
        >>> from elexon_bmrs import TypedBMRSClient
        >>> 
        >>> client = TypedBMRSClient(api_key="your-key")
        >>> 
        >>> # Fully typed response
        >>> abuc_data = client.get_datasets_abuc(
        ...     publishDateTimeFrom="2024-01-01T00:00:00Z",
        ...     publishDateTimeTo="2024-01-02T00:00:00Z"
        ... )
        >>> # abuc_data is now AbucDatasetRow_DatasetResponse, not Dict[str, Any]
        >>> 
        >>> # Type-safe access
        >>> for row in abuc_data.data or []:
        ...     print(f"Dataset: {row.dataset}, PSR: {row.psrType}")
    """
    
    def __getattribute__(self, name: str):
        """
        Override attribute access to provide typed methods.
        
        For methods that start with 'get_', we return a wrapper that provides
        proper type hints and response parsing.
        """
        attr = super().__getattribute__(name)
        
        # Only wrap get_ methods that have specific response types
        if (name.startswith('get_') and 
            callable(attr) and 
            name in get_typed_endpoints()):
            
            return self._create_typed_method(name, attr)
        
        return attr
    
    def _create_typed_method(self, method_name: str, original_method):
        """
        Create a typed wrapper for a method.
        
        Args:
            method_name: Name of the method
            original_method: The original method from GeneratedBMRSMethods
            
        Returns:
            Wrapped method with proper type hints and response parsing
        """
        response_type = get_response_type(method_name)
        
        def typed_method(*args, **kwargs):
            """Typed wrapper for the original method."""
            # Call the original method
            response_data = original_method(*args, **kwargs)
            
            # Parse response with the appropriate Pydantic model
            if isinstance(response_data, dict):
                try:
                    return response_type(**response_data)
                except Exception as e:
                    # If parsing fails, return the raw data but log the error
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(
                        f"Failed to parse response for {method_name} as {response_type.__name__}: {e}. "
                        f"Returning raw data."
                    )
                    return response_data
            else:
                return response_data
        
        # Copy the original method's signature and docstring
        typed_method.__name__ = original_method.__name__
        typed_method.__doc__ = original_method.__doc__
        typed_method.__module__ = original_method.__module__
        
        # Set the return type annotation
        typed_method.__annotations__ = {
            **original_method.__annotations__,
            'return': response_type
        }
        
        return typed_method
    
    def get_typing_info(self) -> Dict[str, Any]:
        """
        Get information about the typing coverage of this client.
        
        Returns:
            Dictionary with typing information
        """
        from elexon_bmrs.response_types import get_typing_stats
        
        stats = get_typing_stats()
        typed_endpoints = get_typed_endpoints()
        
        return {
            "typing_stats": stats,
            "typed_endpoints": list(typed_endpoints.keys()),
            "untyped_endpoints": [m for m in dir(self) if m.startswith('get_') 
                                 and m not in typed_endpoints]
        }


# Convenience function to create a typed client
def create_typed_client(api_key: Optional[str] = None, **kwargs: Any) -> TypedBMRSClient:
    """
    Create a fully typed BMRS client.
    
    Args:
        api_key: BMRS API key (optional but recommended)
        **kwargs: Additional arguments for BMRSClient
        
    Returns:
        TypedBMRSClient instance with proper response types
        
    Example:
        >>> from elexon_bmrs import create_typed_client
        >>> 
        >>> client = create_typed_client(api_key="your-key")
        >>> 
        >>> # All methods now return properly typed responses
        >>> abuc_data = client.get_datasets_abuc(...)  # Returns AbucDatasetRow_DatasetResponse
        >>> freq_data = client.get_datasets_freq(...)  # Returns appropriate response type
    """
    return TypedBMRSClient(api_key=api_key, **kwargs)


# Export the typed client
__all__ = ['TypedBMRSClient', 'create_typed_client']
