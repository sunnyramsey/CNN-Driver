import os
import unittest
from appium import webdriver
from time import sleep
import time
import subprocess
import threading
import psutil
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

class MitmProxyDriver(object):

    def __init__(self):
	self.process = None
	self.status = None
	self.startTag = True
 
    def run(self,timeout,log,err,driver,data_no):
        def target(**kwargs):
            try:
		driver = kwargs['driver']
		startTag = kwargs['startTag']
		temp_args = 'delay-mitm.py'
		log = kwargs['stdout']
		err = kwargs['stderr']
		args = ['mitmproxy','-s']
		args.append(temp_args)
		self.process = subprocess.Popen(args,stdout=log,stderr=err)
		if startTag == True:
			sleep(5)
			startTag = False
		else:	
			sleep(2)

		els = driver.find_elements_by_id('com.cnn.mobile.android.phone:id/broadsheet_headline')	
		el = els[0]

		location = el.location
		size = el.size
		el_x = location['x'] + size['width']/2
		el_y = location['y'] + size['height']/2
	

		action = TouchAction(driver)
		action.press(x=el_x, y=el_y).release().perform()


		f = open(BASE_PATH + '/delay','a+')
		info = 'click: %d ' % int(time.time())
		f.write(info+'\n')
		f.close()		

		self.process.wait()

            except:
                self.status = -1

	
	kwargs = {}
	kwargs['id'] = data_no
	kwargs['driver'] = driver
	kwargs['stdout'] = log
	kwargs['stderr'] = err
	kwargs['startTag'] = self.startTag
        if self.startTag == True:
		self.startTag = False

        thread = threading.Thread(target=target,kwargs=kwargs)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
	    print 'time out'
            thread.join()
        return self.status

class CnnTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
	pass
        #self.driver.quit()

    def test_cnn(self):
	for i in range(5):
		desired_caps = {}
        	desired_caps['platformName'] = 'Android'
      	  	desired_caps['platformVersion'] = '4.3'
        	desired_caps['deviceName'] = 'Android Emulator'
        	desired_caps['app'] = BASE_PATH + '/apps/cnn.apk'
		desired_caps['newCommandTimeout'] = 150
		desired_caps['appActivity'] = '.ui.MainActivity'

		self.log_file = open(BASE_PATH + '/logs/log-file','w')	
		self.err_file = open(BASE_PATH + '/logs/err-file','w')
		args = ['mitmproxy']

		self.proxy_process = subprocess.Popen(args,stdout=self.log_file,stderr=self.err_file)
       
		sleep(5)

        	self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
		#initial

		sleep(3)
	
		#close whats new window
		el = self.driver.find_element_by_xpath('//android.widget.Button[contains(@text, "Dismiss")]')
		el.click()	
	
		sleep(3)
	
		#close privacy window
		el = self.driver.find_element_by_xpath('//android.widget.TextView[contains(@text, "Close")]')
		el.click()

		sleep(3)

		#click home button

		els = self.driver.find_elements_by_xpath('//android.widget.TextView[contains(@text, "Home")]')
		el = els[1]
		location = el.location
		size = el.size
		el_x = location['x'] + size['width']/2
		el_y = location['y'] + size['height']/2

		action = TouchAction(self.driver)
		action.press(x=el_x, y=el_y).release().perform()

		sleep(10)
	
		print 'shut down normal proxy'
		parent = psutil.Process(self.proxy_process.pid)
		for child in parent.children(recursive=True):
			child.kill()
		parent.kill()

		sleep(3)
		print 'click news'
		mitm = MitmProxyDriver()
		mitm.run(50,self.log_file,self.err_file,self.driver,i)
		
		print 'quit'

		self.driver.quit()



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CnnTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
