"""
Infer required fields by making actual API requests and analyzing responses.

This script tests various BMRS API endpoints to determine which fields
are consistently present (and therefore should be required).
"""

import json
import sys
from pathlib import Path
from typing import Dict, Set, List, Any
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from elexon_bmrs import BMRSClient


class RequiredFieldInferrer:
    """Infer required fields from actual API responses."""
    
    def __init__(self, api_key: str = None):
        """Initialize with optional API key."""
        self.client = BMRSClient(api_key=api_key)
        self.field_presence: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_responses: Dict[str, int] = defaultdict(int)
    
    def test_endpoint(self, endpoint_name: str, method_name: str, **kwargs) -> None:
        """
        Test an endpoint and record which fields are present.
        
        Args:
            endpoint_name: Name for tracking (e.g., 'abuc')
            method_name: Client method name (e.g., 'get_datasets_abuc')
            **kwargs: Parameters to pass to the method
        """
        try:
            print(f"Testing {endpoint_name}...", end=" ")
            method = getattr(self.client, method_name)
            response = method(**kwargs)
            
            if isinstance(response, dict) and 'data' in response:
                data_list = response['data']
                if data_list and isinstance(data_list, list):
                    # Analyze each row
                    for row in data_list[:10]:  # Sample first 10 rows
                        if isinstance(row, dict):
                            self.total_responses[endpoint_name] += 1
                            for field_name, field_value in row.items():
                                if field_value is not None:
                                    self.field_presence[endpoint_name][field_name] += 1
                    
                    print(f"✓ ({len(data_list)} rows)")
                else:
                    print("✗ (no data)")
            else:
                print("✗ (unexpected format)")
                
        except Exception as e:
            print(f"✗ ({str(e)[:50]})")
    
    def analyze_results(self) -> Dict[str, Set[str]]:
        """
        Analyze results to determine which fields should be required.
        
        Returns:
            Dictionary mapping endpoint names to sets of required field names
        """
        required_by_endpoint = {}
        
        for endpoint_name, field_counts in self.field_presence.items():
            total = self.total_responses[endpoint_name]
            if total == 0:
                continue
                
            # Fields present in 90%+ of responses should be required
            required_fields = set()
            for field_name, count in field_counts.items():
                presence_rate = count / total
                if presence_rate >= 0.9:  # 90% threshold
                    required_fields.add(field_name)
            
            required_by_endpoint[endpoint_name] = required_fields
        
        return required_by_endpoint
    
    def get_common_required_fields(self, required_by_endpoint: Dict[str, Set[str]]) -> Set[str]:
        """
        Get fields that are required across multiple endpoints.
        
        Args:
            required_by_endpoint: Results from analyze_results()
            
        Returns:
            Set of commonly required field names
        """
        field_frequency = defaultdict(int)
        
        for endpoint_fields in required_by_endpoint.values():
            for field in endpoint_fields:
                field_frequency[field] += 1
        
        # Fields required in 3+ endpoints are likely universally required
        common_required = {
            field for field, freq in field_frequency.items()
            if freq >= 3
        }
        
        return common_required


def main():
    """Main entry point."""
    print("\n╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "Required Field Inferrer" + " " * 31 + "║")
    print("╚" + "=" * 68 + "╝\n")
    
    print("This tool tests actual API endpoints to determine which fields")
    print("are consistently present and should be marked as required.\n")
    
    # Initialize inferrer
    inferrer = RequiredFieldInferrer()
    
    # Test various endpoints with recent data (last 7 days)
    from datetime import datetime, timedelta
    
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    
    start_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    start_date = start_time.strftime('%Y-%m-%d')
    end_date = end_time.strftime('%Y-%m-%d')
    
    print(f"Testing endpoints with data from {start_date} to {end_date}:\n")
    
    # Dataset endpoints
    inferrer.test_endpoint(
        'abuc', 'get_datasets_abuc',
        publishDateTimeFrom=start_str,
        publishDateTimeTo=end_str
    )
    
    inferrer.test_endpoint(
        'agpt', 'get_datasets_agpt',
        publishDateTimeFrom=start_str,
        publishDateTimeTo=end_str
    )
    
    inferrer.test_endpoint(
        'freq', 'get_datasets_freq',
        from_=start_str,
        to=end_str
    )
    
    inferrer.test_endpoint(
        'bod', 'get_datasets_bod',
        from_=start_str,
        to=end_str
    )
    
    inferrer.test_endpoint(
        'indod', 'get_datasets_indod',
        publishDateTimeFrom=start_str,
        publishDateTimeTo=end_str
    )
    
    inferrer.test_endpoint(
        'temp', 'get_datasets_temp',
        publishDateTimeFrom=start_str,
        publishDateTimeTo=end_str
    )
    
    # Analyze results
    print("\n" + "=" * 70)
    print("Analyzing field presence across endpoints...\n")
    
    required_by_endpoint = inferrer.analyze_results()
    
    # Print results per endpoint
    for endpoint_name, required_fields in sorted(required_by_endpoint.items()):
        print(f"\n{endpoint_name.upper()}:")
        print(f"  Required fields ({len(required_fields)}): {sorted(required_fields)}")
    
    # Get common required fields
    common_required = inferrer.get_common_required_fields(required_by_endpoint)
    
    print("\n" + "=" * 70)
    print(f"\nCOMMON REQUIRED FIELDS ({len(common_required)}):")
    print("These fields appear as required in 3+ endpoints:\n")
    for field in sorted(common_required):
        print(f"  - {field}")
    
    # Save results
    output_file = Path(__file__).parent / "inferred_required_fields.json"
    results = {
        'common_required_fields': sorted(common_required),
        'by_endpoint': {
            endpoint: sorted(fields)
            for endpoint, fields in required_by_endpoint.items()
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to: {output_file}")
    print("\nNext steps:")
    print("  1. Review the inferred required fields above")
    print("  2. Update tools/generate_models.py with these fields")
    print("  3. Regenerate models: python tools/generate_models.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

