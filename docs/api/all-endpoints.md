# Complete Endpoint Reference

This page lists all **287 available endpoints** in the BMRS API client. All methods are auto-generated from the official OpenAPI specification with full docstrings and type hints.

## How to Use

Every endpoint is available as a method on the `BMRSClient` instance:

```python
from elexon_bmrs import BMRSClient

client = BMRSClient(api_key="your-key")

# All 287 methods are available
data = client.get_balancing_dynamic(bmUnit="2__HFLEX001", snapshotAt="2024-01-01T12:00:00Z")
```

## Getting Help

To get detailed help for any endpoint:

```python
# View method signature and docstring
help(client.get_balancing_dynamic)

# List all available methods
methods = [m for m in dir(client) if m.startswith('get_')]
print(f"Total endpoints: {len(methods)}")
```

## Endpoint Categories

### Balancing Mechanism

Dynamic, physical, and rate data for Balancing Mechanism Units (BMUs):

- `get_balancing_dynamic` - Dynamic data per BMU (SEL, SIL, MZT, MNZT, MDV, MDP, NTB, NTO, NDZ)
- `get_balancing_dynamic_all` - Market-wide dynamic data
- `get_balancing_dynamic_rates` - Dynamic rate data per BMU
- `get_balancing_dynamic_rates_all` - Market-wide dynamic rate data
- `get_balancing_physical` - Physical data per BMU (FPN, PN, BOA)
- `get_balancing_physical_all` - Market-wide physical data
- `get_balancing_bid_offer` - Bid-offer data per BMU
- `get_balancing_bid_offer_all` - Market-wide bid-offer data
- `get_balancing_acceptances` - Acceptance data per BMU
- `get_balancing_acceptances_all` - Market-wide acceptances
- `get_balancing_acceptances_all_latest` - Latest market-wide acceptances

### Non-BM Data

Data for non-Balancing Mechanism services:

- `get_balancing_nonbm_disbsad` - DISBSAD summary
- `get_balancing_nonbm_disbsad_summary` - DISBSAD summary
- `get_balancing_nonbm_disbsad_details` - DISBSAD details
- `get_balancing_nonbm_netbsad` - NETBSAD summary
- `get_balancing_nonbm_netbsad_events` - NETBSAD events
- `get_balancing_nonbm_stor` - STOR summary
- `get_balancing_nonbm_stor_events` - STOR events
- `get_balancing_nonbm_volumes` - Non-BM volumes

### Pricing & Settlement

Market prices, settlements, and cashflows:

- `get_balancing_pricing_market_index` - Market index prices
- `get_balancing_settlement_system_prices` - System prices
- `get_balancing_settlement_summary` - Settlement summary
- `get_balancing_settlement_stack_all` - Stack data
- `get_balancing_settlement_market_depth` - Market depth
- `get_balancing_settlement_acceptance_volumes_all` - Acceptance volumes
- `get_balancing_settlement_acceptances_all` - Settlement acceptances
- `get_balancing_settlement_indicative_volumes_all` - Indicative volumes
- `get_balancing_settlement_indicative_cashflows_all` - Indicative cashflows
- `get_balancing_settlement_messages` - Settlement messages
- `get_balancing_settlement_default_notices` - Default notices

### Generation & Demand

Generation by fuel type, wind forecasts, and demand data:

- `get_generation_outturn_summary` - Generation outturn summary
- `get_generation_outturn_fueltype` - Generation by fuel type
- `get_generation_actual_per_type` - Actual generation per type
- `get_generation_wind_and_solar_forecast` - Wind and solar forecasts
- `get_generation_availability` - Generation availability
- `get_demand_outturn_national` - National demand outturn
- `get_demand_outturn_transmission` - Transmission demand
- `get_demand_peak` - Peak demand
- `get_demand_total` - Total demand
- `get_demand_rolling_system_demand` - Rolling system demand

### System Data

System frequency, warnings, and operational data:

- `get_system_frequency` - System frequency measurements
- `get_system_warnings` - System warnings
- `get_system_misc_system_warnings` - Miscellaneous system warnings
- `get_loss_of_load_probability` - Loss of load probability
- `get_margin_forecast` - Margin forecast

### Reference Data

Reference datasets and metadata:

- `get_cdn` - Credit Default Notice
- `get_reference_bmunits` - BM Unit reference data
- `get_reference_interconnectors` - Interconnector reference
- `get_reference_fueltypes` - Fuel type reference

### Dataset Endpoints

Access to specific BMRS datasets (100+ datasets):

#### Common Datasets

