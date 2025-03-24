import redis
from config import Config


redis_user = redis.Redis.from_url(f"{Config.REDIS_URL}/{Config.REDIS_USER_DB}", decode_responses=True)
redis_user_payment = redis.Redis.from_url(f"{Config.REDIS_URL}/{Config.REDIS_USER_PAYMENT_DB}", decode_responses=True)
redis_admin = redis.Redis.from_url(f"{Config.REDIS_URL}/{Config.REDIS_ADMIN_DB}", decode_responses=True)
redis_musician = redis.Redis.from_url(f"{Config.REDIS_URL}/{Config.REDIS_MUSICIAN_DB}", decode_responses=True)
redis_musician_payment = redis.Redis.from_url(f"{Config.REDIS_URL}/{Config.REDIS_MUSICIAN_PAYMENT_DB}", decode_response=True)
