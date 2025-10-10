"""
Basic usage examples for the Elexon BMRS Python client.

This script demonstrates the most common use cases for accessing
UK electricity market data from the BMRS API with type-safe Pydantic models.

Each method returns its own specific response type!
"""

from datetime import date, datetime, timedelta
from elexon_bmrs import (
    BMRSClient,
    SystemDemandResponse,
    GenerationResponse,
    WindForecastResponse,
    SystemPricesResponse,
    SystemFrequencyResponse,
)
from elexon_bmrs.generated_models import (
    DemandOutturnNational,
    WindGenerationForecast,
)

# Replace with your actual API key (get one at https://www.elexonportal.co.uk/)
# API key is optional but strongly recommended for higher rate limits
API_KEY = "your-api-key-here"


def example_generation_data():
    """Example: Get generation data by fuel type with specific typed response."""
    print("=" * 60)
    print("Example 1: Generation by Fuel Type (Specific Type)")
    print("=" * 60)

    with BMRSClient(api_key=API_KEY) as client:
        # Get generation data for the last 2 days
        today = date.today()
        yesterday = today - timedelta(days=1)

        # Returns GenerationResponse automatically!
        response: GenerationResponse = client.get_generation_by_fuel_type(
            from_date=yesterday, to_date=today
        )
        
        print(f"\nGeneration data from {yesterday} to {today}:")
        print(f"  Total records: {len(response.data)}")
        print(f"  Response type: {type(response).__name__} ✓")
        
        if response.data:
            first_record = response.data[0]
            print(f"  Sample record keys: {list(first_record.keys())[:5]}...")


def example_demand_data():
    """Example: Get system demand data with specific typed response."""
    print("\n" + "=" * 60)
    print("Example 2: System Demand (Specific Response Type)")
    print("=" * 60)

    with BMRSClient(api_key=API_KEY) as client:
        today = date.today()

        # Method automatically returns SystemDemandResponse!
        response: SystemDemandResponse = client.get_system_demand(
            from_date=today, to_date=today, 
            settlement_period_from=1, 
            settlement_period_to=10
        )
        # ↑ Returns SystemDemandResponse - specific to demand data!
        
        print(f"\nDemand data for {today} (first 10 settlement periods):")
        print(f"  Total records: {len(response.data)}")
        print(f"  Response type: {type(response).__name__} ✓")
        
        # Parse individual records with type-safe model
        try:
            demands = [DemandOutturnNational(**item) for item in response.data[:3]]
            
            print("\n  Type-safe parsed records:")
            for i, demand in enumerate(demands, 1):
                print(f"    {i}. Period {demand.settlement_period}: {demand.demand} MW")
                # ↑ IDE provides autocomplete for all fields!
        except Exception as e:
            print(f"  Note: Could not parse with DemandOutturnNational model: {e}")
            print(f"  Raw data structure: {list(response.data[0].keys()) if response.data else 'No data'}")


def example_pricing_data():
    """Example: Get system prices - returns SystemPricesResponse automatically."""
    print("\n" + "=" * 60)
    print("Example 3: System Prices (SystemPricesResponse)")
    print("=" * 60)

    with BMRSClient(api_key=API_KEY) as client:
        today = date.today()

        # Automatically returns SystemPricesResponse!
        response: SystemPricesResponse = client.get_system_prices(
            settlement_date=today, 
            settlement_period=20
        )

        print(f"\nSystem prices for {today}, period 20:")
        print(f"  Records: {len(response.data)}")
        print(f"  Response type: {type(response).__name__} ✓")
        
        if response.data:
            for item in response.data[:3]:  # Show first 3
                # Type-safe access with validation
                settlement_period = item.get("settlementPeriod")
                price = item.get("price")
                print(f"    Period {settlement_period}: £{price}/MWh" if price else "    No price data")


