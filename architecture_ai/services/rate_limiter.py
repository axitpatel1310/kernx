import redis

from django.conf import settings


ANALYSIS_LIMIT = 9
WINDOW_SECONDS = 3 * 60 * 60


redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


def check_analysis_limit(user_id):
    """
    Allow 9 architecture analyses every 3 hours.
    """

    key = f"kernx:analysis_limit:{user_id}"

    current_count = redis_client.get(key)

    if current_count is not None:
        current_count = int(current_count)

        if current_count >= ANALYSIS_LIMIT:
            ttl = redis_client.ttl(key)

            return {
                "allowed": False,
                "remaining": 0,
                "reset_in": max(ttl, 0),
            }

    # Atomically increment
    count = redis_client.incr(key)

    # First request starts the 3-hour window
    if count == 1:
        redis_client.expire(
            key,
            WINDOW_SECONDS,
        )

    return {
        "allowed": True,
        "remaining": ANALYSIS_LIMIT - count,
        "reset_in": redis_client.ttl(key),
    }