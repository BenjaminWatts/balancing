"""
Validators and mixins for BMRS API models.

This module provides validation logic and reusable mixins for common field patterns
in BMRS API responses.

Mixins are applied automatically based on which fields are present in a model:
- PublishTimeMixin: Models with publish_time field (86 models)
- SettlementPeriodMixin: Models with settlement_date + settlement_period (71 models)
- StartTimeMixin: Models with start_time field (56 models)
- TimeRangeMixin: Models with time_from + time_to (10+ models)
- LevelRangeMixin: Models with level_from + level_to (10+ models)
- BmUnitMixin: Models with bm_unit/national_grid_bm_unit (22+ models)
- DocumentMixin: Models with document_id + document_revision_number (19 models)
- FlowDirectionMixin: Models with flow_direction (6+ models)
- QuantityMixin: Models with quantity (80+ models)
- PriceMixin: Models with price (50+ models)
- FuelTypeMixin: Models with fuel_type (12 models)
- PsrTypeMixin: Models with psr_type (13 models)
- BusinessTypeMixin: Models with business_type (10 models)
"""

from datetime import date, datetime, time
from typing import Optional
from pydantic import field_validator, model_validator, ConfigDict


class SettlementPeriodMixin:
    """
    Mixin for models with settlement date and period fields.
    
    Provides validation for:
    - Settlement period range (1-50 for normal days, 1-46 for short days, 1-50 for long days)
    - Settlement date and period consistency
    """
    
    @field_validator('settlement_period')
    @classmethod
    def validate_settlement_period(cls, v: Optional[int]) -> Optional[int]:
        """
        Validate settlement period is in valid range.
        
        UK has 48 half-hour periods normally (1-48), but:
        - Short days (clock forward): 46 periods (1-46)
        - Long days (clock back): 50 periods (1-50)
        
        We allow 1-50 to cover all cases.
        """
        if v is not None:
            if v < 1 or v > 50:
                raise ValueError(
                    f"Settlement period must be between 1 and 50, got {v}. "
                    f"Normal days: 1-48, Short days: 1-46, Long days: 1-50"
                )
        return v
    
    @model_validator(mode='after')
    def validate_settlement_consistency(self):
        """
        Validate settlement date and period are consistent.
        
        Checks for known short/long days in the UK (clock changes).
        """
        if not hasattr(self, 'settlement_date') or not hasattr(self, 'settlement_period'):
            return self
            
        settlement_date = getattr(self, 'settlement_date', None)
        settlement_period = getattr(self, 'settlement_period', None)
        
        if settlement_date and settlement_period:
            # Check if this is a known short/long day
            # UK clock changes typically last Sunday of March (short) and October (long)
            if isinstance(settlement_date, date):
                # Short day (spring forward): max 46 periods
                if self._is_short_day(settlement_date) and settlement_period > 46:
                    raise ValueError(
                        f"Settlement period {settlement_period} is invalid for short day "
                        f"{settlement_date}. Maximum is 46 periods."
                    )
                # Long day (fall back): up to 50 periods
                elif self._is_long_day(settlement_date) and settlement_period > 50:
                    raise ValueError(
                        f"Settlement period {settlement_period} is invalid for long day "
                        f"{settlement_date}. Maximum is 50 periods."
                    )
                # Normal day: max 48 periods
                elif not self._is_short_day(settlement_date) and not self._is_long_day(settlement_date):
                    if settlement_period > 48:
                        raise ValueError(
                            f"Settlement period {settlement_period} is invalid for normal day "
                            f"{settlement_date}. Maximum is 48 periods."
                        )
        
        return self
    
    @staticmethod
    def _is_short_day(d: date) -> bool:
        """Check if date is a short day (spring clock change)."""
        # UK spring clock change is last Sunday of March
        # This is a simplified check - in production you'd want a more robust solution
        if d.month == 3 and d.weekday() == 6:  # Sunday in March
            # Check if it's the last Sunday
            next_week = date(d.year, d.month, d.day + 7)
            if next_week.month != 3:
                return True
        return False
    
    @staticmethod
    def _is_long_day(d: date) -> bool:
        """Check if date is a long day (autumn clock change)."""
        # UK autumn clock change is last Sunday of October
        if d.month == 10 and d.weekday() == 6:  # Sunday in October
            # Check if it's the last Sunday
            next_week = date(d.year, d.month, d.day + 7)
            if next_week.month != 10:
                return True
        return False


