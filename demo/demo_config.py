
import commons.Logger
from commons.Config import get_config
from commons.Logger import logger

# 跨脚本执行的时候，经常遇到的一个问题
# 找不到config.ini
# print(get_config('database'))
print(get_config('options.url'))

logger.info("测试日志位置")
