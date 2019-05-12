# define check_chunk(A, P)              do_check_chunk (A, P)
# define check_free_chunk(A, P)         do_check_free_chunk (A, P)
# define check_inuse_chunk(A, P)        do_check_inuse_chunk (A, P)
# define check_remalloced_chunk(A, P, N) do_check_remalloced_chunk (A, P, N)
# define check_malloced_chunk(A, P, N)   do_check_malloced_chunk (A, P, N)

# define check_malloc_state(A)         do_check_malloc_state (A)

do_check_chunk(av,p)
{
    if(nchunk)
    {
        if(not topchunk)
            if(av contiguous)            //the arena is contiiguous
                check:
                    p>=min_address;
                    p+sz<=av->top;   
                                     //max_address=top_ptr+top_size
                                     //min_size=max_address-av->system_mem
        else    
            check:
                sz>=MINSIZE;
                p->prev_inuse==1;
    }
}

do_check_free_chunk(av,p)
{
    do_check_chunk(p);

    check:
        next->prev_inuse==0;        //p freed
        p is nchunk;
        sz,ptr align;
        next inuse;              //top chunk || next->next_chunk->previnuse==1

        p->fd->bk==p;             // 类似 unlink check
        p->bk->fd==p;

        p->size&~(PREV_INUSE|NON_MAIN_ARENA)==p->mchunk_prevsize;
                     //i don't know this ^^^
}

do_check_inuse_chunk(av,p)
{
    do_check_chunk(av,p);

    if(mchunk)
        return;

    check:
        next->prev_inuse==1;            //p inuse

    if(prv freed)
        check:
            prv->next_chunk==p;
            do_check_free_chunk(av,prv);

    if(next top_chunk)
        check:
            next->prev_inuse==1;
            next->size>=Minsize;
    else if(next freed)
        do_check_free_chunk(av,prv);                         //这里有点问题
}

do_check_remalloced_chunk(av,p,s)
{
    if(nchunk)
    {
        check:
            av;                 
    }
    do_check_inuse_chunk(av,p);

    check:
        sz,ptr,align;
        sz>=MINSIZE;
    
    an check for rest after spliting chunk;      //maybe for rest,i am not sure
}

do_check_malloced_chunk(av,p,s)
{
    do_check_remalloced_chunk(av,p,s);

    check:
        p->prev_inuse==1;             // prv inuse
}



#define unlink_check
    check:
        next->prev_size==msize;        //msize is the p->size after mask

        p->bk=BK;
        p->fd=FD;
        BK->fd=p;
        FD->bk=p;
        if(in largebin && P->fd_nextsize!=null)          // P in largebin and in nextsize list
            check: 
                p->fd_nextsize->bk_nextsize==P;
                p->bk_nextsize->fd_nextsize==P;


#define unlink(p){
    p->size=(p->next)->prev_size 
    //chunk_size(p)==prev_size(next_chunk(p))
    FD=P->fd;
    BK=P->bk;

    FD->bk=BK;         doing unlink;
    BK->fd=FD;

    if(largechunk in large bin)
        set nextsize;
}