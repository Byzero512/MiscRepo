'''
	used to patch procgram with patch by byte in IDA
'''
def str2hex(shellcode_payload):
	shellcode_num=''
	for i in range(len(shellcode_payload)):
		shellcode_num=hex(ord((shellcode_payload[i])))[2:]+shellcode_num	
	return shellcode_num

