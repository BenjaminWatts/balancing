"""
Field mixins for Pydantic models to avoid repetition.

These mixins provide common fields that appear across multiple BMRS API response models.
Each mixin class defines a set of related fields with proper types and aliases.

Usage in Pydantic V2:
    class MyModel(DatasetFields, SettlementFields, BaseModel):
        # Model will inherit dataset, settlementDate, and settlementPeriod fields
        other_field: str
"""

from datetime import datetime
from typing import Optional
from pydantic import Field, ConfigDict


class DatasetFields:
    """Dataset identifier field (80 schemas)."""
    dataset: Optional[str] = None


class PublishTimeFields:
    """Publish time field (86 schemas)."""
    publish_time: datetime = Field(alias="publishTime")


class SettlementFields:
    """Settlement date and period fields (71 schemas)."""
    settlement_date: str = Field(alias="settlementDate")
    settlement_period: int = Field(alias="settlementPeriod")


class StartTimeFields:
    """Start time field (56 schemas)."""
    start_time: datetime = Field(alias="startTime")


class TimeRangeFields:
    """Time range fields (10 schemas)."""
    time_from: datetime = Field(alias="timeFrom")
    time_to: datetime = Field(alias="timeTo")


class StartEndTimeFields:
    """Start and end time fields (2 schemas)."""
    start_time: datetime = Field(alias="startTime")
    end_time: Optional[datetime] = Field(alias="endTime", default=None)


class BmUnitFields:
    """BMU identifier fields (22 schemas)."""
    bmu_id: str = Field(alias="bmUnit")
    national_grid_bm_unit: Optional[str] = Field(alias="nationalGridBmUnit", default=None)


class LevelFields:
    """Level from/to fields (7 schemas)."""
    level_from: int = Field(alias="levelFrom")
    level_to: int = Field(alias="levelTo")


class QuantityFields:
    """Quantity field (20 schemas)."""
    quantity: float = Field(alias="quantity")


class DocumentFields:
    """Document ID and revision fields (19 schemas)."""
    document_id: str = Field(alias="documentId")
    document_revision_number: int = Field(alias="documentRevisionNumber")


class YearFields:
    """Year field (14 schemas)."""
    year: int = Field(alias="year")


class ForecastDateFields:
    """Forecast date field (13 schemas)."""
    forecast_date: str = Field(alias="forecastDate")


class DemandFields:
    """Demand field (13 schemas)."""
    demand: float = Field(alias="demand")


class PsrTypeFields:
    """Power System Resource type field (13 schemas)."""
    psr_type: str = Field(alias="psrType")


class FuelTypeFields:
    """Fuel type field (12 schemas)."""
    fuel_type: str = Field(alias="fuelType")


class BoundaryFields:
    """Boundary field (10 schemas)."""
    boundary: str = Field(alias="boundary")


class BusinessTypeFields:
    """Business type field (10 schemas)."""
    business_type: str = Field(alias="businessType")


class GenerationFields:
    """Generation field (9 schemas)."""
    generation: int = Field(alias="generation")


class VolumeFields:
    """Volume field (8 schemas)."""
    volume: float = Field(alias="volume")


class OutputUsableFields:
    """Output usable field (8 schemas)."""
    output_usable: int = Field(alias="outputUsable")


class RevisionNumberFields:
    """Revision number field (7 schemas)."""
    revision_number: int = Field(alias="revisionNumber")


class WeekFields:
    """Week field (7 schemas)."""
    week: int = Field(alias="week")


class AssetFields:
    """Asset ID field (6 schemas)."""
    asset_id: str = Field(alias="assetId")


class CreatedDateTimeFields:
    """Created datetime field (6 schemas)."""
    created_date_time: datetime = Field(alias="createdDateTime")


class FlowDirectionFields:
    """Flow direction field (6 schemas)."""
    flow_direction: str = Field(alias="flowDirection")


class MessageTypeFields:
    """Message type field (5 schemas)."""
    message_type: str = Field(alias="messageType")


class BiddingZoneFields:
    """Bidding zone field (5 schemas)."""
    bidding_zone: str = Field(alias="biddingZone")


class IdFields:
    """Generic ID field (5 schemas)."""
    id: str = Field(alias="id")


