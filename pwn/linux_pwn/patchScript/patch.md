# patch

## exchangeGot

1. 有一个函数: exchangGot\(fpath=""\); 可以将两个函数的got entry互换, 但是不改变文件大小
2. 有些类似通防, 也没有经过大量测试, 慎用


## segmentAdd

1. 有一个函数: segmentAdd\(fpath=""\); 可以给可执行文件增加一个RWX段; 但是这个函数无法用在32位下没开pie的程序, 而且会增加文件大小, 慎用;


