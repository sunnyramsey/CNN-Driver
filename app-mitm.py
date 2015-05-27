from libmproxy.script import concurrent
import time,thread,os
import Image
import psutil


def make_regalur_image(region):
    return region.resize((256,256)).convert('RGB')

def split_image(img, part_size = (64, 64)):
	w, h = img.size
	pw, ph = part_size
	assert w % pw == h % ph == 0
	return [img.crop((i, j, i+pw, j+ph)).copy() \
	                for i in xrange(0, w, pw) \
	                for j in xrange(0, h, ph)]

def hist_similar(lh, rh):
	assert len(lh) == len(rh)
	return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

def calc_similar(li, ri):
	return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0

def calc_similar_by_path(lf, rf):
	l_temp = Image.open(lf)
	r_temp = Image.open(rf)
	#this crop box can be got by python code
	box = (1,119,428,664)
	l_pic = l_temp.crop(box)
	r_pic = r_temp.crop(box)
	li, ri = make_regalur_image(l_pic),make_regalur_image(r_pic)
	return calc_similar(li, ri)


class WindowScreenShot:
    def __init__(self):
        try:
            import wnck
        except:
            pass
        else:
            self.screen = wnck.screen_get_default()
            self.wins=[]
            self.win=None

    def getScreenShot(self,name,fileName):

        self.screen.force_update()
        self.wins = self.screen.get_windows()
        for wintmp in self.wins:
            win_name = wintmp.get_name()
            if name in win_name:
                self.win = wintmp
                break
        if self.win is not None:
            import gtk.gdk
            rootWindow = gtk.gdk.get_default_root_window()
            windowGeometry = self.win.get_geometry()
            pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,windowGeometry[2],windowGeometry[3])
            pb = pb.get_from_drawable(rootWindow,rootWindow.get_colormap(),windowGeometry[0],windowGeometry[1],0,0,windowGeometry[2],windowGeometry[3])
            pb.save(fileName,"png")



def start(context,argv):
	context.endTime = 0
	context.currentId=0
	context.f_summary = open('summary-log','a+')
	context.lock = thread.allocate_lock()
	context.finish = False
	context.screenTool = WindowScreenShot()
	context.lastRequest = ''
	context.path ='/home/ramsey/mitmproxy-result/'+argv[1]
	os.mkdir(context.path)
	os.mkdir(context.path+'/screenshot')
	context.f = open(context.path+'/http-log','w')

@concurrent
def request(context ,flow):
	context.lock.acquire()
	startTime = int(time.time())
	requestId = context.currentId + 1
	context.currentId = requestId
	screenShot = '%s/screenshot/log-%d.png' % (context.path,requestId)
	if startTime >= context.endTime:
		context.endTime = startTime + 5
	else :
		context.endTime = context.endTime + 5
	sleepTime = context.endTime - startTime
	context.lock.release()

	time.sleep(sleepTime)
	
	if context.finish == True:
		pass
	else :
		context.screenTool.getScreenShot('Genymotion',screenShot)
		if requestId > 1:
			lastId = requestId-1
			l_path = '%s/screenshot/log-%d.png' % (context.path,lastId)
			r_path = '%s/screenshot/log-%d.png' % (context.path,requestId)
			similar = calc_similar_by_path(l_path,r_path)
			context.f.write('similar:'+str(similar)+'\n')
			context.f.flush()
#			if similar < 0.975:
#				context.finish = True
#				context.f.close()
#				context.f_summary.write(context.lastRequest+'\n')
#				context.f_summary.flush()
#				context.f_summary.close()
#				parent = psutil.Process(os.getpid())
#				for child in parent.children(recursive=True):
					#os.kill(child.pid,9)
#					child.kill()
#				parent.kill()
				#os.kill(parent.pid,9)	

		info = 'request:%d:%d:%s:%s%s' % (int(time.time()),requestId,screenShot,flow.request.host,flow.request.path)
		context.f.write(info+'\n')
		context.f.flush()
		context.lastRequest = '%d:%s%s' % (requestId,flow.request.host,flow.request.path)

def done(context):
	context.f.close()

	