class TransmissionDemandFields:
    """Transmission system demand field (5 schemas)."""
    transmission_system_demand: int = Field(alias="transmissionSystemDemand")


class MarginFields:
    """Margin field (5 schemas)."""
    margin: int = Field(alias="margin")


class SoFlagFields:
    """System Operator flag field (5 schemas)."""
    so_flag: bool = Field(alias="soFlag", default=False)


class StorFlagFields:
    """STOR flag field (4 schemas)."""
    stor_flag: bool = Field(alias="storFlag", default=False)


class BmUnitTypeFields:
    """BMU type field (4 schemas)."""
    bm_unit_type: str = Field(alias="bmUnitType")


class LeadPartyFields:
    """Lead party name field (4 schemas)."""
    lead_party_name: str = Field(alias="leadPartyName")


class NationalDemandFields:
    """National demand field (4 schemas)."""
    national_demand: int = Field(alias="nationalDemand")


class SurplusFields:
    """Surplus field (4 schemas)."""
    surplus: int = Field(alias="surplus")


class SystemZoneFields:
    """System zone field (4 schemas)."""
    system_zone: str = Field(alias="systemZone")


class InterconnectorFields:
    """Interconnector name field (4 schemas)."""
    interconnector_name: str = Field(alias="interconnectorName")


class CapacityFields:
    """Capacity fields (4 schemas)."""
    minimum_possible: float = Field(alias="minimumPossible")
    maximum_available: float = Field(alias="maximumAvailable")


# Additional common field combinations
class SettlementPeriodRangeFields:
    """Settlement period range fields."""
    settlement_period_from: int = Field(alias="settlementPeriodFrom")
    settlement_period_to: int = Field(alias="settlementPeriodTo")


class AcceptanceFields:
    """Acceptance-related fields."""
    acceptance_number: int = Field(alias="acceptanceNumber")
    acceptance_time: datetime = Field(alias="acceptanceTime")


class BidOfferPriceFields:
    """Bid and offer price fields."""
    bid_price: float = Field(alias="bidPrice")
    offer_price: float = Field(alias="offerPrice")


class BidOfferVolumeFields:
    """Bid and offer volume fields."""
    bid_volume: float = Field(alias="bidVolume")
    offer_volume: float = Field(alias="offerVolume")


class BidOfferFields(BidOfferPriceFields, BidOfferVolumeFields):
    """Complete bid-offer data fields (combines price and volume)."""
    pass


class AmendmentFlagFields:
    """Amendment flag field."""
    amendment_flag: bool = Field(alias="amendmentFlag", default=False)


class ActiveFlagFields:
    """Active flag field."""
    active_flag: bool = Field(alias="activeFlag", default=True)


class TimeFields:
    """Generic time field."""
    time: datetime = Field(alias="time")


# Export all mixins
__all__ = [
    'DatasetFields',
    'PublishTimeFields',
    'SettlementFields',
    'StartTimeFields',
    'TimeRangeFields',
    'StartEndTimeFields',
    'BmUnitFields',
    'LevelFields',
    'QuantityFields',
    'DocumentFields',
    'YearFields',
    'ForecastDateFields',
    'DemandFields',
    'PsrTypeFields',
    'FuelTypeFields',
    'BoundaryFields',
    'BusinessTypeFields',
    'GenerationFields',
    'VolumeFields',
    'OutputUsableFields',
    'RevisionNumberFields',
    'WeekFields',
    'AssetFields',
    'CreatedDateTimeFields',
    'FlowDirectionFields',
    'MessageTypeFields',
    'BiddingZoneFields',
    'IdFields',
    'TransmissionDemandFields',
    'MarginFields',
    'SoFlagFields',
    'StorFlagFields',
    'BmUnitTypeFields',
    'LeadPartyFields',
    'NationalDemandFields',
    'SurplusFields',
    'SystemZoneFields',
    'InterconnectorFields',
    'CapacityFields',
    'SettlementPeriodRangeFields',
    'AcceptanceFields',
    'BidOfferPriceFields',
    'BidOfferVolumeFields',
    'BidOfferFields',
    'AmendmentFlagFields',
    'ActiveFlagFields',
    'TimeFields',
]
