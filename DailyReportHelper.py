import itchat
from datetime import datetime
import pytz
from itchat.content import TEXT, ATTACHMENT

# CONSTS
# 放置每日汇报的文件夹
DAILY_REPORT_FOLDER = r'E:\Files and Documents\文档\硕士研究生文档\每日汇报\导出的PDF文档'
# 主动提交作业时，如果还没有写作业，那么发这张图作为提示
PROMPT_MYSELF = r'G:\DailyReportHelper\prompt_myself.png'
# 其他同学提交作业时，如果还没有写作业，那么发这张图作为提示
PROMPT_OTHERS = r'G:\DailyReportHelper\prompt_others.png'
# 将微信“文件传输助手”的 ID 写成字面常量
YOURSELF = "filehelper"
# 目标群聊的名称
TARGET_GROUP = "文件暂存群"

# Login
itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir='itchat.pkl')


# Work Logic
# 主动交作业
@itchat.msg_register(TEXT)
def upload_files_by_myself(msg):
    if msg["ToUserName"] == YOURSELF and msg["Text"] in ["交作业", "交日报", "交汇报", "交每日作业", "交每日日报", "交每日汇报"]:
        path = (DAILY_REPORT_FOLDER + '\\' +  # 文件夹路径
                # 文件名规范：4位年2位月2位日-每日汇报.pdf
                datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y%m%d') + "-每日汇报.pdf")
        try:
            test = open(path)
            test.close()
            itchat.send('@fil@%s' % path, YOURSELF)
        except FileNotFoundError:
            itchat.send('@img@%s' % PROMPT_MYSELF, YOURSELF)


# TODO: 晚上八点以后，如果教研室群有除了自己以外的人发送了附件，那么自动交作业
@itchat.msg_register(ATTACHMENT, isGroupChat=True)
def upload_files_when_prompted(msg):
    if msg["User"]["NickName"] == TARGET_GROUP:
        if (datetime.now(pytz.timezone('Asia/Shanghai')).hour >= 20 or
                datetime.now(pytz.timezone('Asia/Shanghai')).hour <= 3):
            itchat.get_chatrooms(update=True)
            target_group = itchat.search_chatrooms(name=TARGET_GROUP)
            if target_group is not None:
                itchat.send("没有找到这个群聊", YOURSELF)


itchat.run()
