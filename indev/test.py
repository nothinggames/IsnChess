from time import *


start = time()
print(strftime("%H:%M:%S", localtime()))
sleep(10)
print(strftime("%H:%M:%S", localtime(start)))
print(strftime("%H:%M:%S", localtime()))
print(gmtime(int(time()-start)))
print(localtime())
print(time()-start)
print(strftime("%H:%M:%S", gmtime(time()-start+10)))