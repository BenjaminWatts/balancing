"""
Fully typed endpoint examples for the Elexon BMRS Python client.

This script demonstrates the TypedBMRSClient which provides proper
response types for all 287 API endpoints instead of Dict[str, Any].

Key benefits:
- Full type safety with Pydantic models
- IDE autocomplete for all response fields
- Type checking with mypy
- Automatic data validation
"""

from datetime import datetime, timedelta
from elexon_bmrs import TypedBMRSClient
from elexon_bmrs.generated_models import (
    AbucDatasetRow,
    ActualAggregatedGenerationPerTypeDatasetRow,
    BidOfferDatasetRow,
)

# Replace with your actual API key (get one at https://www.elexonportal.co.uk/)
API_KEY = "your-api-key-here"


def example_typed_abuc_data():
    """Example: Fully typed ABUC (Amount of Balancing Reserves Under Contract) data."""
    print("=" * 70)
    print("Example 1: Typed ABUC Data (Amount of Balancing Reserves Under Contract)")
    print("=" * 70)

    with TypedBMRSClient(api_key=API_KEY) as client:
        # Get ABUC data - returns AbucDatasetRow_DatasetResponse, not Dict[str, Any]!
        end_time = datetime.now()
        start_time = end_time - timedelta(days=1)
        
        response = client.get_datasets_abuc(
            publishDateTimeFrom=start_time.isoformat() + "Z",
            publishDateTimeTo=end_time.isoformat() + "Z"
        )
        
        print(f"\nABUC Data Response Type: {type(response).__name__}")
        print(f"Response has data field: {hasattr(response, 'data')}")
        print(f"Total records: {len(response.data or [])}")
        
        # Type-safe access to response fields
        if response.data:
            print(f"\nSample ABUC records:")
            for i, row in enumerate(response.data[:3], 1):
                # Full IDE autocomplete available for row.* fields!
                print(f"  {i}. Dataset: {row.dataset}")
                print(f"     Document ID: {row.documentId}")
                print(f"     Business Type: {row.businessType}")
                print(f"     PSR Type: {row.psrType}")
                print(f"     Publish Time: {row.publishTime}")
                print(f"     Quantity: {row.quantity} MW")
                print()


def example_typed_agpt_data():
    """Example: Fully typed AGPT (Aggregated Generation Per Type) data."""
    print("\n" + "=" * 70)
    print("Example 2: Typed AGPT Data (Aggregated Generation Per Type)")
    print("=" * 70)

    with TypedBMRSClient(api_key=API_KEY) as client:
        # Get AGPT data - returns ActualAggregatedGenerationPerTypeDatasetRow_DatasetResponse
        end_time = datetime.now()
        start_time = end_time - timedelta(days=1)
        
        response = client.get_datasets_agpt(
            publishDateTimeFrom=start_time.isoformat() + "Z",
            publishDateTimeTo=end_time.isoformat() + "Z"
        )
        
        print(f"\nAGPT Data Response Type: {type(response).__name__}")
        print(f"Total records: {len(response.data or [])}")
        
        # Type-safe access with full IDE support
        if response.data:
            print(f"\nSample AGPT records:")
            for i, row in enumerate(response.data[:5], 1):
                # IDE provides autocomplete for all fields!
                print(f"  {i}. Fuel Type: {row.fuelType}")
                print(f"     Generation: {row.generation} MW")
                print(f"     Output: {row.output} MW")
                print(f"     Publish Time: {row.publishTime}")
                print(f"     Business Type: {row.businessType}")
                print()


def example_typed_bod_data():
    """Example: Fully typed BOD (Bid Offer Data) data."""
    print("\n" + "=" * 70)
    print("Example 3: Typed BOD Data (Bid Offer Data)")
    print("=" * 70)

    with TypedBMRSClient(api_key=API_KEY) as client:
        # Get BOD data - returns BidOfferDatasetRow_DatasetResponse
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=6)
        
        response = client.get_datasets_bod(
            publishDateTimeFrom=start_time.isoformat() + "Z",
            publishDateTimeTo=end_time.isoformat() + "Z"
        )
        
        print(f"\nBOD Data Response Type: {type(response).__name__}")
        print(f"Total records: {len(response.data or [])}")
        
        # Type-safe access to bid-offer data
        if response.data:
            print(f"\nSample BOD records:")
            for i, row in enumerate(response.data[:3], 1):
                # Full type safety for bid-offer fields!
                print(f"  {i}. BM Unit: {row.bmUnit}")
                print(f"     Bid Offer Level: {row.bidOfferLevel}")
                print(f"     Bid Offer Volume: {row.bidOfferVolume}")
                print(f"     Bid Offer Price: £{row.bidOfferPrice}/MWh")
                print(f"     Publish Time: {row.publishTime}")
                print()