class TimeRangeMixin:
    """
    Mixin for models with time_from and time_to fields.
    
    Provides validation that time_to is after time_from.
    """
    
    @model_validator(mode='after')
    def validate_time_range(self):
        """Validate that time_to is after time_from."""
        if not hasattr(self, 'time_from') or not hasattr(self, 'time_to'):
            return self
            
        time_from = getattr(self, 'time_from', None)
        time_to = getattr(self, 'time_to', None)
        
        if time_from and time_to:
            if isinstance(time_from, datetime) and isinstance(time_to, datetime):
                if time_to < time_from:
                    raise ValueError(
                        f"time_to ({time_to}) must be after time_from ({time_from})"
                    )
        
        return self


class LevelRangeMixin:
    """
    Mixin for models with level_from and level_to fields.
    
    Provides validation that level_to is >= level_from.
    """
    
    @model_validator(mode='after')
    def validate_level_range(self):
        """Validate that level_to is >= level_from."""
        if not hasattr(self, 'level_from') or not hasattr(self, 'level_to'):
            return self
            
        level_from = getattr(self, 'level_from', None)
        level_to = getattr(self, 'level_to', None)
        
        if level_from is not None and level_to is not None:
            if level_to < level_from:
                raise ValueError(
                    f"level_to ({level_to}) must be >= level_from ({level_from})"
                )
        
        return self


class FlowDirectionMixin:
    """
    Mixin for models with flow_direction field.
    
    Provides validation and helper methods for flow direction.
    """
    
    @field_validator('flow_direction')
    @classmethod
    def validate_flow_direction(cls, v: Optional[str]) -> Optional[str]:
        """Validate flow direction is 'Up' or 'Down'."""
        if v is not None:
            if v not in ['Up', 'Down']:
                raise ValueError(
                    f"flow_direction must be 'Up' or 'Down', got '{v}'"
                )
        return v
    
    def is_upward_flow(self) -> bool:
        """Check if flow direction is upward."""
        return getattr(self, 'flow_direction', None) == 'Up'
    
    def is_downward_flow(self) -> bool:
        """Check if flow direction is downward."""
        return getattr(self, 'flow_direction', None) == 'Down'


class BmUnitMixin:
    """
    Mixin for models with BM Unit fields.
    
    Provides helper methods for BM Unit handling.
    """
    
    def get_bm_unit(self) -> Optional[str]:
        """Get the BM Unit identifier (prefers bmUnit over nationalGridBmUnit)."""
        return getattr(self, 'bm_unit', None) or getattr(self, 'national_grid_bm_unit', None)
    
    def is_transmission_unit(self) -> bool:
        """Check if this is a transmission BM Unit (starts with 'T_')."""
        bm_unit = self.get_bm_unit()
        return bm_unit.startswith('T_') if bm_unit else False
    
    def is_interconnector(self) -> bool:
        """Check if this is an interconnector unit (starts with 'I_')."""
        bm_unit = self.get_bm_unit()
        return bm_unit.startswith('I_') if bm_unit else False


class QuantityMixin:
    """
    Mixin for models with quantity fields.
    
    Provides helper methods for quantity handling.
    """
    
    def get_quantity_mw(self) -> Optional[float]:
        """Get quantity in MW."""
        return getattr(self, 'quantity', None)
    
    def get_quantity_gwh(self) -> Optional[float]:
        """Get quantity in GWh (assuming quantity is in MW and for half-hour period)."""
        quantity = self.get_quantity_mw()
        if quantity is not None:
            # Convert MW to GWh for half-hour period: MW * 0.5 / 1000
            return quantity * 0.5 / 1000
        return None


class PriceMixin:
    """
    Mixin for models with price fields.
    
    Provides helper methods for price handling.
    """
    
    def get_price_per_mwh(self) -> Optional[float]:
        """Get price in £/MWh."""
        return getattr(self, 'price', None)
    
    def get_price_per_kwh(self) -> Optional[float]:
        """Get price in £/kWh."""
        price = self.get_price_per_mwh()
        if price is not None:
            return price / 1000
        return None


# Validator functions for use in models
def validate_positive(v: Optional[float]) -> Optional[float]:
    """Validate that a value is positive."""
    if v is not None and v < 0:
        raise ValueError(f"Value must be positive, got {v}")
    return v


