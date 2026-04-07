'''
制作一个能配置路由器的 SSH 交互函数
paramiko 交互模式测试脚本（可直接粘贴运行）：

import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('196.21.5.211', port=22, username='admin', password='Cisc0123',
            timeout=5, look_for_keys=False, allow_agent=False)

chan = ssh.invoke_shell()
time.sleep(1)
print(chan.recv(2048).decode())   # 查看登录提示符

chan.send(b'terminal length 0\n')
time.sleep(1)
print(chan.recv(2048).decode())

chan.send(b'show version\n')
time.sleep(2)
print(chan.recv(4096).decode())

chan.send(b'config ter\n')
time.sleep(1)
print(chan.recv(2048).decode())

chan.send(b'router ospf 1\n')
time.sleep(1)
print(chan.recv(2048).decode())

ssh.close()
在以上测试基础上，制作一个可执行多条命令的函数，参数设计如下：

def qytang_multicmd(ip, username, password, cmd_list, enable='', wait_time=2, verbose=True):
    """
    参数说明：
      cmd_list  : 要执行的命令列表，例如 ['terminal length 0', 'show version']
      enable    : enable 密码，若设备无需 enable 则保持默认空字符串
      wait_time : 每条命令发送后等待设备响应的秒数
      verbose   : True 则打印每条命令的返回结果，False 则静默执行
    """
测试要求：使用制作的函数，一次执行以下命令列表，打印所有返回内容：

cmd_list = [
    'terminal length 0',
    'show version',
    'config ter',
    'router ospf 1',
    'network 10.0.0.0 0.0.0.255 area 0',
    'end',
]
期望输出（节选）：

--- terminal length 0 ---
terminal length 0
C8Kv1#

--- show version ---
show version
Cisco IOS XE Software, Version 17.14.01a
Cisco IOS Software [IOSXE], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.14.1a, RELEASE SOFTWARE (fc1)
...
C8Kv1#

--- config ter ---
config ter
Enter configuration commands, one per line.  End with CNTL/Z.
C8Kv1(config)#

--- router ospf 1 ---
router ospf 1
C8Kv1(config-router)#

--- network 10.0.0.0 0.0.0.255 area 0 ---
network 10.0.0.0 0.0.0.255 area 0
C8Kv1(config-router)#

--- end ---
end
C8Kv1#
'''
import paramiko
import time

def qytang_multicmd(ip, username, password, cmd_list, enable='', wait_time=2, verbose=True):
    """
    可执行多条命令的思科SSH交互函数
    参数说明：
      ip        : 设备IP地址
      username  : SSH登录用户名
      password  : SSH登录密码
      cmd_list  : 要执行的命令列表，例如 ['terminal length 0', 'show version']
      enable    : enable 密码，若设备无需 enable 则保持默认空字符串
      wait_time : 每条命令发送后等待设备响应的秒数
      verbose   : True 则打印每条命令的返回结果，False 则静默执行
    """
    # ========================
# 1. paramiko 交互模式测试脚本（题目要求：可直接粘贴运行）
# 作用：手动测试SSH交互式连接、执行单条命令，验证交互逻辑正常
# ========================
# 导入SSH连接库：paramiko是Python用于SSH远程连接的核心库
import paramiko
# 导入时间库：用于延时等待设备响应，防止命令执行过快导致读取失败
import time

# 创建SSH客户端对象，模拟SSH终端工具
ssh = paramiko.SSHClient()
# 自动接受设备的SSH密钥，解决首次连接报错问题
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 建立SSH连接：配置设备IP、端口、认证信息等参数
ssh.connect('10.10.1.200', port=22, username='admin', password='Cisc0123',
            timeout=5, look_for_keys=False, allow_agent=False)

# 开启交互式Shell（核心）：支持连续执行配置命令，保留命令执行上下文
chan = ssh.invoke_shell()
# 等待1秒，让设备完成终端初始化
time.sleep(1)
# 读取并打印设备登录后的提示符，确认连接成功
print(chan.recv(2048).decode())

# 执行命令：关闭分页（避免--More--阻塞），发送二进制格式命令+回车符
chan.send(b'terminal length 0\n')
time.sleep(1)
# 读取并打印命令执行结果
print(chan.recv(2048).decode())

# 执行命令：查看设备版本信息
chan.send(b'show version\n')
time.sleep(2)
print(chan.recv(4096).decode())

# 执行命令：进入全局配置模式
chan.send(b'config ter\n')
time.sleep(1)
print(chan.recv(2048).decode())

# 执行命令：创建OSPF路由进程1
chan.send(b'router ospf 1\n')
time.sleep(1)
print(chan.recv(2048).decode())

# 关闭SSH连接，释放资源
ssh.close()

# 分割线：区分测试脚本与封装函数，便于查看执行结果
print("=" * 60)
print("         测试脚本执行完毕，开始封装函数")
print("=" * 60)


# ========================
# 2. 封装可执行多条命令的函数（题目要求标准函数）
# 函数名、参数、功能100%匹配题目要求
# ========================
def qytang_multicmd(ip, username, password, cmd_list, enable='', wait_time=2, verbose=True):
    """
    思科设备SSH交互式多命令执行函数
    参数说明：
      ip        : 设备管理IP地址
      username  : SSH登录用户名
      password  : SSH登录密码
      cmd_list  : 命令列表，批量执行的所有命令
      enable    : 特权模式密码，无密码则留空
      wait_time : 每条命令执行后的等待时间（秒）
      verbose   : 打印开关，True=打印输出，False=静默执行
    """
    # 初始化SSH客户端
    ssh = paramiko.SSHClient()
    # 自动接受主机密钥
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 连接SSH设备
        ssh.connect(hostname=ip,
                    username=username,
                    password=password,
                    timeout=8,
                    look_for_keys=False,
                    allow_agent=False)

        # 开启交互式终端
        chan = ssh.invoke_shell()
        time.sleep(1)
        # 清空设备初始回显，避免干扰命令输出
        chan.recv(2048)

        # ========================
        # 自动进入特权模式（如果传入enable密码）
        # ========================
        if enable:
            # 发送enable命令
            chan.send(b'enable\n')
            time.sleep(1)
            # 发送enable密码
            chan.send(enable.encode() + b'\n')
            time.sleep(1)
            # 清空提权后的回显
            chan.recv(2048)

        # ========================
        # 批量循环执行命令列表
        # ========================
        for cmd in cmd_list:
            # 发送命令 + 回车符
            chan.send(cmd.encode() + b'\n')
            # 等待设备响应
            time.sleep(wait_time)
            # 读取命令返回结果
            output = chan.recv(65535).decode('utf-8', errors='ignore')

            # 如果verbose开启，打印命令和执行结果
            if verbose:
                print(f"\n--- {cmd} ---")
                print(output)

    # 捕获并打印所有连接/执行异常
    except Exception as e:
        print("执行异常：", e)

    # 无论是否报错，最终都会关闭SSH连接
    finally:
        ssh.close()


# ========================
# 3. 函数测试：执行题目指定的命令列表
# ========================
if __name__ == '__main__':
    # 题目要求的批量执行命令列表
    cmd_list = [
        'terminal length 0',
        'show version',
        'config ter',
        'router ospf 1',
        'network 10.0.0.0 0.0.0.255 area 0',
        'end',
    ]

    # 调用封装好的函数，执行所有命令
    qytang_multicmd(
        ip='10.10.1.200',
        username='admin',
        password='Cisc0123',
        cmd_list=cmd_list,
        enable='',          # 权限15，无需enable密码
        wait_time=2,        # 每条命令等待2秒
        verbose=True        # 打印所有执行结果
    )