# 每日汇报小助手 - DailyReportHelper

Weixin bot used for managing my daily report.

用于“自动”向特定的微信群发送文件，基于 [ItChat](https://github.com/littlecodersh/ItChat) 的，小而美的微信机器人。

## 使用方法

1. 点击网页上方绿色 `Code` 按钮，选择 `Download ZIP` 下载源码并解压。
2. 首次运行时，程序会生成默认 `config.yml` 配置文件并弹窗提示，
   
   用记事本或其他文本编辑器打开此文件，按照其中提示文字填写后保存。
   
   如填写有误，程序也会作相应弹窗提示。
3. 双击 `.bat` 后缀的文件，如果一切正常，小助手就应当开始运行，
    
   此时会提示你使用微信扫描程序窗口的二维码，完成登录微信的步骤。
4. 窗口中显示 `Start auto replying.` 即为登录成功，小助手就开始工作了。

## 功能

你在小助手上登录了自己的微信账号后：

1. 向“文件传输助手”发送下列关键词中任何一个：
   ```
   交作业, 交日报, 交汇报, 交每日作业, 交每日日报, 交每日汇报,
   发作业, 发日报, 发汇报, 发每日作业, 发每日日报, 发每日汇报
   ```
   那么小助手会从你指定的，存放待发送文件的文件夹中，找到那个名叫
   `今天的日期-每日汇报.pdf`
   的作业 pdf，发到你指定的那个群里，提交今天的每日汇报。
2. 向“文件传输助手”发送下列关键词中任何一个：
   ```
   补交作业, 补交日报, 补交汇报, 补交每日作业, 补交每日日报, 补交每日汇报,
   补发作业, 补发日报, 补发汇报, 补发每日作业, 补发每日日报, 补发每日汇报
   ```
   那么小助手会从你指定的，存放待发送文件的文件夹中，找到那个名叫
   `昨天的日期-每日汇报.pdf`
   的作业 pdf，发到你指定的那个群里，补交昨天的每日汇报。
3. 如果那个群里有其他同学发了文件（必须是发文件，文字、图片、红包等都不算），
   且发送时的时间不早于你指定的那个时间，
   那么小助手会从你指定的，存放待发送文件的文件夹中，找到那个名叫
   `今天的日期-每日汇报.pdf`
   的作业 pdf，发到你指定的那个群里。
4. 以上三个功能触发时，你没有写今天的每日汇报，导致小助手没有找到的话，
   小助手会向你发送一条提示图片，告诉你作业还没有写。