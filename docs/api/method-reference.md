# Complete Method Reference

This page lists **all 287 available methods** in the BMRS API client, organized by category.

## Method Categories

### 1. Balancing Mechanism (20 methods)

**Dynamic Data:**
- `get_balancing_dynamic` - Dynamic data per BMU (SEL, SIL, MZT, MNZT, MDV, MDP, NTB, NTO, NDZ)
- `get_balancing_dynamic_all` - Market-wide dynamic data
- `get_balancing_dynamic_rates` - Dynamic rate data per BMU
- `get_balancing_dynamic_rates_all` - Market-wide dynamic rate data

**Physical Data:**
- `get_balancing_physical` - Physical data per BMU (FPN, PN, BOA)
- `get_balancing_physical_all` - Market-wide physical data

**Bid/Offer Data:**
- `get_balancing_bid_offer` - Bid-offer data per BMU
- `get_balancing_bid_offer_all` - Market-wide bid-offer data

**Acceptances:**
- `get_balancing_acceptances` - Acceptance data per BMU
- `get_balancing_acceptances_all` - Market-wide acceptances
- `get_balancing_acceptances_all_latest` - Latest market-wide acceptances

**Non-BM Services:**
- `get_balancing_nonbm_disbsad_details` - DISBSAD details
- `get_balancing_nonbm_disbsad_summary` - DISBSAD summary
- `get_balancing_nonbm_netbsad` - NETBSAD summary
- `get_balancing_nonbm_netbsad_events` - NETBSAD events
- `get_balancing_nonbm_stor` - STOR summary
- `get_balancing_nonbm_stor_events` - STOR events
- `get_balancing_nonbm_volumes` - Non-BM volumes

**Pricing:**
- `get_balancing_pricing_market_index` - Market index prices

### 2. Settlement Data (12 methods)

- `get_balancing_settlement_acceptance_volumes_all` - Acceptance volumes
- `get_balancing_settlement_acceptances_all` - Settlement acceptances
- `get_balancing_settlement_default_notices` - Default notices
- `get_balancing_settlement_indicative_cashflows_all` - Indicative cashflows
- `get_balancing_settlement_indicative_volumes_all` - Indicative volumes
- `get_balancing_settlement_market_depth` - Market depth
- `get_balancing_settlement_messages` - Settlement messages
- `get_balancing_settlement_stack_all` - Stack data
- `get_balancing_settlement_summary` - Settlement summary
- `get_balancing_settlement_system_prices` - System prices

### 3. Generation & Demand (15 methods)

**Generation:**
- `get_generation_outturn_summary` - Generation outturn summary
- `get_generation_outturn_fueltype` - Generation by fuel type
- `get_generation_actual_per_type` - Actual generation per type
- `get_generation_wind_and_solar_forecast` - Wind and solar forecasts
- `get_generation_availability` - Generation availability

**Demand:**
- `get_demand_outturn_national` - National demand outturn
- `get_demand_outturn_transmission` - Transmission demand
- `get_demand_peak` - Peak demand
- `get_demand_total` - Total demand
- `get_demand_rolling_system_demand` - Rolling system demand

### 4. System Data (8 methods)

- `get_system_frequency` - System frequency measurements
- `get_system_warnings` - System warnings
- `get_system_misc_system_warnings` - Miscellaneous system warnings
- `get_loss_of_load_probability` - Loss of load probability
- `get_margin_forecast` - Margin forecast

### 5. Reference Data (3 methods)

- `get_cdn` - Credit Default Notice
- `get_reference_bmunits` - BM Unit reference data
- `get_reference_interconnectors` - Interconnector reference
- `get_reference_fueltypes` - Fuel type reference

### 6. Dataset Endpoints (150+ methods)

**Major Datasets:**

**ABUC - Accepted Bids/Offers:**
- `get_datasets_abuc` - Historical data
- `get_datasets_abuc_stream` - Streaming data

**AGPT - Aggregated Generation Per Type:**
- `get_datasets_agpt` - Historical data
- `get_datasets_agpt_stream` - Streaming data

**AGWS - Aggregated Generation Wind/Solar:**
- `get_datasets_agws` - Historical data
- `get_datasets_agws_stream` - Streaming data

**AOBE - Accepted Offered/Bid Energy:**
- `get_datasets_aobe` - Historical data
- `get_datasets_aobe_stream` - Streaming data

**ATL - Available Transmission Line:**
- `get_datasets_atl` - Historical data
- `get_datasets_atl_stream` - Streaming data

