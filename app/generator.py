import random


def generate_log_type():
    return random.choice(["info", "warning", "error", "debug"])


def generate_method_activity():
    return random.choice(["GET", "POST", "PUT", "DELETE"])


def generate_path_activity():
    return random.choice(
        [
            f"/api/v1/users/{random.randint(1, 1000)}",
            f"/api/v1/orders/{random.randint(1, 5000)}",
            f"/api/v1/products/{random.randint(1, 200)}",
            "/api/v1/auth/login",
            "/api/v1/auth/logout",
            "/api/v1/auth/refresh",
            f"/api/v1/categories/{random.randint(1, 50)}",
            "/api/v1/search",
            "/healthz",
            f"/api/v1/files/{random.randint(1, 10000)}",
            f"/api/v1/reports/{random.randint(1, 100)}",
            "/api/v1/settings",
            f"/api/v1/notifications/{random.randint(1, 1000)}",
            "/api/v1/dashboard",
            f"/api/v1/analytics/{random.choice(['daily', 'weekly', 'monthly'])}",
        ]
    )

    # Optional: limit loops for testing (remove in production)
    # if loop_count > 100:
    #     logger.info("Completed test run", total_requests=loop_count)
    #     break
