import os
import random
import sys
import time
import uuid

import structlog
from business_logic import (
    simulate_authentication,
    simulate_data_analytics,
    simulate_file_upload,
    simulate_order_processing,
    simulate_user_registration,
)
from generator import (
    generate_log_type,
    generate_method_activity,
    generate_path_activity,
)
from log_config import setup_logging

setup_logging(log_level="DEBUG", enable_file_logs=False)
logger = structlog.get_logger()

NAME_APP = os.getenv("NAME_APP", "python-logger-demo")


def main():
    """Main loop that generates various log messages with UUIDs"""
    structlog.contextvars.bind_contextvars(app_name=NAME_APP)
    logger.info("Starting logging application")

    while True:
        # simulate user activity
        request_id = str(uuid.uuid4())
        path = generate_path_activity()
        method = generate_method_activity()

        # START of processing
        start_time = time.time()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=path,
            method=method,
        )

        # PROCESSING logic business with some various log messages, timesleep, error, success, etc.
        log_type = generate_log_type()

        # Simulate different business operations based on the path
        try:
            if "/users" in path:
                # Simulate user operations
                if method == "POST":
                    user_data = {
                        "username": f"user_{random.randint(1000, 9999)}",
                        "email": f"user{random.randint(1, 1000)}@example.com",
                    }
                    result = simulate_user_registration(user_data)
                    status_code = 201 if result["success"] else 400
                else:
                    logger.info(
                        "User data retrieved", user_count=random.randint(1, 100)
                    )
                    status_code = 200

            elif "/orders" in path:
                # Simulate order operations
                if method == "POST":
                    order_data = {
                        "order_id": random.randint(10000, 99999),
                        "user_id": random.randint(1000, 9999),
                        "amount": random.uniform(10.0, 500.0),
                        "product_id": random.randint(1, 200),
                        "payment_method": random.choice(
                            ["credit_card", "paypal", "bank_transfer"]
                        ),
                    }
                    result = simulate_order_processing(order_data)
                    status_code = 201 if result["success"] else 400
                else:
                    logger.info("Order data retrieved", order_id=path.split("/")[-1])
                    status_code = 200

            elif "/auth" in path:
                # Simulate authentication
                if "login" in path:
                    username = f"user_{random.randint(1, 1000)}"
                    password = "password123"
                    result = simulate_authentication(username, password)
                    status_code = 200 if result["success"] else 401
                elif "logout" in path:
                    logger.info("User logout", session_ended=True)
                    status_code = 200
                else:
                    logger.info("Token refresh", new_token_issued=True)
                    status_code = 200

            elif "/analytics" in path:
                # Simulate analytics queries
                query_type = random.choice(["simple", "complex", "medium"])
                result = simulate_data_analytics(query_type)
                status_code = 200

            elif "/files" in path:
                # Simulate file operations
                if method == "POST":
                    filename = f"document_{random.randint(1, 1000)}.pdf"
                    file_size = random.uniform(0.5, 150.0)
                    result = simulate_file_upload(filename, file_size)
                    status_code = 201 if result["success"] else 400
                else:
                    logger.info("File retrieved", file_id=path.split("/")[-1])
                    status_code = 200

            elif "/health" in path:
                # Health check - minimal logging
                if random.random() < 0.95:  # 95% healthy
                    logger.debug("Health check passed")
                    status_code = 200
                else:
                    logger.warning("Health check failed", component="database")
                    status_code = 503

            else:
                # Generic operations
                if log_type == "info":
                    logger.info("Operation completed successfully")
                    status_code = 200
                elif log_type == "warning":
                    logger.warning(
                        "Operation completed with warnings",
                        warning="deprecated_api",
                    )
                    status_code = 200
                elif log_type == "error":
                    logger.error(
                        "Operation failed",
                        error="internal_server_error",
                    )
                    status_code = 500
                else:  # debug
                    logger.debug("Debug information")
                    status_code = 200

            # Add status code to context for response logging
            structlog.contextvars.bind_contextvars(status_code=status_code)

        except Exception as e:
            logger.error(
                "Unexpected error in business logic",
                error=str(e),
                error_type=type(e).__name__,
            )
            status_code = 500
            structlog.contextvars.bind_contextvars(status_code=status_code)

        # Random delay to simulate processing time
        time.sleep(random.uniform(0.1, 2.0))

        # END of processing
        end_time = time.time()
        response_time_ms = int((end_time - start_time) * 1000)
        logger.info("Request completed", response_time_ms=response_time_ms)

        structlog.contextvars.unbind_contextvars(
            "request_id",
            "path",
            "method",
            "status_code",
        )
        # Add some variety in timing
        time.sleep(random.uniform(0.5, 3.0))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Application shutting down", reason="keyboard_interrupt")
        sys.exit(0)
    except Exception as e:
        logger.error("Unexpected error", error=str(e), error_type=type(e).__name__)
        sys.exit(1)