**B1610 - B1610 Data:**
- `get_datasets_b1610` - Historical data
- `get_datasets_b1610_stream` - Streaming data

**BEB - Bid-Offer Energy Balance:**
- `get_datasets_beb` - Historical data
- `get_datasets_beb_stream` - Streaming data

**BOALF - Bid-Offer Acceptance Level Flagged:**
- `get_datasets_boalf` - Historical data
- `get_datasets_boalf_stream` - Streaming data

**BOD - Bid-Offer Data:**
- `get_datasets_bod` - Historical data
- `get_datasets_bod_stream` - Streaming data

**CBS - Capacity Balancing Service:**
- `get_datasets_cbs` - Historical data
- `get_datasets_cbs_stream` - Streaming data

**FREQ - System Frequency:**
- `get_datasets_freq` - Historical data
- `get_datasets_freq_stream` - Streaming data

**IMBALNGC - Imbalance Prices:**
- `get_datasets_imbalngc` - Historical data
- `get_datasets_imbalngc_stream` - Streaming data

**INDOD - Initial National Demand Outturn:**
- `get_datasets_indod` - Historical data
- `get_datasets_indod_stream` - Streaming data

**ISPSTACK - Indicated System Price Stack:**
- `get_datasets_ispstack` - Historical data
- `get_datasets_ispstack_stream` - Streaming data

**LOLPDRM - Loss of Load Probability & De-rated Margin:**
- `get_datasets_lolpdrm` - Historical data
- `get_datasets_lolpdrm_stream` - Streaming data

**MELNGC - Maximum Export Limit:**
- `get_datasets_melngc` - Historical data
- `get_datasets_melngc_stream` - Streaming data

**MILNGC - Maximum Import Limit:**
- `get_datasets_milngc` - Historical data
- `get_datasets_milngc_stream` - Streaming data

**NDFD - National Demand Forecast Day Ahead:**
- `get_datasets_ndfd` - Historical data
- `get_datasets_ndfd_stream` - Streaming data

**PN - Physical Notification:**
- `get_datasets_pn` - Historical data
- `get_datasets_pn_stream` - Streaming data

**QPN - Quiescent Physical Notification:**
- `get_datasets_qpn` - Historical data
- `get_datasets_qpn_stream` - Streaming data

**RDRE - Run Down Rate Export:**
- `get_datasets_rdre` - Historical data
- `get_datasets_rdre_stream` - Streaming data

**RDRI - Run Down Rate Import:**
- `get_datasets_rdri` - Historical data
- `get_datasets_rdri_stream` - Streaming data

**RURE - Run Up Rate Export:**
- `get_datasets_rure` - Historical data
- `get_datasets_rure_stream` - Streaming data

**RURI - Run Up Rate Import:**
- `get_datasets_ruri` - Historical data
- `get_datasets_ruri_stream` - Streaming data

**SOSO - SO-SO Prices:**
- `get_datasets_soso` - Historical data
- `get_datasets_soso_stream` - Streaming data

**SYSWARN - System Warnings:**
- `get_datasets_syswarn` - Historical data
- `get_datasets_syswarn_stream` - Streaming data

**TEMP - Temperature Data:**
- `get_datasets_temp` - Historical data
- `get_datasets_temp_stream` - Streaming data

**TSDF - Transmission System Demand Forecast:**
- `get_datasets_tsdf` - Historical data
- `get_datasets_tsdf_stream` - Streaming data

**UOU - Unpriced Offered/Bid Units:**
- `get_datasets_uou` - Historical data
- `get_datasets_uou_stream` - Streaming data

## Complete Alphabetical List

For the complete alphabetical list of all 287 methods:

```python
from elexon_bmrs import BMRSClient

client = BMRSClient()
methods = sorted([m for m in dir(client) if m.startswith('get_')])

print(f"Total endpoints: {len(methods)}")
for method in methods:
    print(f"  {method}")
```

## Usage Examples

### Balancing Mechanism

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

## Method Documentation

Every method includes comprehensive documentation:

```python
# Get help for any method
help(client.get_balancing_dynamic)

# Shows:
# - Full docstring from OpenAPI spec
# - Parameter descriptions
# - Type hints
# - Return type
# - Examples (where available)
```

## See Also

- [Client API Reference](client.md) - Main client documentation
- [Generated Client](../development/code-generation.md) - Code generation details
- [Examples](../examples/basic.md) - Usage examples
- [OpenAPI Specification](https://bmrs.elexon.co.uk/api-documentation) - Official API docs