def validate_percentage(v: Optional[float]) -> Optional[float]:
    """Validate that a value is a valid percentage (0-100)."""
    if v is not None:
        if v < 0 or v > 100:
            raise ValueError(f"Percentage must be between 0 and 100, got {v}")
    return v


def validate_frequency(v: Optional[float]) -> Optional[float]:
    """Validate that a frequency is in valid range (typically 49.5-50.5 Hz for UK)."""
    if v is not None:
        if v < 47 or v > 53:  # Allow some margin for extreme events
            raise ValueError(
                f"Frequency must be between 47 and 53 Hz, got {v}. "
                f"Normal UK frequency is 50 Hz ± 0.5 Hz"
            )
    return v


class PublishTimeMixin:
    """
    Mixin for models with publish_time field.
    
    Provides helper methods for publish time handling.
    Used in: 86 models
    """
    
    def get_publish_time(self) -> Optional[datetime]:
        """Get the publish time."""
        return getattr(self, 'publish_time', None)
    
    def is_recent(self, hours: int = 24) -> bool:
        """Check if published within the last N hours."""
        publish_time = self.get_publish_time()
        if publish_time:
            from datetime import datetime, timedelta, timezone
            now = datetime.now(timezone.utc)
            return (now - publish_time) <= timedelta(hours=hours)
        return False


class StartTimeMixin:
    """
    Mixin for models with start_time field.
    
    Provides helper methods for start time handling.
    Used in: 56 models
    """
    
    def get_start_time(self) -> Optional[datetime]:
        """Get the start time."""
        return getattr(self, 'start_time', None)
    
    def get_start_date(self) -> Optional[date]:
        """Get the start date (date part of start_time)."""
        start_time = self.get_start_time()
        return start_time.date() if start_time else None


class DocumentMixin:
    """
    Mixin for models with document_id and document_revision_number fields.
    
    Provides helper methods for document handling.
    Used in: 19 models
    """
    
    def get_document_id(self) -> Optional[str]:
        """Get the document ID."""
        return getattr(self, 'document_id', None)
    
    def get_document_revision(self) -> Optional[int]:
        """Get the document revision number."""
        return getattr(self, 'document_revision_number', None)
    
    def get_document_identifier(self) -> str:
        """Get full document identifier (ID + revision)."""
        doc_id = self.get_document_id() or "UNKNOWN"
        revision = self.get_document_revision() or 0
        return f"{doc_id}_v{revision}"


class FuelTypeMixin:
    """
    Mixin for models with fuel_type field.
    
    Provides helper methods for fuel type classification.
    Used in: 12 models
    """
    
    def get_fuel_type(self) -> Optional[str]:
        """Get the fuel type."""
        return getattr(self, 'fuel_type', None)
    
    def is_renewable(self) -> bool:
        """Check if fuel type is renewable."""
        fuel = self.get_fuel_type()
        if fuel:
            renewable_types = ['WIND', 'SOLAR', 'HYDRO', 'BIOMASS', 'MARINE', 
                             'Wind Onshore', 'Wind Offshore', 'Solar', 
                             'Hydro Pumped Storage', 'Hydro Run-of-river and poundage']
            return str(fuel) in renewable_types or any(r in str(fuel) for r in ['Wind', 'Solar', 'Hydro'])
        return False
    
    def is_fossil(self) -> bool:
        """Check if fuel type is fossil fuel."""
        fuel = self.get_fuel_type()
        if fuel:
            fossil_types = ['CCGT', 'COAL', 'GAS', 'OIL', 'OCGT',
                          'Fossil Gas', 'Fossil Hard coal', 'Fossil Oil']
            return str(fuel) in fossil_types or 'Fossil' in str(fuel)
        return False
    
    def is_nuclear(self) -> bool:
        """Check if fuel type is nuclear."""
        fuel = self.get_fuel_type()
        return str(fuel) in ['NUCLEAR', 'Nuclear'] if fuel else False


