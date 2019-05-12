struct large_chunk = {long long prev_size;
union size {
    long long no_mask_size;
    long long mask_size;
} size;
large_chunk *fd;
large_chunk *bk;
large_chunk *fd_nextsize;
large_chunk *bk_nextsize;
}
;

// 插在最后面 bin->bk: 即小于最小
void smaller_than_all() {

    // size |= 1;
    // check(bck->bk);
    fwd = bin;
    bck = bin->bk;

    victim->fd_nextsize = bin->fd;
    victim->bk_nextsize = bin->fd->bk_nextsize;
    (bin->fd)->bk_nextsize->fd_nextsize = victim;      // ***********这里可以做点什么? 通过控制第一个chunk的 bk_nextsize 往某个地址写入victim?
    (bin->fd)->bk_nextsize = victim;

    victim->bk = bin;
    victim->fd = bin->fd;
    (bin->bk)->fd = victim;
    bin->bk = victim;
}

// 插在nextsize链上: 大于最小, 并且没有相同大小的,?????????????????? 这个可以往两个地方写入victim?
void insert_into_nextsize() {
    bck = bin;
    fwd = bin->fd;
    size |= 1;
    // assert(chunk_main_arena(bin->bk));
    // assert(chunk_main_arena(fwd));                     // 这里的fwd就是找出来的那个 fwd, bck 被找出来之后不能被改变
    while (size < fwd->no_mask_size) {
        fwd = fwd->fd_nextsize;
        // assert(chunk_main_arena(fwd));
    }
    // ****下面的fwd是上面while循环找出来的****
    victim->fd_nextsize = fwd;
    victim->bk_nextsize = fwd->bk_nextsize; 
    fwd->bk_nextsize->fd_nextsize = victim;         // 可以通过控制 fwd的bk_nextsize往某个地址写入victim
    fwd->bk_nextsize = victim;
    
    // bck = fwd->bk;
    victim->bk = fwd->bk;
    victim->fd = fwd;
    fwd->bk->fd = victim;                         // *********************** 可以通过控制fwd的bk来往某个地址写入victim
    fwd->bk = victim;
}

// 插在fd-bk链上: 即bin中有和这个要插入的chunk1大小相同大小的chunk0, 等于某一个
void insert_into_fd_bk() {
    bck = bin;
    fwd = bin->fd;
    size |= 1;
    // assert(chunk_main_arena(bck->bk));
    // assert(chunk_main_arena(fwd));
    while (size < fwd->no_mask_size) {
        fwd = fwd->fd_nextsize;
        // assert(chunk_main_arena(fwd));
    }
    // ****下面的fwd是上面while循环找出来的****
    bck = fwd->fd->bk;
    victim->bk = bck;
    victim->fd = fwd->fd;
    fwd->fd->bk->fd = victim;                     // ************************** 可以通过控制fwd的fd指向的那一个chunk的的bk来往某个地址写入victim
    fwd->fd->bk = victim;
}