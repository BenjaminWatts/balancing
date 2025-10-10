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


# ==================== BOALF and Balancing Mechanism Models ====================

class BOALF(BaseModel):
    """BOALF (Bid Offer Acceptance Level Flag) - Balancing Mechanism Acceptances."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    acceptance_number: int = Field(alias="acceptanceNumber")
    acceptance_time: datetime = Field(alias="acceptanceTime")
    bmu_id: str = Field(alias="bmUnit")
    settlement_date: str = Field(alias="settlementDate")
    settlement_period_from: int = Field(alias="settlementPeriodFrom")
    settlement_period_to: int = Field(alias="settlementPeriodTo")
    time_from: datetime = Field(alias="timeFrom")
    time_to: datetime = Field(alias="timeTo")
    level_from: int = Field(alias="levelFrom")
    level_to: int = Field(alias="levelTo")
    national_grid_bm_unit: str = Field(alias="nationalGridBmUnit")
    so_flag: bool = Field(alias="soFlag", default=False)
    deemed_bo_flag: bool = Field(alias="deemedBoFlag", default=False)
    stor_flag: bool = Field(alias="storFlag", default=False)
    rr_flag: bool = Field(alias="rrFlag", default=False)


class BOD(BaseModel):
    """BOD (Bid Offer Data) - Balancing Mechanism Bid/Offer Data."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    bmu_id: str = Field(alias="bmUnit")
    bid_price: float = Field(alias="bidPrice")
    bid_volume: float = Field(alias="bidVolume")
    offer_price: float = Field(alias="offerPrice")
    offer_volume: float = Field(alias="offerVolume")
    time_from: datetime = Field(alias="timeFrom")
    time_to: datetime = Field(alias="timeTo")
    amendment_flag: bool = Field(alias="amendmentFlag", default=False)
    national_grid_bm_unit: Optional[str] = Field(alias="nationalGridBmUnit", default=None)


class PN(BaseModel):
    """PN (Physical Notification) - Physical notification data."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    bmu_id: str = Field(alias="bmUnit")
    level_from: float = Field(alias="levelFrom")
    level_to: float = Field(alias="levelTo")
    notification_type: str = Field(alias="notificationType")
    settlement_date: str = Field(alias="settlementDate")
    settlement_period: int = Field(alias="settlementPeriod")
    national_grid_bm_unit: Optional[str] = Field(alias="nationalGridBmUnit", default=None)


class B1610(BaseModel):
    """B1610 - Actual generation output data."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    bmu_id: str = Field(alias="bmUnit")
    actual_generation: float = Field(alias="actualGeneration")
    settlement_date: str = Field(alias="settlementDate")
    settlement_period: int = Field(alias="settlementPeriod")
    national_grid_bm_unit: Optional[str] = Field(alias="nationalGridBmUnit", default=None)


class SettlementStackPair(BaseModel):
    """Settlement stack pair for bid/offer data."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    bmu_id: str = Field(alias="id")
    volume: float
    price: float
    so_flag: bool = Field(alias="soFlag", default=False)
    transmission_loss_multiplier: Optional[float] = Field(alias="transmissionLossMultiplier", default=None)
    acceptance_number: Optional[int] = Field(alias="acceptanceNumber", default=None)


class AcceptedVolumes(BaseModel):
    """Container for accepted volumes data."""
    model_config = ConfigDict(extra='allow')
    
    bmu_id: str
    settlement_date: str
    settlement_period: int
    bid_volume: float
    offer_volume: float
    net_volume: float
    num_bid_pairs: int
    num_offer_pairs: int
    bid_pairs: List[SettlementStackPair] = Field(default_factory=list)
    offer_pairs: List[SettlementStackPair] = Field(default_factory=list)


# Response types for BOALF endpoints
class BOALFResponse(TypedAPIResponse[BOALF]):
    """Typed response for BOALF endpoints."""
    pass


class BODResponse(TypedAPIResponse[BOD]):
    """Typed response for BOD endpoints."""
    pass


class PNResponse(TypedAPIResponse[PN]):
    """Typed response for PN endpoints."""
    pass


class B1610Response(TypedAPIResponse[B1610]):
    """Typed response for B1610 endpoints."""
    pass