class PsrTypeMixin:
    """
    Mixin for models with psr_type field.
    
    Provides helper methods for PSR type classification.
    Used in: 13 models
    """
    
    def get_psr_type(self) -> Optional[str]:
        """Get the PSR type."""
        return getattr(self, 'psr_type', None)
    
    def is_generation_type(self) -> bool:
        """Check if PSR type is generation."""
        psr = self.get_psr_type()
        return str(psr) == 'Generation' if psr else False
    
    def is_renewable_psr(self) -> bool:
        """Check if PSR type is renewable."""
        psr = self.get_psr_type()
        if psr:
            renewable = ['Solar', 'Wind Onshore', 'Wind Offshore', 
                        'Hydro Pumped Storage', 'Hydro Run-of-river and poundage',
                        'Marine']
            return str(psr) in renewable
        return False


class BusinessTypeMixin:
    """
    Mixin for models with business_type field.
    
    Provides helper methods for business type classification.
    Used in: 10 models
    """
    
    def get_business_type(self) -> Optional[str]:
        """Get the business type."""
        return getattr(self, 'business_type', None)
    
    def is_generation_business(self) -> bool:
        """Check if business type is generation-related."""
        btype = self.get_business_type()
        if btype:
            return 'generation' in str(btype).lower()
        return False


class DatasetMixin:
    """
    Mixin for models with dataset field.
    
    Provides helper methods for dataset identification.
    Used in: Many models
    """
    
    def get_dataset(self) -> Optional[str]:
        """Get the dataset identifier."""
        return getattr(self, 'dataset', None)
    
    def get_dataset_name(self) -> str:
        """Get the dataset name as string."""
        dataset = self.get_dataset()
        return str(dataset.value) if hasattr(dataset, 'value') else str(dataset) if dataset else "UNKNOWN"


class CreatedDateTimeMixin:
    """
    Mixin for models with created_date_time field.
    
    Provides helper methods for creation time handling.
    Used in: 6 models
    """
    
    def get_created_time(self) -> Optional[datetime]:
        """Get the creation time."""
        return getattr(self, 'created_date_time', None)
    
    def get_age_hours(self) -> Optional[float]:
        """Get age in hours since creation."""
        created = self.get_created_time()
        if created:
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc)
            delta = now - created
            return delta.total_seconds() / 3600
        return None


class RevisionMixin:
    """
    Mixin for models with revision_number field.
    
    Provides helper methods for revision handling.
    Used in: 7 models
    """
    
    def get_revision_number(self) -> Optional[int]:
        """Get the revision number."""
        return getattr(self, 'revision_number', None)
    
    def is_original(self) -> bool:
        """Check if this is the original version (revision 1)."""
        revision = self.get_revision_number()
        return revision == 1 if revision is not None else False
    
    def is_revised(self) -> bool:
        """Check if this is a revised version (revision > 1)."""
        revision = self.get_revision_number()
        return revision > 1 if revision is not None else False


class AssetMixin:
    """
    Mixin for models with asset_id and optionally asset_type fields.
    
    Provides helper methods for asset identification.
    Used in: 6+ models
    """
    
    def get_asset_id(self) -> Optional[str]:
        """Get the asset ID."""
        return getattr(self, 'asset_id', None)
    
    def get_asset_type(self) -> Optional[str]:
        """Get the asset type."""
        return getattr(self, 'asset_type', None)


class MessageMixin:
    """
    Mixin for models with message_heading and message_type fields.
    
    Provides helper methods for message handling.
    Used in: 4 models
    """
    
    def get_message_heading(self) -> Optional[str]:
        """Get the message heading."""
        return getattr(self, 'message_heading', None)
    
    def get_message_type(self) -> Optional[str]:
        """Get the message type."""
        return getattr(self, 'message_type', None)
    
    def get_full_message(self) -> str:
        """Get full message identifier."""
        heading = self.get_message_heading() or "UNKNOWN"
        msg_type = self.get_message_type() or "UNKNOWN"
        return f"[{msg_type}] {heading}"


class EventMixin:
    """
    Mixin for models with event_type and event_status fields.
    
    Provides helper methods for event handling.
    Used in: 4 models
    """
    
    def get_event_type(self) -> Optional[str]:
        """Get the event type."""
        return getattr(self, 'event_type', None)
    
    def get_event_status(self) -> Optional[str]:
        """Get the event status."""
        return getattr(self, 'event_status', None)
    
    def is_active_event(self) -> bool:
        """Check if event is active."""
        status = self.get_event_status()
        return str(status) == 'Active' if status else False
    
    def is_completed_event(self) -> bool:
        """Check if event is completed."""
        status = self.get_event_status()
        return str(status) == 'Completed' if status else False


