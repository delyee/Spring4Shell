from multiprocessing import cpu_count

REDIS_SERVER_URL = "redis://:password@redis.mdamda.com"
REDIS_SERVER_DB = 0
ERROR_LOG = "error.log"

NUM_CPU_CORES = cpu_count() * 3
NUM_COROS = 4