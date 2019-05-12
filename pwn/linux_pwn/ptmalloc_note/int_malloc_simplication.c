
int_malloc()
{
    if(fast_req)
        {
            exact_fit;           
            check idx;
            check_remalloced_chunk();
            return;
        }
    if(small_req)
        {
            exact_fit; 
            check BK->fd == p;                    //BK=p->bk,即倒数第二个
            check size=next->prevsize
            check_malloced_chunk();
            return;
        }
    if(large_req)
        {
            consolidate();           
        }

    for(;;)            //大循环
        {                              
            while(unsorted bin不为空)
            {
                check victim->size;    //带标志位,不能太大不能太小

                if(small_req && use remainder)
                    fit;
                    check_malloced_chunk();
                    
                    return;
                all_req:
                    exact_fit;     
                    check_malloced_chunk();
                    return;
                place unsorted_chunk into its bin;      // =============== 可以说是没有检查
                
                //如果是largebin的话,会检查最后一个chunk以及fwd(要插入的fd_nextsize链的下一个),要检查他们是否为nchunk
                //正向遍历,bk_nextsize链
            }

            if(large_req)
                fit;        //large_req use same_bin for exact_fit and next_fit
                unlink();   //反向遍历,fd_nextsize链,找到第一个不小于的
                check_malloced_chunk();        
                return;                                       //关于nextfit需要补充一下？？？？？？？？？？？？？？？？？？？？

            all_req:                 
                next_fit;            //use next_bin(not fastbin) for next_fit 
                unlink();
                check_malloced_chunk();
                return;

            use top_chunk:                           
                if(fit)
                    check_malloced_chunk();
                    return;
                else if(have_fastchunk)
                    consolidate();                   //just here can use the Circle
                else
                    sysmalloc();                     // mmap and extend top_chunk
                    return;
        }
}

//change link --> get chunk --> set something --> merge --> check() --> return 