class EventTimeMixin:
    """
    Mixin for models with event_start_time and event_end_time fields.
    
    Provides helper methods and validation for event times.
    Used in: Multiple models
    """
    
    def get_event_start_time(self) -> Optional[datetime]:
        """Get the event start time."""
        return getattr(self, 'event_start_time', None)
    
    def get_event_end_time(self) -> Optional[datetime]:
        """Get the event end time."""
        return getattr(self, 'event_end_time', None)
    
    def get_event_duration_hours(self) -> Optional[float]:
        """Get event duration in hours."""
        start = self.get_event_start_time()
        end = self.get_event_end_time()
        if start and end:
            delta = end - start
            return delta.total_seconds() / 3600
        return None
    
    @model_validator(mode='after')
    def validate_event_time_range(self):
        """Validate that event_end_time is after event_start_time."""
        start = getattr(self, 'event_start_time', None)
        end = getattr(self, 'event_end_time', None)
        
        if start and end:
            if isinstance(start, datetime) and isinstance(end, datetime):
                if end < start:
                    raise ValueError(
                        f"event_end_time ({end}) must be after event_start_time ({start})"
                    )
        
        return self


class AffectedUnitMixin:
    """
    Mixin for models with affected_unit field.
    
    Provides helper methods for affected unit handling.
    Used in: 4 models
    """
    
    def get_affected_unit(self) -> Optional[str]:
        """Get the affected unit."""
        return getattr(self, 'affected_unit', None)


class ParticipantMixin:
    """
    Mixin for models with participant_id field.
    
    Provides helper methods for participant handling.
    Used in: 3+ models
    """
    
    def get_participant_id(self) -> Optional[str]:
        """Get the participant ID."""
        return getattr(self, 'participant_id', None)


class AcceptanceMixin:
    """
    Mixin for models with acceptance_number and optionally acceptance_time fields.
    
    Provides helper methods for acceptance handling.
    Used in: 3+ models
    """
    
    def get_acceptance_number(self) -> Optional[int]:
        """Get the acceptance number."""
        return getattr(self, 'acceptance_number', None)
    
    def get_acceptance_time(self) -> Optional[datetime]:
        """Get the acceptance time."""
        return getattr(self, 'acceptance_time', None)


class BidOfferMixin:
    """
    Mixin for models with bid and offer fields.
    
    Provides helper methods for bid/offer handling.
    Used in: Multiple models
    """
    
    def get_bid(self) -> Optional[float]:
        """Get the bid value."""
        return getattr(self, 'bid', None)
    
    def get_offer(self) -> Optional[float]:
        """Get the offer value."""
        return getattr(self, 'offer', None)
    
    def get_spread(self) -> Optional[float]:
        """Get the bid-offer spread."""
        bid = self.get_bid()
        offer = self.get_offer()
        if bid is not None and offer is not None:
            return abs(offer - bid)
        return None


class PairIdMixin:
    """
    Mixin for models with pair_id field.
    
    Provides helper methods for pair ID handling.
    Used in: Multiple models
    """
    
    def get_pair_id(self) -> Optional[int]:
        """Get the pair ID."""
        return getattr(self, 'pair_id', None)


class FlagsMixin:
    """
    Mixin for models with various flag fields (deemed_bo_flag, so_flag, stor_flag, rr_flag).
    
    Provides helper methods for flag handling.
    Used in: Multiple models
    """
    
    def is_deemed_bo(self) -> bool:
        """Check if deemed BO flag is set."""
        return getattr(self, 'deemed_bo_flag', False) or False
    
    def is_so_flagged(self) -> bool:
        """Check if SO flag is set."""
        return getattr(self, 'so_flag', False) or False
    
    def is_stor_flagged(self) -> bool:
        """Check if STOR flag is set."""
        return getattr(self, 'stor_flag', False) or False
    
    def is_rr_flagged(self) -> bool:
        """Check if RR flag is set."""
        return getattr(self, 'rr_flag', False) or False


