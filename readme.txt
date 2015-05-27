These scripts is the first version,so the whole process may be not effective.
And I'm sorry about the trouble because of my poor English.

step 1.
start genymotion emulator (Google Nexus Android 4.3)

启动模拟器

step 2.
start appium

Note:appium is not stable always,if the driver program cant work, restart appium.

启动appium，有时可能会因为过程终止而导致appium出错，重启即可。

step 3.
start driver program : driver-measure.py
driver-measure.py will drive CNN app to click the news automatically five times,
result will be saved in /home/ramsey/mitmproxy-result/0 or .../1 and so on.
each directory include the http request log,and screenshot of genymotion.
during the process of opening news,
it will delay and log the http request one by one,and take a screenshot before the each request send.
it's done by the script app-mitm.py(for the mitmproxy).
In the log file,it also logs the similar value of different screenshot.
each request will have one similar value,if the value is small,it represent this request will make the app change.

Note: it will take lots of time to drive the app.
please make sure the window of genymotion always on the top during using.
create the directory mitmproxy-result before starting it,and make sure it's empty

启动驱动程序driver-measure.py
将会对cnn新闻做5次测试，结果保存在/home/ramsey/mitmproxy-result/0 或.../1等等中。
每次结果文件包含记录和截图，截图在每个url发送前截取，并于之前的截图比较。
记录中包含了每个url的详细内容，以及他造成了app的变化程度，越小的值将会造成越大的变化

过程中因为要根据窗口的截图，所以必须保证模拟器窗口在最前面
为存储结果，请手动的创建mitmproxy-result文件夹，并清空（主要不要出现0，1,2文件夹）


step 4.
after driver program ,start analyse program Analyze-URL.py
it will find the first url to show something,and the common url list of openning news,find the last url from the result of last step.

驱动结束后，启动分析程序Analyze-URL.py。查找第一个显示内容的URL和常用的URL列表，以及最后一个的URL
（这个部分在接下来的工作已经弃用）

step 5.
Modify the delay-mitm.py ,it's used for log the delay.
It will log the all response time(delay-time).
According to first url's respone and the last url's response,log the time to another file(delay).
This script is simple ,you can modify this to log any detail.

Analyze-TIME is aim to find the whole delay accroding to log file "delay-time"
If there are no response after 6s ,we define this process is end.

根据上个结果中的URL修改delay-mitm.py中的部分内容，该脚本主要用于记录所有响应的时间，以及特殊的响应时间。
脚本较为简单，可以直接从脚本中找到为记录特定URL的部分。
Analyze-TIME的脚本是根据记录的所有响应时间，从中找出完整的时延。
定义新闻打开的结束为出现6s而不产生新的request。


step 6.
Run driver-delay to click news five times,and log the user-perceive delay by using delay-mitm.py(mitmproxy)
Currently,it will log the two time point of CNN apps to judge the user-perceive delay.
for example:
cdn.flipboard.com/flipmag/assets/fonts/truetype/Roboto-Regular-5673da.ttf
ii2.cdn.turner.com/cnnnext/dam/assets/150524085634-sotu-starr-defense-secretary-ash-carter-iraq-ramadi-isis-00000000-horizontal-gallery.jpg

启动driver-delay完成自动化记录响应事件，主要利用了delay-mitm脚本中实现的功能
目前通过记录两个特定的时间点来判断用户感知的时延，分别是字体请求与图片请求。

_______________________________________________
diff-zone.py is aim to find the part of display content of CNN app.
it will compare two pictures and find the different zone of them.
it's used in app-mitm.py to calculate the similar value of two picture.

diff-zone.py是为了截图图片中的不同显示区域