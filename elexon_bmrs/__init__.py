"""
Elexon BMRS Python Client Library

A Python client for accessing the Elexon BMRS (Balancing Mechanism Reporting Service) API.
This library provides easy access to UK electricity market data with full type safety.
"""

from elexon_bmrs.client import BMRSClient
# TypedBMRSClient removed - all typing is now in BMRSClient
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
    # BOALF and Balancing Mechanism models
    BOALF,
    BOD,
    PN,
    B1610,
    SettlementStackPair,
    AcceptedVolumes,
    BOALFResponse,
    BODResponse,
    PNResponse,
    B1610Response,
)
# Import manually created models for previously untyped endpoints
from elexon_bmrs.untyped_models import (
    HealthCheckResponse,
    CDNResponse,
    DemandResponse,
    InitialDemandOutturn,
    DemandSummaryItem,
    RollingSystemDemandResponse,
    DemandTotalActualResponse,
    GenerationCurrentItem,
    HalfHourlyInterconnectorResponse,
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

__version__ = "0.3.0"
__all__ = [
    "BMRSClient",
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
    # BOALF and Balancing Mechanism models
    "BOALF",
    "BOD",
    "PN",
    "B1610",
    "SettlementStackPair",
    "AcceptedVolumes",
    "BOALFResponse",
    "BODResponse",
    "PNResponse",
    "B1610Response",
    # Manual models for previously untyped endpoints
    "HealthCheckResponse",
    "CDNResponse",
    "DemandResponse",
    "InitialDemandOutturn",
    "DemandSummaryItem",
    "RollingSystemDemandResponse",
    "DemandTotalActualResponse",
    "GenerationCurrentItem",
    "HalfHourlyInterconnectorResponse",
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