class CapacityMixin:
    """
    Mixin for models with capacity fields (normal_capacity, available_capacity, unavailable_capacity).
    
    Provides helper methods for capacity handling.
    Used in: Multiple models
    """
    
    def get_normal_capacity(self) -> Optional[float]:
        """Get the normal capacity."""
        return getattr(self, 'normal_capacity', None)
    
    def get_available_capacity(self) -> Optional[float]:
        """Get the available capacity."""
        return getattr(self, 'available_capacity', None)
    
    def get_unavailable_capacity(self) -> Optional[float]:
        """Get the unavailable capacity."""
        return getattr(self, 'unavailable_capacity', None)
    
    def get_capacity_utilization(self) -> Optional[float]:
        """Get capacity utilization as percentage."""
        normal = self.get_normal_capacity()
        available = self.get_available_capacity()
        if normal and normal > 0 and available is not None:
            return (available / normal) * 100
        return None


class LeadPartyMixin:
    """
    Mixin for models with lead_party_name and optionally lead_party_id fields.
    
    Provides helper methods for lead party handling.
    Used in: Multiple models
    """
    
    def get_lead_party_name(self) -> Optional[str]:
        """Get the lead party name."""
        return getattr(self, 'lead_party_name', None)
    
    def get_lead_party_id(self) -> Optional[str]:
        """Get the lead party ID."""
        return getattr(self, 'lead_party_id', None)


class MridMixin:
    """
    Mixin for models with mrid or m_rid field.
    
    Provides helper methods for MRID handling.
    Used in: 3+ models
    """
    
    def get_mrid(self) -> Optional[str]:
        """Get the MRID (Message Resource Identifier)."""
        # Try both possible field names
        return getattr(self, 'mrid', None) or getattr(self, 'm_rid', None)


class VolumeMixin:
    """
    Mixin for models with volume field.
    
    Provides helper methods for volume handling.
    Used in: 8 models
    """
    
    def get_volume(self) -> Optional[float]:
        """Get the volume."""
        return getattr(self, 'volume', None)
    
    def get_volume_mwh(self) -> Optional[float]:
        """Get volume in MWh."""
        return self.get_volume()
    
    def get_volume_gwh(self) -> Optional[float]:
        """Get volume in GWh."""
        volume = self.get_volume()
        return volume / 1000 if volume is not None else None


class CostMixin:
    """
    Mixin for models with cost field.
    
    Provides helper methods for cost handling.
    Used in: 3+ models
    """
    
    def get_cost(self) -> Optional[float]:
        """Get the cost."""
        return getattr(self, 'cost', None)
    
    def get_cost_per_mw(self, volume: Optional[float] = None) -> Optional[float]:
        """Get cost per MW."""
        cost = self.get_cost()
        if cost is not None and volume and volume > 0:
            return cost / volume
        return None


class DemandMixin:
    """
    Mixin for models with demand field.
    
    Provides helper methods for demand handling.
    Used in: 3+ models
    """
    
    def get_demand(self) -> Optional[int]:
        """Get the demand."""
        return getattr(self, 'demand', None)
    
    def get_demand_mw(self) -> Optional[int]:
        """Get demand in MW."""
        return self.get_demand()
    
    def get_demand_gw(self) -> Optional[float]:
        """Get demand in GW."""
        demand = self.get_demand()
        return demand / 1000 if demand is not None else None


class GenerationMixin:
    """
    Mixin for models with generation field.
    
    Provides helper methods for generation handling.
    Used in: 3+ models
    """
    
    def get_generation(self) -> Optional[int]:
        """Get the generation."""
        return getattr(self, 'generation', None)
    
    def get_generation_mw(self) -> Optional[int]:
        """Get generation in MW."""
        return self.get_generation()
    
    def get_generation_gw(self) -> Optional[float]:
        """Get generation in GW."""
        generation = self.get_generation()
        return generation / 1000 if generation is not None else None


class MarginMixin:
    """
    Mixin for models with margin field.
    
    Provides helper methods for margin handling.
    Used in: 5 models
    """
    
    def get_margin(self) -> Optional[int]:
        """Get the margin."""
        return getattr(self, 'margin', None)
    
    def get_margin_mw(self) -> Optional[int]:
        """Get margin in MW."""
        return self.get_margin()


class SurplusMixin:
    """
    Mixin for models with surplus field.
    
    Provides helper methods for surplus handling.
    Used in: 4 models
    """
    
    def get_surplus(self) -> Optional[int]:
        """Get the surplus."""
        return getattr(self, 'surplus', None)


class ImbalanceMixin:
    """
    Mixin for models with imbalance field.
    
    Provides helper methods for imbalance handling.
    Used in: Multiple models
    """
    
    def get_imbalance(self) -> Optional[int]:
        """Get the imbalance."""
        return getattr(self, 'imbalance', None)