def example_type_coverage():
    """Example: Check type coverage of the client."""
    print("\n" + "=" * 70)
    print("Example 4: Type Coverage Information")
    print("=" * 70)

    client = TypedBMRSClient(api_key=API_KEY)
    
    # Get typing information
    info = client.get_typing_info()
    stats = info['typing_stats']
    
    print(f"\nType Coverage Statistics:")
    print(f"  Total endpoints: {stats['total_endpoints']}")
    print(f"  Typed endpoints: {stats['typed_endpoints']}")
    print(f"  Untyped endpoints: {stats['untyped_endpoints']}")
    print(f"  Coverage: {stats['typing_coverage_percent']}%")
    
    print(f"\nSample typed endpoints:")
    for endpoint in list(info['typed_endpoints'])[:10]:
        print(f"  ✅ {endpoint}")
    
    if info['untyped_endpoints']:
        print(f"\nSample untyped endpoints:")
        for endpoint in info['untyped_endpoints'][:5]:
            print(f"  ⚠️  {endpoint} (returns APIResponse)")


def example_type_checking():
    """Example: Demonstrate type checking capabilities."""
    print("\n" + "=" * 70)
    print("Example 5: Type Checking Demonstration")
    print("=" * 70)

    def process_abuc_data(client: TypedBMRSClient) -> None:
        """Process ABUC data with full type safety."""
        response = client.get_datasets_abuc(
            publishDateTimeFrom="2024-01-01T00:00:00Z",
            publishDateTimeTo="2024-01-02T00:00:00Z"
        )
        
        # Type checker knows response.data is List[AbucDatasetRow]
        total_quantity = 0
        for row in response.data or []:
            if row.quantity:
                total_quantity += row.quantity
        
        print(f"Total quantity across all ABUC records: {total_quantity} MW")
    
    # This function demonstrates type checking
    print("\nFunction 'process_abuc_data' demonstrates:")
    print("  ✅ Parameter type annotation (client: TypedBMRSClient)")
    print("  ✅ Return type annotation (-> None)")
    print("  ✅ Type-safe access to response.data")
    print("  ✅ Type-safe access to row.quantity")
    print("  ✅ mypy can verify all type usage")


def example_migration_from_standard_client():
    """Example: Migration from standard BMRSClient to TypedBMRSClient."""
    print("\n" + "=" * 70)
    print("Example 6: Migration from Standard Client")
    print("=" * 70)

    print("\nBefore (BMRSClient):")
    print("```python")
    print("from elexon_bmrs import BMRSClient")
    print("client = BMRSClient(api_key='your-key')")
    print("response = client.get_datasets_abuc(...)  # Returns Dict[str, Any]")
    print("data = response['data']  # No type safety!")
    print("```")

    print("\nAfter (TypedBMRSClient):")
    print("```python")
    print("from elexon_bmrs import TypedBMRSClient")
    print("client = TypedBMRSClient(api_key='your-key')")
    print("response = client.get_datasets_abuc(...)  # Returns AbucDatasetRow_DatasetResponse")
    print("for row in response.data or []:  # Type-safe access!")
    print("    print(row.dataset)  # IDE autocomplete!")
    print("```")

    print("\nMigration benefits:")
    print("  ✅ Same method signatures - drop-in replacement")
    print("  ✅ Proper return types instead of Dict[str, Any]")
    print("  ✅ Full IDE autocomplete and type checking")
    print("  ✅ Automatic data validation with Pydantic")
    print("  ✅ Better error handling and debugging")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 6 + "Elexon BMRS Typed Client Examples" + " " * 6 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n🎯 All examples use TypedBMRSClient for full type safety!")
    print("📝 IDE provides autocomplete for all response fields")
    print("🔍 Type checking with mypy validates all code")
    print("\nNote: Replace API_KEY with your actual API key to run these examples.\n")

    # Run all examples
    try:
        example_typed_abuc_data()
        example_typed_agpt_data()
        example_typed_bod_data()
        example_type_coverage()
        example_type_checking()
        example_migration_from_standard_client()

        print("\n" + "=" * 70)
        print("All typed client examples completed successfully!")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Make sure you have set a valid API key.")