def example_frequency_data():
    """Example: Get system frequency - returns SystemFrequencyResponse."""
    print("\n" + "=" * 60)
    print("Example 4: System Frequency (SystemFrequencyResponse)")
    print("=" * 60)

    with BMRSClient(api_key=API_KEY) as client:
        today = date.today()
        yesterday = today - timedelta(days=1)

        # Automatically returns SystemFrequencyResponse!
        response: SystemFrequencyResponse = client.get_system_frequency(
            from_date=yesterday, 
            to_date=today
        )

        print(f"\nSystem frequency from {yesterday} to {today}:")
        print(f"  Total measurements: {len(response.data)}")
        print(f"  Response type: {type(response).__name__} ✓")
        
        if response.data:
            print(f"  Sample readings:")
            for item in response.data[:5]:  # First 5
                timestamp = item.get("timestamp", "N/A")
                frequency = item.get("frequency", "N/A")
                print(f"    {timestamp}: {frequency} Hz")


def example_wind_forecast():
    """Example: Get wind generation forecast - returns WindForecastResponse."""
    print("\n" + "=" * 60)
    print("Example 5: Wind Generation Forecast (WindForecastResponse)")
    print("=" * 60)

    with BMRSClient(api_key=API_KEY) as client:
        today = date.today()
        next_week = today + timedelta(days=7)

        # Automatically returns WindForecastResponse!
        response: WindForecastResponse = client.get_wind_generation_forecast(
            from_date=today, to_date=next_week
        )

        print(f"\nWind generation forecast from {today} to {next_week}:")
        print(f"  Total forecasts: {len(response.data)}")
        print(f"  Response type: {type(response).__name__} ✓")
        
        # Try to parse with generated model
        try:
            forecasts = [
                WindGenerationForecast(**item) 
                for item in response.data[:5]  # First 5 for demo
            ]
            
            print("\n  Type-safe parsed forecasts:")
            for i, forecast in enumerate(forecasts, 1):
                gen = forecast.generation if forecast.generation else "N/A"
                print(f"    {i}. {forecast.start_time}: {gen} MW")
                # IDE provides full autocomplete for forecast.* fields!
        except Exception as e:
            print(f"  Note: Model parsing: {e}")
            if response.data:
                print(f"  Available fields: {list(response.data[0].keys())}")


def example_market_index():
    """Example: Get market index - returns SystemPricesResponse automatically."""
    print("\n" + "=" * 60)
    print("Example 6: Market Index (SystemPricesResponse)")
    print("=" * 60)

    with BMRSClient(api_key=API_KEY) as client:
        today = date.today()

        # Automatically returns SystemPricesResponse!
        response: SystemPricesResponse = client.get_market_index(settlement_date=today)

        print(f"\nMarket index for {today}:")
        print(f"  Records: {len(response.data)}")
        print(f"  Response type: {type(response).__name__} ✓")
        
        if response.metadata:
            print(f"  Metadata keys: {list(response.metadata.keys())}")
        
        if response.data:
            print(f"  First record: {response.data[0]}")


def example_without_context_manager():
    """Example: Using the client without context manager - still type-safe!"""
    print("\n" + "=" * 60)
    print("Example 7: Without Context Manager (Specific Response Type)")
    print("=" * 60)

    # Initialize client
    client = BMRSClient(api_key=API_KEY)

    try:
        today = date.today()
        
        # Automatically returns SystemDemandResponse!
        response: SystemDemandResponse = client.get_system_demand(
            from_date=today, 
            to_date=today
        )
        
        print(f"\nDemand data for {today}:")
        print(f"  Records: {len(response.data)}")
        print(f"  Response type: {type(response).__name__} ✓")
        
        # Demonstrate type safety benefits
        print(f"\n  ✓ Response is SystemDemandResponse (specific to demand)")
        print(f"  ✓ Automatically validated by Pydantic")
        print(f"  ✓ All fields type-checked")
        print(f"  ✓ IDE autocomplete available for response.data, response.metadata")
    finally:
        # Always close the client
        client.close()


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 8 + "Elexon BMRS Type-Safe Client Examples" + " " * 12 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n🎯 All examples use Pydantic models for full type safety!")
    print("📝 Your IDE will provide autocomplete for all response fields")
    print("\nNote: Replace API_KEY with your actual API key to run these examples.\n")

    # Run all examples
    try:
        example_generation_data()
        example_demand_data()
        example_pricing_data()
        example_frequency_data()
        example_wind_forecast()
        example_market_index()
        example_without_context_manager()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Make sure you have set a valid API key.")

