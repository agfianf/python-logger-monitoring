import random
import time
from typing import Any, Dict

import structlog

logger = structlog.get_logger(__name__)


def simulate_user_registration(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate user registration process with logging"""
    logger.info("Starting user registration", username=user_data.get("username"))

    # Simulate validation
    time.sleep(random.uniform(0.1, 0.3))
    if random.random() < 0.1:  # 10% chance of validation error
        logger.warning(
            "User registration validation failed",
            reason="invalid_email",
            email=user_data.get("email"),
        )
        return {"success": False, "error": "Invalid email format"}

    # Simulate database operation
    time.sleep(random.uniform(0.2, 0.5))
    if random.random() < 0.05:  # 5% chance of database error
        logger.error(
            "Database error during user registration",
            error="connection_timeout",
            operation="user_insert",
        )
        return {"success": False, "error": "Database unavailable"}

    user_id = random.randint(1000, 9999)
    logger.info(
        "User registration successful",
        user_id=user_id,
        username=user_data.get("username"),
    )

    return {"success": True, "user_id": user_id}


def simulate_order_processing(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate order processing with comprehensive logging"""
    order_id = order_data.get("order_id", random.randint(10000, 99999))
    user_id = order_data.get("user_id", random.randint(1000, 9999))
    amount = order_data.get("amount", random.uniform(10.0, 500.0))

    logger.info(
        "Processing order", order_id=order_id, user_id=user_id, amount=round(amount, 2)
    )

    # Simulate inventory check
    time.sleep(random.uniform(0.1, 0.2))
    if random.random() < 0.15:  # 15% chance of inventory issue
        logger.warning(
            "Insufficient inventory",
            order_id=order_id,
            product_id=order_data.get("product_id", 123),
        )
        return {"success": False, "error": "Insufficient stock"}

    # Simulate payment processing
    time.sleep(random.uniform(0.3, 0.8))
    if random.random() < 0.08:  # 8% chance of payment failure
        logger.error(
            "Payment processing failed",
            order_id=order_id,
            payment_method=order_data.get("payment_method", "credit_card"),
            error_code="PAYMENT_DECLINED",
        )
        return {"success": False, "error": "Payment declined"}

    # Simulate shipping calculation
    time.sleep(random.uniform(0.1, 0.3))
    shipping_cost = random.uniform(5.0, 25.0)

    logger.info(
        "Order processed successfully",
        order_id=order_id,
        user_id=user_id,
        total_amount=round(amount + shipping_cost, 2),
        shipping_cost=round(shipping_cost, 2),
        status="confirmed",
    )

    return {
        "success": True,
        "order_id": order_id,
        "total_amount": round(amount + shipping_cost, 2),
    }


def simulate_data_analytics(query_type: str) -> Dict[str, Any]:
    """Simulate data analytics operations with performance logging"""
    logger.info("Starting analytics query", query_type=query_type)

    start_time = time.time()

    # Simulate different query complexities
    if query_type == "simple":
        time.sleep(random.uniform(0.1, 0.3))
        records_processed = random.randint(100, 1000)
    elif query_type == "complex":
        time.sleep(random.uniform(1.0, 3.0))
        records_processed = random.randint(10000, 100000)

        # Simulate memory usage warning for large queries
        if records_processed > 50000:
            logger.warning(
                "High memory usage detected",
                records_processed=records_processed,
                memory_usage_mb=random.randint(512, 1024),
            )
    else:
        time.sleep(random.uniform(0.5, 1.5))
        records_processed = random.randint(1000, 10000)

    end_time = time.time()
    processing_time = round((end_time - start_time) * 1000, 2)

    # Simulate occasional query optimization suggestions
    if processing_time > 2000:
        logger.warning(
            "Slow query detected",
            query_type=query_type,
            processing_time_ms=processing_time,
            suggestion="consider_adding_index",
        )

    logger.info(
        "Analytics query completed",
        query_type=query_type,
        records_processed=records_processed,
        processing_time_ms=processing_time,
    )

    return {
        "success": True,
        "records_processed": records_processed,
        "processing_time_ms": processing_time,
    }


def simulate_authentication(username: str, password: str) -> Dict[str, Any]:
    """Simulate user authentication with security logging"""
    logger.info("Authentication attempt", username=username)

    # Simulate authentication delay
    time.sleep(random.uniform(0.2, 0.5))

    # Simulate different authentication scenarios
    auth_result = random.choices(
        ["success", "invalid_password", "user_not_found", "account_locked"],
        weights=[70, 20, 5, 5],
    )[0]

    if auth_result == "success":
        session_id = f"sess_{random.randint(100000, 999999)}"
        logger.info(
            "Authentication successful", username=username, session_id=session_id
        )
        return {"success": True, "session_id": session_id}

    elif auth_result == "invalid_password":
        logger.warning(
            "Authentication failed",
            username=username,
            reason="invalid_password",
            attempt_count=random.randint(1, 3),
        )
        return {"success": False, "error": "Invalid credentials"}

    elif auth_result == "user_not_found":
        logger.warning(
            "Authentication failed", username=username, reason="user_not_found"
        )
        return {"success": False, "error": "User not found"}

    else:  # account_locked
        logger.error(
            "Authentication blocked",
            username=username,
            reason="account_locked",
            security_alert=True,
        )
        return {"success": False, "error": "Account locked"}


def simulate_file_upload(filename: str, file_size_mb: float) -> Dict[str, Any]:
    """Simulate file upload process with progress logging"""
    file_id = f"file_{random.randint(100000, 999999)}"

    logger.info(
        "File upload started",
        filename=filename,
        file_size_mb=file_size_mb,
        file_id=file_id,
    )

    # Simulate upload validation
    if file_size_mb > 100:
        logger.error(
            "File upload rejected",
            filename=filename,
            file_size_mb=file_size_mb,
            reason="file_too_large",
            max_size_mb=100,
        )
        return {"success": False, "error": "File too large"}

    # Simulate upload process with progress
    upload_time = file_size_mb * random.uniform(0.1, 0.3)
    time.sleep(upload_time)

    # Simulate virus scan
    time.sleep(random.uniform(0.2, 0.5))
    if random.random() < 0.02:  # 2% chance of virus detection
        logger.error(
            "File upload blocked",
            filename=filename,
            file_id=file_id,
            reason="virus_detected",
            security_alert=True,
        )
        return {"success": False, "error": "File contains malware"}

    logger.info(
        "File upload completed",
        filename=filename,
        file_id=file_id,
        upload_time_sec=round(upload_time, 2),
        status="stored",
    )

    return {"success": True, "file_id": file_id}
