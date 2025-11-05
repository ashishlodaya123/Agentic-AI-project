#!/usr/bin/env python3

import requests
import time

def test_metrics():
    """Test that metrics are being collected and exposed."""
    try:
        # Test the main endpoint to generate some metrics
        response = requests.get("http://127.0.0.1:8000/")
        print(f"Root endpoint status: {response.status_code}")
        
        # Wait a moment for metrics to be collected
        time.sleep(1)
        
        # Test the metrics endpoint
        metrics_response = requests.get("http://127.0.0.1:8000/metrics")
        print(f"Metrics endpoint status: {metrics_response.status_code}")
        print(f"Metrics content type: {metrics_response.headers.get('content-type')}")
        
        if metrics_response.status_code == 200:
            metrics_text = metrics_response.text
            print("Sample of metrics data:")
            # Print first 10 lines of metrics
            lines = metrics_text.split('\n')
            for line in lines[:10]:
                if line and not line.startswith('#'):
                    print(f"  {line}")
            
            # Check for specific metrics
            if 'http_requests_total' in metrics_text:
                print("✓ http_requests_total metric found")
            else:
                print("✗ http_requests_total metric not found")
                
            if 'triage_requests_total' in metrics_text:
                print("✓ triage_requests_total metric found")
            else:
                print("✗ triage_requests_total metric not found")
                
        else:
            print(f"Error fetching metrics: {metrics_response.text}")
            
    except Exception as e:
        print(f"Error testing metrics: {e}")

if __name__ == "__main__":
    test_metrics()