class FrequencyMixin:
    """
    Mixin for models with frequency field.
    
    Provides helper methods and validation for frequency.
    Used in: Multiple models
    """
    
    @field_validator('frequency')
    @classmethod
    def validate_frequency_value(cls, v: Optional[float]) -> Optional[float]:
        """Validate frequency is in valid range (47-53 Hz)."""
        return validate_frequency(v)
    
    def get_frequency(self) -> Optional[float]:
        """Get the frequency in Hz."""
        return getattr(self, 'frequency', None)
    
    def is_normal_frequency(self) -> bool:
        """Check if frequency is within normal range (49.5-50.5 Hz)."""
        freq = self.get_frequency()
        if freq is not None:
            return 49.5 <= freq <= 50.5
        return False


class TemperatureMixin:
    """
    Mixin for models with temperature field.
    
    Provides helper methods for temperature handling.
    Used in: Multiple models
    """
    
    def get_temperature(self) -> Optional[float]:
        """Get the temperature in Celsius."""
        return getattr(self, 'temperature', None)
    
    def get_temperature_fahrenheit(self) -> Optional[float]:
        """Get temperature in Fahrenheit."""
        temp_c = self.get_temperature()
        if temp_c is not None:
            return (temp_c * 9/5) + 32
        return None


class YearMixin:
    """
    Mixin for models with year field.
    
    Provides helper methods for year handling.
    Used in: 14 models
    """
    
    def get_year(self) -> Optional[int]:
        """Get the year."""
        return getattr(self, 'year', None)


class WeekMixin:
    """
    Mixin for models with week field.
    
    Provides helper methods for week handling.
    Used in: 7 models
    """
    
    def get_week(self) -> Optional[int]:
        """Get the week number."""
        return getattr(self, 'week', None)


class MonthMixin:
    """
    Mixin for models with month field.
    
    Provides helper methods for month handling.
    Used in: Multiple models
    """
    
    def get_month(self) -> Optional[str]:
        """Get the month."""
        return getattr(self, 'month', None)


class ForecastDateMixin:
    """
    Mixin for models with forecast_date field.
    
    Provides helper methods for forecast date handling.
    Used in: 13 models
    """
    
    def get_forecast_date(self) -> Optional[date]:
        """Get the forecast date."""
        return getattr(self, 'forecast_date', None)


class BoundaryMixin:
    """
    Mixin for models with boundary field.
    
    Provides helper methods for boundary handling.
    Used in: 10 models
    """
    
    def get_boundary(self) -> Optional[str]:
        """Get the boundary."""
        return getattr(self, 'boundary', None)
    
    def is_gb_boundary(self) -> bool:
        """Check if boundary is GB."""
        boundary = self.get_boundary()
        return str(boundary) == 'GB' if boundary else False


class OutputUsableMixin:
    """
    Mixin for models with output_usable field.
    
    Provides helper methods for output usable handling.
    Used in: 8 models
    """
    
    def get_output_usable(self) -> Optional[int]:
        """Get the output usable in MW."""
        return getattr(self, 'output_usable', None)
    
    def get_output_usable_gw(self) -> Optional[float]:
        """Get output usable in GW."""
        output = self.get_output_usable()
        return output / 1000 if output is not None else None


class BiddingZoneMixin:
    """
    Mixin for models with bidding_zone field.
    
    Provides helper methods for bidding zone handling.
    Used in: 5 models
    """
    
    def get_bidding_zone(self) -> Optional[str]:
        """Get the bidding zone."""
        return getattr(self, 'bidding_zone', None)


class InterconnectorMixin:
    """
    Mixin for models with interconnector_name field.
    
    Provides helper methods for interconnector handling.
    Used in: 4 models
    """
    
    def get_interconnector_name(self) -> Optional[str]:
        """Get the interconnector name."""
        return getattr(self, 'interconnector_name', None)


class SettlementDateMixin:
    """
    Mixin for models with ONLY settlement_date (without settlement_period).
    
    Provides helper methods for settlement date handling.
    Used in: Models with settlement_date but not settlement_period
    """
    
    def get_settlement_date(self) -> Optional[date]:
        """Get the settlement date."""
        return getattr(self, 'settlement_date', None)

