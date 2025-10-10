"""
Data models for BMRS API responses.

This module provides Pydantic models for type-safe API responses.
Auto-generated models are available in generated_models.py
"""

from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel, Field, ConfigDict


# Generic type variable for typed responses
T = TypeVar("T")


class APIResponse(BaseModel):
    """
    Generic API response wrapper.
    
    Most BMRS API endpoints return data in this format.
    """
    model_config = ConfigDict(extra='allow')

    data: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    total_records: Optional[int] = Field(default=None, alias="totalRecords")


class TypedAPIResponse(BaseModel, Generic[T]):
    """
    Generic typed API response wrapper.
    
    Use this for type-safe responses:
        response: TypedAPIResponse[DemandOutturn] = client.get_demand_typed(...)
    """
    model_config = ConfigDict(extra='allow')

    data: List[T] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    total_records: Optional[int] = Field(default=None, alias="totalRecords")


class StreamResponse(BaseModel):
    """Response for streaming endpoints."""
    model_config = ConfigDict(extra='allow')

    data: List[Dict[str, Any]] = Field(default_factory=list)


# ============================================================================
# Common Data Models (manually crafted for key endpoints)
# ============================================================================


class SettlementPeriod(BaseModel):
    """Model for settlement period data."""
    model_config = ConfigDict(extra='allow')

    settlement_date: str = Field(alias="settlementDate")
    settlement_period: int = Field(alias="settlementPeriod")
    start_time: Optional[datetime] = Field(default=None, alias="startTime")
    end_time: Optional[datetime] = Field(default=None, alias="endTime")


class GenerationByFuelType(BaseModel):
    """Model for generation by fuel type data."""
    model_config = ConfigDict(extra='allow')

    settlement_date: str = Field(alias="settlementDate")
    settlement_period: int = Field(alias="settlementPeriod")
    ccgt: Optional[float] = None  # Combined Cycle Gas Turbine
    oil: Optional[float] = None
    coal: Optional[float] = None
    nuclear: Optional[float] = None
    wind: Optional[float] = None
    ps: Optional[float] = None  # Pumped Storage
    npshyd: Optional[float] = None  # Non-Pumped Storage Hydro
    ocgt: Optional[float] = None  # Open Cycle Gas Turbine
    other: Optional[float] = None
    intfr: Optional[float] = None  # Interconnector France
    intirl: Optional[float] = None  # Interconnector Ireland
    intned: Optional[float] = None  # Interconnector Netherlands
    intew: Optional[float] = None  # East-West Interconnector
    biomass: Optional[float] = None


class SystemFrequency(BaseModel):
    """Model for system frequency data."""
    model_config = ConfigDict(extra='allow')

    timestamp: datetime
    frequency: float


class MarketIndex(BaseModel):
    """Model for market index data."""
    model_config = ConfigDict(extra='allow')

    settlement_date: str = Field(alias="settlementDate")
    settlement_period: int = Field(alias="settlementPeriod")
    price: float


class DemandData(BaseModel):
    """Model for electricity demand data."""
    model_config = ConfigDict(extra='allow')

    settlement_date: str = Field(alias="settlementDate")
    settlement_period: int = Field(alias="settlementPeriod")
    timestamp: Optional[datetime] = None
    demand: float  # in MW


class ImbalancePrice(BaseModel):
    """Model for imbalance pricing data."""
    model_config = ConfigDict(extra='allow')

    settlement_date: str = Field(alias="settlementDate")
    settlement_period: int = Field(alias="settlementPeriod")
    imbalance_price_gbp_per_mwh: float = Field(alias="imbalancePriceGbpPerMwh")


# ============================================================================
# Specific Response Types (one for each endpoint type)
# ============================================================================

class SystemDemandResponse(TypedAPIResponse["DemandData"]):
    """
    Typed response for system demand endpoints.
    
    Example:
        >>> response = client.get_system_demand(...)
        >>> for demand in response.data:
        >>>     print(f"{demand.settlement_date}: {demand.demand} MW")
    """
    pass


class GenerationResponse(TypedAPIResponse[GenerationByFuelType]):
    """Typed response for generation by fuel type endpoints."""
    pass


class WindForecastResponse(TypedAPIResponse["WindGenerationForecast"]):
    """Typed response for wind generation forecast endpoints."""
    pass


class SystemPricesResponse(TypedAPIResponse[MarketIndex]):
    """Typed response for system prices endpoints."""
    pass


class SystemFrequencyResponse(TypedAPIResponse[SystemFrequency]):
    """Typed response for system frequency endpoints."""
    pass


class ImbalancePricesResponse(TypedAPIResponse[ImbalancePrice]):
    """Typed response for imbalance prices endpoints."""
    pass

