//bypass测试与ubuntu16.04LTS, 使用 glibc2.23

do_check_malloced_chunk():
	do_check_remalloced_chunk()
	上一个chunk在使用                     //即在list上的previnuse位都为1
do_check_remalloced_chunk():
	指针大小要对齐
	next->previnuse==1

# fake chunk原则:
1. previnuse=1
2. next不是topchunk      

malloc:
	fastbin:
		idx                  
	smallbin:
		BK->fd==victim
		prev_inuse==1                // fake的时候注意一下
		next->previnuse==1           // 程序会自动帮忙设置好
	unsortedbin:
		next->previnuse==1          // 程序会自动帮忙设置好,注意bk要指向一个可写的区域
	largebin:
		unlink
		next->previnuse==1         // 程序会自动帮忙设置好,不用fake
// malloc的时候可能还要注意next在使用
free:
	检查指针大小对齐
	fastbin:
		double_free
		idx
		next->size
	other nchunk:
        next->size
		next->previnuse==1               // 程序不会帮忙设置 即 cur inuse
		(next->nextchunk->previnuse==1 
		|| next in list and normal)  // 这个check很麻烦




