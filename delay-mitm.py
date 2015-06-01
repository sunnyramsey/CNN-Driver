from libmproxy.script import concurrent
import time,thread,os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

def start(context,argv):
	context.f = open(BASE_PATH + '/delay','a+')
	context.f_time = open(BASE_PATH + '/delay-time','w')
	context.startUrl = 'cdn.flipboard.com/flipmag/assets/fonts/truetype/Roboto-Regular-5673da.ttf'
	context.startUrl_1 = 'ii2.cdn.turner.com/cnnnext/dam/assets/150524085634-sotu-starr-defense-secretary-ash-carter-iraq-ramadi-isis-00000000-horizontal-gallery.jpg'
	info = 'open: %d ' % int(time.time())
	context.f.write(info+'\n')
	context.f.flush()


@concurrent
def response(context,flow):

	info = '%d' % int(time.time())
	context.f_time.write(info+'\n')
	context.f_time.flush()

	rsc = flow.request.host + flow.request.path
	if rsc == context.startUrl:
		info = 'start_text: %d ' % int(time.time())
		context.f.write(info+'\n')
		context.f.flush()
	elif rsc == context.startUrl_1:
		info = 'start_pic: %d ' % int(time.time())
		context.f.write(info+'\n')
		context.f.flush()
#	elif rsc == context.endUrl:
#		info = 'end: %d ' % int(time.time())
#		context.f.write(info+'\n')
#		context.f.flush()

def done(context):
	context.f.close()
	context.f_time.close()
