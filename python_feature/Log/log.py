from loguru import logger

path = "./test.log"

# rotation - 分割大小
# retention - 留存索引
# compression - 压缩方式 zip tar gz
# serialize - 序列化保存文件
logger.add(path, rotation="200KB", compression="zip", retention=1, serialize=True)
logger.remove(0)  # 移除标准输出, 不在控制台打印

logger.debug("debug")
logger.info("hello")
logger.warning("warning")
logger.critical("critical")