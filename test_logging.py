#!/usr/bin/env python3
"""
Test script to validate logging configuration
Run this to test if structlog is working correctly before running the full application
"""

import os
import sys

# Add app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

import structlog
from business_logic import (
    simulate_authentication,
    simulate_data_analytics,
    simulate_file_upload,
    simulate_order_processing,
    simulate_user_registration,
)
from log_config import setup_logging


def test_logging_setup():
    """Test basic logging configuration"""
    print("🧪 Testing logging configuration...")

    # Setup logging with file output for testing
    setup_logging(log_level="DEBUG", enable_file_logs=True, log_file="logs/test.log")

    logger = structlog.get_logger(__name__)

    # Test basic logging
    logger.info("Testing basic structured logging", test_id="LOG001")
    logger.warning("Testing warning level", test_id="LOG002", component="test")
    logger.error("Testing error level", test_id="LOG003", error_code="TEST_ERROR")
    logger.debug("Testing debug level", test_id="LOG004", details="verbose_info")

    print("✅ Basic logging test completed")


def test_business_logic():
    """Test business logic functions"""
    print("🧪 Testing business logic simulations...")

    logger = structlog.get_logger(__name__)

    # Test user registration
    user_data = {"username": "test_user", "email": "test@example.com"}
    result = simulate_user_registration(user_data)
    logger.info("User registration test", result=result)

    # Test order processing
    order_data = {
        "order_id": 12345,
        "user_id": 1001,
        "amount": 99.99,
        "product_id": 501,
        "payment_method": "credit_card",
    }
    result = simulate_order_processing(order_data)
    logger.info("Order processing test", result=result)

    # Test authentication
    result = simulate_authentication("test_user", "password123")
    logger.info("Authentication test", result=result)

    # Test analytics
    result = simulate_data_analytics("simple")
    logger.info("Analytics test", result=result)

    # Test file upload
    result = simulate_file_upload("test_document.pdf", 5.2)
    logger.info("File upload test", result=result)

    print("✅ Business logic test completed")


def test_structured_data():
    """Test complex structured data logging"""
    print("🧪 Testing structured data logging...")

    logger = structlog.get_logger(__name__)

    # Test with complex data structures
    complex_data = {
        "user_profile": {
            "user_id": 12345,
            "preferences": ["email", "sms"],
            "settings": {"theme": "dark", "notifications": True},
        },
        "transaction": {
            "amount": 150.75,
            "currency": "USD",
            "items": [
                {"id": 1, "name": "Product A", "qty": 2},
                {"id": 2, "name": "Product B", "qty": 1},
            ],
        },
        "metadata": {"source": "mobile_app", "version": "2.1.0", "platform": "ios"},
    }

    logger.info("Complex structured data test", **complex_data)

    # Test sensitive data masking
    sensitive_data = {
        "username": "test_user",
        "password": "secret123",
        "api_key": "sk_test_123456",
        "email": "user@example.com",
        "credit_card": "4111-1111-1111-1111",
    }

    logger.info("Sensitive data masking test", **sensitive_data)

    print("✅ Structured data test completed")


if __name__ == "__main__":
    print("🚀 Starting logging tests...")
    print("=" * 50)

    try:
        test_logging_setup()
        test_business_logic()
        test_structured_data()

        print("=" * 50)
        print("🎉 All tests completed successfully!")
        print("📂 Check logs/test.log for output")
        print("💡 Now run: docker-compose up --build")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
