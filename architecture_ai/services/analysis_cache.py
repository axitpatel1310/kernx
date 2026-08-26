import hashlib
import json

import redis

from django.conf import settings


CACHE_TTL = 24 * 60 * 60  # 24 hours


redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)


def architecture_hash(data):
    """
    Generate a deterministic hash for an architecture.
    """

    serialized = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()


def get_cached_analysis(data):
    """
    Return cached analysis if available.
    """

    key = f"kernx:analysis:{architecture_hash(data)}"

    return redis_client.get(key)


def cache_analysis(data, result):
    """
    Store architecture analysis in Redis.
    """

    key = f"kernx:analysis:{architecture_hash(data)}"

    redis_client.setex(
        key,
        CACHE_TTL,
        result,
    )