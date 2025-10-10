"""
Elexon BMRS Python Client Library

A Python client for accessing the Elexon BMRS (Balancing Mechanism Reporting Service) API.
This library provides easy access to UK electricity market data with full type safety.
"""

from elexon_bmrs.client import BMRSClient
from elexon_bmrs.typed_client import TypedBMRSClient, create_typed_client
from elexon_bmrs.exceptions import (
    BMRSException,
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)
from elexon_bmrs.models import (
    APIResponse,
    TypedAPIResponse,
    DemandData,
    GenerationByFuelType,
    ImbalancePrice,
    MarketIndex,
    SettlementPeriod,
    SystemFrequency,
    # Specific response types
    SystemDemandResponse,
    GenerationResponse,
    WindForecastResponse,
    SystemPricesResponse,
    SystemFrequencyResponse,
    ImbalancePricesResponse,
)
# Import commonly used enums
from elexon_bmrs.enums import (
    DatasetEnum,
    PsrtypeEnum,
    FueltypeEnum,
    BusinesstypeEnum,
    MessagetypeEnum,
    EventtypeEnum,
    FlowdirectionEnum,
    SettlementruntypeEnum,
    MarketagreementtypeEnum,
    AssettypeEnum,
    EventstatusEnum,
    UnavailabilitytypeEnum,
    TradedirectionEnum,
    BoundaryEnum,
    BmunittypeEnum,
    ProcesstypeEnum,
    WarningtypeEnum,
    PricederivationcodeEnum,
    SystemzoneEnum,
    AmendmentflagEnum,
    RecordtypeEnum,
    DeliverymodeEnum,
)

__version__ = "0.1.0"
__all__ = [
    "BMRSClient",
    "TypedBMRSClient",  # Fully typed client with proper response types
    "create_typed_client",  # Convenience function
    "BMRSException",
    "APIError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "APIResponse",
    "TypedAPIResponse",
    "DemandData",
    "GenerationByFuelType",
    "ImbalancePrice",
    "MarketIndex",
    "SettlementPeriod",
    "SystemFrequency",
    # Specific response types
    "SystemDemandResponse",
    "GenerationResponse",
    "WindForecastResponse",
    "SystemPricesResponse",
    "SystemFrequencyResponse",
    "ImbalancePricesResponse",
    # Commonly used enums
    "DatasetEnum",
    "PsrtypeEnum",
    "FueltypeEnum",
    "BusinesstypeEnum",
    "MessagetypeEnum",
    "EventtypeEnum",
    "FlowdirectionEnum",
    "SettlementruntypeEnum",
    "MarketagreementtypeEnum",
    "AssettypeEnum",
    "EventstatusEnum",
    "UnavailabilitytypeEnum",
    "TradedirectionEnum",
    "BoundaryEnum",
    "BmunittypeEnum",
    "ProcesstypeEnum",
    "WarningtypeEnum",
    "PricederivationcodeEnum",
    "SystemzoneEnum",
    "AmendmentflagEnum",
    "RecordtypeEnum",
    "DeliverymodeEnum",
]

