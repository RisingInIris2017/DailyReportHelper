from datetime import datetime
import yaml
import itchat
import pytz
from os.path import abspath
from sys import exit
import win32api
import win32con
from itchat.content import TEXT, ATTACHMENT

# CONSTS
# 配置文件的路径
CONFIG_PATH = abspath(r'.\config.yml')
# 程序常量
# 主动提交作业时，如果还没有写作业，那么发这张图作为提示
PROMPT_MYSELF = abspath(r'.\prompt_myself.png')
# 其他同学提交作业时，如果还没有写作业，那么发这张图作为提示
PROMPT_OTHERS = abspath(r'.\prompt_others.png')
# 将微信“文件传输助手”的 ID 写成字面常量
YOURSELF = "filehelper"


# 专门用于发送提示的函数
def hint(text: str, msgbox_title: str):
    print(msgbox_title + ": " + text)
    itchat.send(text, YOURSELF)
    win32api.MessageBox(0, text, msgbox_title, win32con.MB_OK)


# 读取配置文件
try:
    config_file = open(CONFIG_PATH, 'r', encoding='utf-8')
    config = yaml.load(config_file, Loader=yaml.FullLoader)
    DAILY_REPORT_FOLDER = config["DAILY_REPORT_FOLDER"]
    TARGET_GROUP = config["TARGET_GROUP"]
    NOT_EARLY_BEFORE = config["NOT_EARLY_BEFORE"]
    # 将字符串值表示的时间解析为整数列表
    time = [int(num) for num in NOT_EARLY_BEFORE.split(":")]
except FileNotFoundError:
    default_config = open(CONFIG_PATH, 'w', encoding='utf-8')
    default_config.write("""
DAILY_REPORT_FOLDER: '填入你放置这些文件的文件夹绝对路径'\n
TARGET_GROUP: '要发送文件的群聊名称'\n
NOT_EARLY_BEFORE: '24小时格式的时间，被动发送文件不会早于这个时间'\n
""")
    hint("默认config.yml配置文件已生成，\n请按照其中提示文字填写后使用")
    itchat.logout()
    exit()


def display_welcome():
    print("每日汇报小助手已成功登录。")
    print("以下是本次启动时，小助手的设置信息，请确认设置无误：")
    print("放置每日汇报文件的目录：%s" % DAILY_REPORT_FOLDER)
    print("待发送每日汇报的群名：%s" % TARGET_GROUP)
    print("小助手将在今天%s之后，自动从上述目录中找到今日汇报发送入群。" % NOT_EARLY_BEFORE)


# 机器人登录
itchat.auto_login(loginCallback=display_welcome, enableCmdQR=2, hotReload=True, statusStorageDir='itchat.pkl')


# 提取该消息所在群聊的群用户名，它是一串类似哈希、随时改变的 string，
# 用于传入 send() 方法的第二个参数
def get_target_group_username(msg, working_mode):
    # 主动交作业和群聊触发交作业这两种场景下，msg 字典的结构不同
    # 由 working_mode 参数控制，切换两种不同的工作逻辑来寻找指定的群聊信息
    if working_mode == "myself":
        search_result = itchat.search_chatrooms(name=TARGET_GROUP)
        if search_result is None:
            hint("未找到指定群聊，请检查程序错误", "每日汇报小助手提醒")
            return False, ""
        else:
            return True, search_result[0]["UserName"]
    elif working_mode == "others":
        # 提取微信群聊信息的 User 键，
        # 从这里可以拿到群聊的显示名 NickName，用于判断是否是我们要的那个群
        # 如果是，从这个键拿到该群的用户名
        dict_usr = msg["User"]
        # 取群聊昵称，判断
        target_group_nickname = dict_usr["NickName"]
        if target_group_nickname == TARGET_GROUP:  # 若命中我们需要的群
            return True, dict_usr["UserName"]  # 提取群用户名
        else:
            return False, ""
    else:
        hint("无效的工作模式参数，无法获取群聊信息", "每日汇报小助手提醒")
        return False, ""


def send_file(target_group_user_name, working_mode):
    path = (DAILY_REPORT_FOLDER + '\\' +  # 文件夹路径
            # 文件名规范：4位年2位月2位日-每日汇报.pdf
            datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d') + "-每日汇报.pdf")
    try:
        test = open(path)
        test.close()
        itchat.send('@fil@%s' % path, target_group_user_name)
        hint("已将文件发送到指定的群：%s" % TARGET_GROUP, "每日汇报小助手-发送成功")
    except FileNotFoundError:
        image_path = PROMPT_MYSELF if (working_mode == "myself") else PROMPT_OTHERS
        itchat.send('@img@%s' % image_path, YOURSELF)


# Work Logic
# 手动触发：主动交作业
@itchat.msg_register(TEXT)
def upload_files_by_myself(msg):
    if msg["ToUserName"] == YOURSELF and msg["Text"] in [
        "交作业", "交日报", "交汇报", "交每日作业", "交每日日报", "交每日汇报",
        "发作业", "发日报", "发汇报", "发每日作业", "发每日日报", "发每日汇报"
    ]:
        get_target_group = get_target_group_username(msg, "myself")
        if get_target_group[0]:  # Flag 为真，表示拿到了目标群聊
            send_file(get_target_group[1], "myself")
        else:
            hint("未找到目标群聊，请检查程序问题", "每日汇报小助手提醒")


# 被动触发：晚上八点以后，如果教研室群有除了自己以外的人发送了附件，那么自动交作业
@itchat.msg_register(ATTACHMENT, isGroupChat=True)
def upload_files_when_prompted(msg):
    current_time = [
        datetime.now(pytz.timezone('Asia/Shanghai')).hour,
        datetime.now(pytz.timezone('Asia/Shanghai')).minute
    ]
    if current_time[0] >= (time[0] + 1) or (current_time[1] >= time[1] and current_time[0] >= time[0]):
        get_target_group = get_target_group_username(msg, "others")
        if get_target_group[0]:
            send_file(get_target_group[1], "others")
        else:
            hint("未找到目标群聊，请检查程序问题", "每日汇报小助手提醒")
    else:
        prompt = "当前时间%s:%s未达到设定时间%s，暂不发送今日汇报" % (
            str(current_time[0]) if len(str(current_time[0])) == 2 else ("0" + str(current_time[0])),
            str(current_time[1]) if len(str(current_time[1])) == 2 else ("0" + str(current_time[1])),
            NOT_EARLY_BEFORE
        )
        hint(prompt, "每日汇报小助手提醒")


itchat.run()
