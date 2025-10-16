"""
Pydantic models for endpoints that have empty schemas in the OpenAPI spec.

These models are manually created based on actual API responses to provide
type safety for the 12 "untyped" endpoints.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


# ==================== Health Endpoint ====================

class HealthCheckEntry(BaseModel):
    """Health check entry."""
    model_config = ConfigDict(extra='allow')
    
    # Structure varies, allow flexible format
    pass


class HealthCheckResponse(BaseModel):
    """Response from /health endpoint."""
    model_config = ConfigDict(extra='allow')
    
    status: str
    total_duration: Optional[str] = Field(alias="totalDuration", default=None)
    entries: Optional[Dict[str, Any]] = None


# ==================== CDN Endpoint ====================

class CreditDefaultNotice(BaseModel):
    """Credit default notice data."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    participant_id: str = Field(alias="participantId")
    participant_name: str = Field(alias="participantName")
    credit_default_level: int = Field(alias="creditDefaultLevel")
    entered_default_settlement_date: str = Field(alias="enteredDefaultSettlementDate")
    entered_default_settlement_period: int = Field(alias="enteredDefaultSettlementPeriod")
    cleared_default_settlement_date: Optional[str] = Field(alias="clearedDefaultSettlementDate", default=None)
    cleared_default_settlement_period: Optional[int] = Field(alias="clearedDefaultSettlementPeriod", default=None)
    cleared_default_text: Optional[str] = Field(alias="clearedDefaultText", default=None)


class CDNResponse(BaseModel):
    """Response from /CDN endpoint."""
    model_config = ConfigDict(extra='allow')
    
    data: List[CreditDefaultNotice]


# ==================== Demand Endpoint ====================

class InitialDemandOutturn(BaseModel):
    """Initial demand outturn data."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    publish_time: datetime = Field(alias="publishTime")
    start_time: datetime = Field(alias="startTime")
    settlement_date: str = Field(alias="settlementDate")
    settlement_period: int = Field(alias="settlementPeriod")
    initial_demand_outturn: int = Field(alias="initialDemandOutturn")
    initial_transmission_system_demand_outturn: int = Field(alias="initialTransmissionSystemDemandOutturn")


class DemandResponse(BaseModel):
    """Response from /demand endpoint."""
    model_config = ConfigDict(extra='allow')
    
    data: List[InitialDemandOutturn]
    metadata: Optional[Dict[str, Any]] = None


# ==================== Demand Summary ====================

class DemandSummaryItem(BaseModel):
    """Demand summary item."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    record_type: str = Field(alias="recordType")
    start_time: datetime = Field(alias="startTime")
    demand: int


# DemandSummaryResponse is just List[DemandSummaryItem]


# ==================== Rolling System Demand ====================

class RollingSystemDemandItem(BaseModel):
    """Rolling system demand item."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    record_type: str = Field(alias="recordType")
    start_time: datetime = Field(alias="startTime")
    demand: int


class RollingSystemDemandResponse(BaseModel):
    """Response from /demand/rollingSystemDemand endpoint."""
    model_config = ConfigDict(extra='allow')
    
    data: List[RollingSystemDemandItem]
    metadata: Optional[Dict[str, Any]] = None


# ==================== Demand Total Actual ====================

class DemandTotalActualItem(BaseModel):
    """Demand total actual item."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    publish_time: datetime = Field(alias="publishTime")
    start_time: datetime = Field(alias="startTime")
    settlement_date: str = Field(alias="settlementDate")
    settlement_period: int = Field(alias="settlementPeriod")
    quantity: float


class DemandTotalActualResponse(BaseModel):
    """Response from /demand/total/actual endpoint."""
    model_config = ConfigDict(extra='allow')
    
    data: List[DemandTotalActualItem]
    metadata: Optional[Dict[str, Any]] = None


# ==================== Generation Current ====================

class GenerationCurrentItem(BaseModel):
    """Generation outturn current (FUELINSTHHCUR) item."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    dataset: str
    fuel_type: str = Field(alias="fuelType")
    current_usage: Optional[int] = Field(alias="currentUsage", default=None)
    current_percentage: Optional[float] = Field(alias="currentPercentage", default=None)
    half_hour_usage: Optional[int] = Field(alias="halfHourUsage", default=None)
    half_hour_percentage: Optional[float] = Field(alias="halfHourPercentage", default=None)
    twenty_four_hour_usage: Optional[int] = Field(alias="twentyFourHourUsage", default=None)
    twenty_four_hour_percentage: Optional[float] = Field(alias="twentyFourHourPercentage", default=None)


# GenerationCurrentResponse is just List[GenerationCurrentItem]


# ==================== Half Hourly Interconnector ====================

class HalfHourlyInterconnectorItem(BaseModel):
    """Half-hourly interconnector generation item."""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    
    dataset: str
    publish_time: datetime = Field(alias="publishTime")
    start_time: datetime = Field(alias="startTime")
    settlement_date: str = Field(alias="settlementDate")
    settlement_date_timezone: str = Field(alias="settlementDateTimezone")
    settlement_period: int = Field(alias="settlementPeriod")
    interconnector_name: str = Field(alias="interconnectorName")
    generation: int


class HalfHourlyInterconnectorResponse(BaseModel):
    """Response from /generation/outturn/halfHourlyInterconnector endpoint."""
    model_config = ConfigDict(extra='allow')
    
    data: List[HalfHourlyInterconnectorItem]
    metadata: Optional[Dict[str, Any]] = None


# ==================== Interop Endpoints ====================
# These would need actual parameters to test - skipping for now as they're legacy


# ==================== Export All ====================

__all__ = [
    'HealthCheckResponse',
    'HealthCheckEntry',
    'CreditDefaultNotice',
    'CDNResponse',
    'InitialDemandOutturn',  # Also used for /demand/stream
    'DemandResponse',
    'DemandSummaryItem',
    'RollingSystemDemandItem',
    'RollingSystemDemandResponse',
    'DemandTotalActualItem',
    'DemandTotalActualResponse',
    'GenerationCurrentItem',
    'HalfHourlyInterconnectorItem',
    'HalfHourlyInterconnectorResponse',
]

