"""
Field mixins that provide common field definitions.

Pydantic V2 supports field inheritance from mixins.
These mixins provide both field definitions AND helper methods,
eliminating massive code duplication.
"""

from datetime import date, datetime
from typing import Optional
from pydantic import Field, field_validator, model_validator


class SettlementFields:
    """
    Provides settlement_date and settlement_period fields with validation.
    Used in: 73 models
    """
    settlement_date: date = Field(alias="settlementDate")
    settlement_period: int = Field(alias="settlementPeriod")
    
    @field_validator('settlement_period')
    @classmethod
    def validate_settlement_period(cls, v: int) -> int:
        """Validate settlement period is in valid range (1-50)."""
        if v < 1 or v > 50:
            raise ValueError(
                f"Settlement period must be between 1 and 50, got {v}. "
                f"Normal days: 1-48, Short days: 1-46, Long days: 1-50"
            )
        return v


class PublishTimeFields:
    """
    Provides publish_time field.
    Used in: 88 models
    """
    publish_time: datetime = Field(alias="publishTime")
    
    def is_recent(self, hours: int = 24) -> bool:
        """Check if published within the last N hours."""
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)
        return (now - self.publish_time) <= timedelta(hours=hours)


class StartTimeFields:
    """
    Provides start_time field.
    Used in: 58 models
    """
    start_time: datetime = Field(alias="startTime")
    
    def get_start_date(self) -> date:
        """Get the start date (date part of start_time)."""
        return self.start_time.date()


class TimeRangeFields:
    """
    Provides time_from and time_to fields with validation.
    Used in: 12 models
    """
    time_from: datetime = Field(alias="timeFrom")
    time_to: datetime = Field(alias="timeTo")
    
    @model_validator(mode='after')
    def validate_time_range(self):
        """Validate that time_to is after time_from."""
        if self.time_to < self.time_from:
            raise ValueError(
                f"time_to ({self.time_to}) must be after time_from ({self.time_from})"
            )
        return self


class LevelRangeFields:
    """
    Provides level_from and level_to fields with validation.
    Used in: 9 models
    """
    level_from: Optional[int] = Field(default=None, alias="levelFrom")
    level_to: Optional[int] = Field(default=None, alias="levelTo")
    
    @model_validator(mode='after')
    def validate_level_range(self):
        """Validate that level_to is >= level_from."""
        if self.level_from is not None and self.level_to is not None:
            if self.level_to < self.level_from:
                raise ValueError(
                    f"level_to ({self.level_to}) must be >= level_from ({self.level_from})"
                )
        return self


class BmUnitFields:
    """
    Provides bm_unit and national_grid_bm_unit fields.
    Used in: 29 models
    """
    bm_unit: str = Field(alias="bmUnit")
    national_grid_bm_unit: str = Field(alias="nationalGridBmUnit")
    
    def get_bm_unit(self) -> str:
        """Get the BM Unit identifier."""
        return self.bm_unit
    
    def is_transmission_unit(self) -> bool:
        """Check if this is a transmission BM Unit (starts with 'T_')."""
        return self.bm_unit.startswith('T_')
    
    def is_interconnector(self) -> bool:
        """Check if this is an interconnector unit (starts with 'I_')."""
        return self.bm_unit.startswith('I_')


class DocumentFields:
    """
    Provides document_id and document_revision_number fields.
    Used in: 21 models
    """
    document_id: str = Field(alias="documentId")
    document_revision_number: int = Field(alias="documentRevisionNumber")
    
    def get_document_identifier(self) -> str:
        """Get full document identifier (ID + revision)."""
        return f"{self.document_id}_v{self.document_revision_number}"


class DatasetFields:
    """
    Provides dataset field.
    Used in: 82 models
    """
    # Note: DatasetEnum will be imported in generated_models.py
    # We use string annotation to avoid circular import
    dataset: 'DatasetEnum' = Field()
    
    def get_dataset_name(self) -> str:
        """Get the dataset name as string."""
        return self.dataset.value if hasattr(self.dataset, 'value') else str(self.dataset)


class QuantityFields:
    """
    Provides quantity field.
    Used in: 22 models
    """
    quantity: float = Field()
    
    def get_quantity_mw(self) -> float:
        """Get quantity in MW."""
        return self.quantity
    
    def get_quantity_gwh(self) -> float:
        """Get quantity in GWh (assuming half-hour period)."""
        return self.quantity * 0.5 / 1000


class PriceFields:
    """
    Provides price field.
    Used in: 5 models
    """
    price: float = Field()
    
    def get_price_per_mwh(self) -> float:
        """Get price in £/MWh."""
        return self.price
    
    def get_price_per_kwh(self) -> float:
        """Get price in £/kWh."""
        return self.price / 1000


class VolumeFields:
    """
    Provides volume field.
    Used in: 10 models
    """
    volume: float = Field()
    
    def get_volume_mwh(self) -> float:
        """Get volume in MWh."""
        return self.volume
    
    def get_volume_gwh(self) -> float:
        """Get volume in GWh."""
        return self.volume / 1000


class DemandFields:
    """
    Provides demand field.
    Used in: 15 models
    """
    demand: int = Field()
    
    def get_demand_mw(self) -> int:
        """Get demand in MW."""
        return self.demand
    
    def get_demand_gw(self) -> float:
        """Get demand in GW."""
        return self.demand / 1000


class GenerationFields:
    """
    Provides generation field.
    Used in: 11 models
    """
    generation: int = Field()
    
    def get_generation_mw(self) -> int:
        """Get generation in MW."""
        return self.generation
    
    def get_generation_gw(self) -> float:
        """Get generation in GW."""
        return self.generation / 1000


class YearFields:
    """Provides year field. Used in: 16 models"""
    year: int = Field()


class WeekFields:
    """Provides week field. Used in: 9 models"""
    week: int = Field()


class ForecastDateFields:
    """Provides forecast_date field. Used in: 15 models"""
    forecast_date: date = Field(alias="forecastDate")


class BoundaryFields:
    """Provides boundary field. Used in: 12 models"""
    from elexon_bmrs.enums import BoundaryEnum
    boundary: 'BoundaryEnum' = Field()


class CreatedDateTimeFields:
    """Provides created_date_time field. Used in: 8 models"""
    created_date_time: datetime = Field(alias="createdDateTime")
    
    def get_age_hours(self) -> float:
        """Get age in hours since creation."""
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        delta = now - self.created_date_time
        return delta.total_seconds() / 3600
