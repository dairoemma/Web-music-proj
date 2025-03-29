import redis
from config import Config 

# important comment
# we planned on using redis, but i deployed a redis on upstash and upstash doesn't support differnt db instance only db 0 can be used
# we commented the codes and used just redis client but we failed to make use of redis in the program because for some reasons the data we added to the redis where not present 

# redis_user = redis.Redis.from_url(f"{Config.REDIS_URL}/{Config.REDIS_USER_DB}", decode_responses=True)
# redis_user_payment = redis.Redis.from_url(f"{Config.REDIS_URL}/{Config.REDIS_USER_PAYMENT_DB}", decode_responses=True)
# redis_admin = redis.Redis.from_url(f"{Config.REDIS_URL}/{Config.REDIS_ADMIN_DB}", decode_responses=True)
# redis_musician = redis.Redis.from_url(f"{Config.REDIS_URL}/{Config.REDIS_MUSICIAN_DB}", decode_responses=True)
# redis_musician_payment = redis.Redis.from_url(f"{Config.REDIS_URL}/{Config.REDIS_MUSICIAN_PAYMENT_DB}", decode_responses=True)

redis_client = redis.Redis.from_url(Config.REDIS_URL, decode_responses=True)