- `get_datasets_abuc` - Accepted Bids/Offers (ABUC)
- `get_datasets_agpt` - Aggregated Generation Per Type (AGPT) 
- `get_datasets_agws` - Aggregated Generation Wind/Solar (AGWS)
- `get_datasets_aobe` - Accepted Offered/Bid Energy (AOBE)
- `get_datasets_bod` - Bid-Offer Data (BOD)
- `get_datasets_boalf` - Bid-Offer Acceptance Level Flagged (BOALF)
- `get_datasets_freq` - System Frequency (FREQ)
- `get_datasets_imbalngc` - Imbalance Prices (IMBALNGC)
- `get_datasets_indod` - Initial National Demand Outturn (INDOD)
- `get_datasets_ispstack` - Indicated System Price Stack (ISPSTACK)
- `get_datasets_lolpdrm` - Loss of Load Probability & De-rated Margin (LOLPDRM)
- `get_datasets_melngc` - Maximum Export Limit (MELNGC)
- `get_datasets_milngc` - Maximum Import Limit (MILNGC)
- `get_datasets_ndfd` - National Demand Forecast Day Ahead (NDFD)
- `get_datasets_pn` - Physical Notification (PN)
- `get_datasets_qpn` - Quiescent Physical Notification (QPN)
- `get_datasets_rdre` - Run Down Rate Export (RDRE)
- `get_datasets_rdri` - Run Down Rate Import (RDRI)
- `get_datasets_rure` - Run Up Rate Export (RURE)
- `get_datasets_ruri` - Run Up Rate Import (RURI)
- `get_datasets_soso` - SO-SO Prices (SOSO)
- `get_datasets_syswarn` - System Warnings (SYSWARN)
- `get_datasets_temp` - Temperature Data (TEMP)
- `get_datasets_tsdf` - Transmission System Demand Forecast (TSDF)
- `get_datasets_uou` - Unpriced Offered/Bid Units (UOU)

#### All Dataset Methods

The client includes methods for **over 100 specific datasets**, each with:
- Standard `get_datasets_*` method for historical data
- `get_datasets_*_stream` method for streaming data (where available)

To see all dataset methods:

```python
dataset_methods = [m for m in dir(client) if m.startswith('get_datasets_')]
print(f"Total dataset endpoints: {len(dataset_methods)}")
```

### Streaming Endpoints

Many datasets support streaming for real-time data:

- Append `_stream` to dataset names (e.g., `get_datasets_freq_stream`)
- Provides real-time updates as they're published
- Useful for monitoring live system conditions

```python
# Example: Stream system frequency data
freq_stream = client.get_datasets_freq_stream(from_date="2024-01-01")
```

## Method Documentation

### Auto-Generated Docstrings

Every method includes comprehensive documentation extracted from the OpenAPI spec:

```python
help(client.get_balancing_dynamic)
```

Output:
```
Dynamic data per BMU (SEL, SIL, MZT, MNZT, MDV, MDP, NTB, NTO, NDZ)

This endpoint provides the dynamic data for a requested BMU, excluding physical rate data.
It returns a "snapshot" of data valid at a given time, and optionally a time series of changes.

Args:
    bmUnit: The BM Unit to query
    snapshotAt: When to retrieve a snapshot of data at
    until: When to retrieve data until (optional)
    snapshotAtSettlementPeriod: Settlement period to retrieve snapshot at (optional)
    ...

Returns:
    API response data
```

### Type Hints

All parameters and return types are fully typed:

```python
def get_balancing_dynamic(
    self,
    bmUnit: str,
    snapshotAt: str,
    until: Optional[str] = None,
    snapshotAtSettlementPeriod: Optional[int] = None,
    ...
) -> Dict[str, Any]:
```

## Complete Method List

For the complete alphabetical list of all 287 methods, use:

```python
from elexon_bmrs import BMRSClient

client = BMRSClient()
methods = sorted([m for m in dir(client) if m.startswith('get_')])

for method in methods:
    print(f"  {method}")
```

## Examples

### Balancing Mechanism Data

```python
# Get dynamic data for specific BMU
dynamic = client.get_balancing_dynamic(
    bmUnit="2__HFLEX001",
    snapshotAt="2024-01-01T12:00:00Z"
)

# Get all acceptances for settlement period
acceptances = client.get_balancing_acceptances_all(
    settlementDate="2024-01-01",
    settlementPeriod=10
)
```

### Generation Data

```python
# Get generation by fuel type
generation = client.get_generation_actual_per_type(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

# Get wind forecast
wind = client.get_generation_wind_and_solar_forecast(
    from_date="2024-01-01"
)
```

### Pricing Data

```python
# Get market index prices
prices = client.get_balancing_pricing_market_index(
    settlement_date="2024-01-01"
)

# Get system prices
sys_prices = client.get_balancing_settlement_system_prices(
    settlement_date="2024-01-01",
    settlement_period=10
)
```

### Dataset Access

```python
# Get specific dataset
freq_data = client.get_datasets_freq(
    from_date="2024-01-01",
    to_date="2024-01-02"
)

# Stream dataset
freq_stream = client.get_datasets_freq_stream(
    from_date="2024-01-01"
)
```

## See Also

- [Client API Reference](client.md) - Main client documentation
- [Generated Client](../development/code-generation.md) - Code generation details
- [Examples](../examples/basic.md) - Usage examples
- [OpenAPI Specification](https://bmrs.elexon.co.uk/api-documentation) - Official API docs

