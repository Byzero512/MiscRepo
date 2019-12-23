

from pwn import *
mode=['byte','short','int']
def fmtstr64_payload(offset,writes,written=0,mode='byte'):
	if mode=='byte':
		fmt64_payload=''


	elif mode=='short':
		fmt64_payload=''
		

	elif mode=='int':
		fmt64_payload=''

	else:
		print("fmt_payload generate false")
		return
	return fmt64_payload

def printarch():
	print(context.arch)
	
