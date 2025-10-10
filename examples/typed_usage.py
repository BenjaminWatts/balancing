"""
Type-safe usage examples for the Elexon BMRS Python client.

This script demonstrates how to use Pydantic models for type-safe API responses.
"""

from datetime import date, timedelta
from elexon_bmrs import BMRSClient, APIResponse
from elexon_bmrs.models import DemandData, GenerationByFuelType


# Replace with your actual API key (get one at https://www.elexonportal.co.uk/)
# API key is optional but strongly recommended for higher rate limits
API_KEY = "your-api-key-here"


def example_untyped_response():
    """Example: Traditional untyped response (Dict[str, Any])."""
    print("=" * 60)
    print("Example 1: Untyped Response (Traditional)")
    print("=" * 60)

    with BMRSClient(api_key=API_KEY) as client:
        today = date.today()

        # Returns Dict[str, Any] - no type safety
        response = client.get_system_demand(from_date=today, to_date=today)

        # You need to manually extract and validate data
        print(f"\nResponse type: {type(response)}")
        print(f"Data records: {len(response.get('data', []))}")
        
        if response.get("data"):
            first_record = response["data"][0]
            print(f"First record keys: {list(first_record.keys())[:5]}...")


def example_api_response_model():
    """Example: Using APIResponse model for structure."""
    print("\n" + "=" * 60)
    print("Example 2: APIResponse Model (Structured)")
    print("=" * 60)

    with BMRSClient(api_key=API_KEY) as client:
        today = date.today()

        # Get raw response
        raw_response = client.get_system_demand(from_date=today, to_date=today)

        # Parse with Pydantic model
        response = APIResponse(**raw_response)

        # Now you have type-safe access to response structure
        print(f"\nResponse has {len(response.data)} records")
        if response.metadata:
            print(f"Metadata keys: {list(response.metadata.keys())}")
        if response.total_records:
            print(f"Total records: {response.total_records}")


def example_importing_generated_models():
    """Example: Using auto-generated models from OpenAPI spec."""
    print("\n" + "=" * 60)
    print("Example 3: Using Generated Pydantic Models")
    print("=" * 60)

    # Import generated models for specific endpoints
    try:
        from elexon_bmrs.generated_models import (
            DemandOutturn,
            DemandOutturnNational,
            DemandOutturnTransmission,
        )

        print("\n✓ Imported generated models successfully")
        print(f"  - DemandOutturn")
        print(f"  - DemandOutturnNational")
        print(f"  - DemandOutturnTransmission")

        with BMRSClient(api_key=API_KEY) as client:
            today = date.today()
            raw_response = client.get_system_demand(from_date=today, to_date=today)

            # Parse individual records with generated models
            if raw_response.get("data"):
                first_record = raw_response["data"][0]
                
                # Try to parse with the model
                try:
                    typed_record = DemandOutturnNational(**first_record)
                    print(f"\n✓ Successfully parsed record with Pydantic model")
                    print(f"  Settlement Date: {typed_record.settlement_date}")
                    print(f"  Settlement Period: {typed_record.settlement_period}")
                    print(f"  Demand: {typed_record.demand} MW")
                except Exception as e:
                    print(f"\n⚠ Could not parse with model: {e}")

    except ImportError as e:
        print(f"\n✗ Generated models not available: {e}")
        print("Run: python tools/generate_models.py")


def example_type_hints_with_models():
    """Example: Using type hints for IDE support."""
    print("\n" + "=" * 60)
    print("Example 4: Type Hints for IDE Support")
    print("=" * 60)

    with BMRSClient(api_key=API_KEY) as client:
        today = date.today()

        # Get response with type hint
        response: APIResponse = APIResponse(**client.get_system_demand(
            from_date=today,
            to_date=today
        ))

        # Now your IDE can autocomplete and type-check
        print(f"\nTotal data records: {len(response.data)}")
        
        # Type hints help catch errors at development time
        # response.invalid_field  # IDE would warn this doesn't exist!


def example_validation_and_errors():
    """Example: Pydantic validation catches data issues."""
    print("\n" + "=" * 60)
    print("Example 5: Pydantic Validation")
    print("=" * 60)

    from pydantic import ValidationError

    # Example of invalid data
    invalid_data = {
        "data": "not-a-list",  # Should be a list
        "total_records": "not-a-number"  # Should be an int
    }

    try:
        response = APIResponse(**invalid_data)
    except ValidationError as e:
        print("\n✓ Pydantic caught validation errors:")
        for error in e.errors():
            print(f"  - Field '{error['loc'][0]}': {error['msg']}")


def example_model_with_config():
    """Example: Models with ConfigDict for flexibility."""
    print("\n" + "=" * 60)
    print("Example 6: Models with Extra Fields (ConfigDict)")
    print("=" * 60)

    # Our models use ConfigDict(extra='allow')
    # This means they accept extra fields not in the schema

    data_with_extras = {
        "data": [],
        "metadata": {"source": "BMRS"},
        "extra_field": "This won't cause an error",
        "another_extra": 12345
    }

    response = APIResponse(**data_with_extras)
    print(f"\n✓ Model accepted extra fields gracefully")
    print(f"  Known fields: data={response.data}, metadata={response.metadata}")
    print(f"  Extra fields are preserved in the model")


def example_parsing_list_of_models():
    """Example: Parse entire response as list of typed models."""
    print("\n" + "=" * 60)
    print("Example 7: Parsing List of Records")
    print("=" * 60)

    with BMRSClient(api_key=API_KEY) as client:
        today = date.today()
        yesterday = today - timedelta(days=1)

        raw_response = client.get_generation_by_fuel_type(
            from_date=yesterday,
            to_date=today
        )

        # Parse each record as a Pydantic model
        records = []
        for item in raw_response.get("data", [])[:5]:  # First 5 for demo
            try:
                # Use the GenerationByFuelType model
                typed_record = GenerationByFuelType(**item)
                records.append(typed_record)
            except Exception as e:
                print(f"Could not parse record: {e}")

        print(f"\n✓ Parsed {len(records)} generation records")
        for i, record in enumerate(records[:3], 1):
            print(f"\nRecord {i}:")
            print(f"  Date: {record.settlement_date}")
            print(f"  Period: {record.settlement_period}")
            if record.wind:
                print(f"  Wind: {record.wind} MW")
            if record.nuclear:
                print(f"  Nuclear: {record.nuclear} MW")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "Type-Safe BMRS Client Examples" + " " * 16 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\nNote: Replace API_KEY with your actual API key.\n")

    try:
        example_untyped_response()
        example_api_response_model()
        example_importing_generated_models()
        example_type_hints_with_models()
        example_validation_and_errors()
        example_model_with_config()
        example_parsing_list_of_models()

        print("\n" + "=" * 60)
        print("All type-safe examples completed!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Make sure you have set a valid API key.")

