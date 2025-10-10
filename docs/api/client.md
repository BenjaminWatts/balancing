# Client API Reference

This page documents the main `BMRSClient` class and all available methods.

The `BMRSClient` inherits from `GeneratedBMRSMethods`, providing access to **all 287 BMRS API endpoints** with full type hints and documentation.

## Core Client Methods

::: elexon_bmrs.client.BMRSClient
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2
      members:
        - __init__
        - close
        - __enter__
        - __exit__
      filters:
        - "!^get_.*"  # Exclude get_ methods to show them separately

## All Available Endpoints (287 Methods)

The client provides access to all BMRS API endpoints. Below are the main categories:

### Balancing Mechanism Endpoints

::: elexon_bmrs.generated_client.GeneratedBMRSMethods
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - get_balancing_dynamic
        - get_balancing_dynamic_all
        - get_balancing_dynamic_rates
        - get_balancing_dynamic_rates_all
        - get_balancing_physical
        - get_balancing_physical_all
        - get_balancing_bid_offer
        - get_balancing_bid_offer_all
        - get_balancing_acceptances
        - get_balancing_acceptances_all
        - get_balancing_acceptances_all_latest
      filters:
        - "!^get_balancing_nonbm.*"
        - "!^get_balancing_settlement.*"
        - "!^get_balancing_pricing.*"

### Generation & Demand Endpoints

::: elexon_bmrs.generated_client.GeneratedBMRSMethods
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - get_generation_outturn_summary
        - get_generation_outturn_fueltype
        - get_generation_actual_per_type
        - get_generation_wind_and_solar_forecast
        - get_generation_availability
        - get_demand_outturn_national
        - get_demand_outturn_transmission
        - get_demand_peak
        - get_demand_total
        - get_demand_rolling_system_demand
      filters:
        - "!^get_balancing.*"
        - "!^get_datasets.*"
        - "!^get_system.*"
        - "!^get_reference.*"

### System & Pricing Endpoints

::: elexon_bmrs.generated_client.GeneratedBMRSMethods
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - get_system_frequency
        - get_system_warnings
        - get_system_misc_system_warnings
        - get_loss_of_load_probability
        - get_margin_forecast
        - get_balancing_pricing_market_index
        - get_balancing_settlement_system_prices
        - get_balancing_settlement_summary
      filters:
        - "!^get_generation.*"
        - "!^get_demand.*"
        - "!^get_datasets.*"
        - "!^get_reference.*"

### Dataset Endpoints (Sample)

::: elexon_bmrs.generated_client.GeneratedBMRSMethods
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - get_datasets_abuc
        - get_datasets_agpt
        - get_datasets_bod
        - get_datasets_freq
        - get_datasets_imbalngc
        - get_datasets_pn
        - get_datasets_qpn
        - get_datasets_temp
      filters:
        - "!^get_balancing.*"
        - "!^get_generation.*"
        - "!^get_demand.*"
        - "!^get_system.*"
        - "!^get_reference.*"

## Complete Method List

For the complete list of all 287 methods, see the [Complete Endpoint Reference](all-endpoints.md).

You can also explore all methods programmatically:

```python
from elexon_bmrs import BMRSClient

client = BMRSClient()
methods = [m for m in dir(client) if m.startswith('get_')]
print(f"Total endpoints: {len(methods)}")  # 287

# Get help for any method
help(client.get_balancing_dynamic)
```

