from time import *

debut = time()
#sleep(60)
fin = time() - debut

l = localtime(fin)
print(strftime("%m:%S", l))