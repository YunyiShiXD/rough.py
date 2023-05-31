import socket
import time

"""
    # 服务器端：IPV4,TCP协议
    # 调用后将socket通信，主机作为客户端，不断尝试连接服务端接收数据   
        参数定义
            Host:服务端IP地址
            port:服务端端口号
            RetryInterval:重新尝试连接的间隔时间
"""
def socket_TCP_Client(Host, Port, RetryInterval):
    while True:
        try:
            # 尝试连接服务端
            conn = socket.create_connection((Host, Port))
            # 如果连接成功，则输出提示信息
            print('成功连接到服务器')
            # 接收数据并输出到控制台
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f'收到数据：{data.decode()}')
            # 不关闭连接，继续接收数据
        except ConnectionRefusedError:
            # 如果连接被拒绝，则输出错误提示信息
            print('无法连接到服务器，请检查服务端是否处于运行状态')
        finally:
            # 等待一段时间后再次尝试连接
            time.sleep(RetryInterval)