import logging

# 要选择性删除的文件地址
file_path = "devicLogInfo.log"

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler("devicLogInfo.log", encoding="GBK")
fh.setLevel(logging.DEBUG)

# 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)


"""
    nodeID:节点设备的ID
    UserID:用户ID
    flag:标志位，0表示设备主动下线。1表示主动上线，2表示异常掉线
"""
# 定义输出函数，在控制台打印输出 & 本地生成相应日志deviceInfo.log
def node_log_Saved(UserID, nodeID, flag):
    # 设置日志格式
    formatter = logging.Formatter(
        "%(asctime)s - 操作用户：" + str(UserID) + " - 设备：" + str(nodeID) + " - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    # 设置控制台、log本地文件输出格式，并将方法绑定至logger。
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

    if flag == 0:
        logger.info("设备已下线")

    elif flag == 1:
        logger.info("设备已上线")

    else:
        logger.warning("设备非正常下线")


# 删除某个节点的历史数据信息
def node_log_Delete(UserID, nodeID):
    global delete_Flag
    delete_Flag = 0
    with open(file_path, 'r') as f:
        lines = f.readlines()
    with open(file_path, 'w') as f:
        for line in lines:
            if " - 设备：" + nodeID not in line:
                f.write(line)
            else:
                delete_Flag = 1
        if delete_Flag == 1:
            logger.info("用户：%s 已删除设备：%s 的上下限消息记录！" % (UserID, nodeID))
