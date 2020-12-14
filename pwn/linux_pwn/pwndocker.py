#!/usr/bin/env python
import os
import sys
# user_name=sys.argv[1]
# psw=sys.argv[2]

user_name='byzero'
psw='byzero512@gmail.com'
# old-releases.ubuntu.com
# 12.04 
# 14.04 trusty(219)
# 16.04 xenial(223)     16.10 yakkety(224)
# 17.04 zesty(224_1)    17.10 artful(226)
# 18.04 bionic(227)     18.10 cosmic(228)
# 19.04 disco(229)      19.10 eoan(229_1)
ubuntu_version=[
    '19.10','19.04',
    '18.10','18.04',
    '17.10','17.04',
    '16.10','16.04',
    '14.04',
    '12.04'
]
old_ubuntu_version=['14.04','12.04']
ubuntu_libc={
    '19.10':'229_1910',
    '19.04':'229_1904',
    '18.10':'228',
    '18.04':'227',
    '17.10':'226',
    '17.04':'224_1704',
    '16.10':'224_1610',
    '16.04':'223',
    '14.04':'219',
    '12.04':'217'
}
# then support 14.04 and 12.04
# mirrors.ustc.edu.cn/ubuntu-old-releases
not_support=[
    '16.10','17.04','17.10'
]
# cur_suport=[
#     '19.10','19.04',
#     '18.10','18.04',
#     '16.04','15.04'
# ]
cur_suport=list(set(ubuntu_version)-set(not_support))
been_built=[
    # '16.04','16.10',
    # '17.10',
    # '18.04,'
    '19.10','19.04',
    '18.10','18.04',
    '17.10','17.04',
    '16.10','16.04'
]
# pip install pwntools -i https://pypi.mirrors.ustc.edu.cn/simple/
dockerfile_content="""
FROM ubuntu:{version}
{command}
RUN dpkg --add-architecture i386 && \
    apt-get clean && \
    apt-get update && \
    apt-get install -y less && \
    apt-get install -y sudo && \
    apt-get install -y vim && \
    apt-get install -y libc6:i386 libc6-dbg:i386 libc6-dbg  libpthread-stubs0-dev gcc-multilib && \
    apt-get install -y lib32stdc++6 g++-multilib && \
    apt-get install -y libssl-dev libffi-dev git && \
    apt-get install -y build-essential strace ltrace && \
    apt-get install -y gcc g++ gdb && \
    apt-get install -y python2.7 python-dev python-pip python3-dev python3-pip && \
    apt-get install -y tmux && \
    apt-get install -y netcat && \
    apt-get install -y qemu qemu-user qemu-system qemu-kvm && \
    apt-get install -y glibc-source && \
    cd /usr/src/glibc/ && \
    tar -xvJf /usr/src/glibc/glibc-*.tar.xz && \
    cd ~ && \
    pip install pwntools

RUN cd ~ && \
    echo "source /shareDir/share/.gdbinit" >> .gdbinit && \
    echo "source /shareDir/share/.bashrc" >> .bashrc && \
    echo "source /shareDir/share/.tmux.conf" >> .tmux.conf

RUN useradd -m {name} && echo "{name}:{password}" | chpasswd && adduser {name} sudo
USER {name}
RUN cd ~ && \
    echo "source /shareDir/share/.gdbinit" >> .gdbinit && \
    echo "source /shareDir/share/.bashrc" >> .bashrc && \
    echo "source /shareDir/share/.tmux.conf" >> .tmux.conf

VOLUME [ "/shareDir" ]
WORKDIR /shareDir
ENTRYPOINT [ "/bin/bash" ]
"""

dockerfile_content1="""
FROM ubuntu:{version}
{command}
RUN dpkg --add-architecture i386 && \
    apt-get clean && \
    apt-get update && \
    apt-get install -y less && \
    apt-get install -y sudo && \
    apt-get install -y vim && \
    apt-get install -y libc6:i386 libc6-dbg:i386 libc6-dbg  libpthread-stubs0-dev gcc-multilib && \
    apt-get install -y lib32stdc++6 g++-multilib && \
    apt-get install -y libssl-dev libffi-dev git && \
    apt-get install -y build-essential strace ltrace && \
    apt-get install -y gcc g++ gdb && \
    apt-get install -y python2.7 python-dev python-pip python3-dev python3-pip && \
    apt-get install -y tmux && \
    apt-get install -y netcat && \
    pip install --upgrade pip && \
    pip install pwntools

RUN cd ~ && \
    echo "source /shareDir/share/.gdbinit" >> .gdbinit && \
    echo "source /shareDir/share/.bashrc" >> .bashrc && \
    echo "source /shareDir/share/.tmux.conf" >> .tmux.conf

RUN useradd -m {name} && echo "{name}:{password}" | chpasswd && adduser {name} sudo
USER {name}
RUN cd ~ && \
    echo "source /shareDir/share/.gdbinit" >> .gdbinit && \
    echo "source /shareDir/share/.bashrc" >> .bashrc && \
    echo "source /shareDir/share/.tmux.conf" >> .tmux.conf

VOLUME [ "/shareDir" ]
WORKDIR /shareDir
ENTRYPOINT [ "/bin/bash" ]
"""

towrite=""""""
def gen_dockerfile():
    for version in ubuntu_version:
        if version in not_support:
            # ------------ official
            command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list"
            # ------------ ustc
            command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/mirrors.ustc.edu.cn\/ubuntu-old-releases/g' /etc/apt/sources.list"
            # ------------ nju
            # command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/mirrors.nju.edu.cn\/ubuntu-old-releases/g' /etc/apt/sources.list"
            # ------------ aliyun
            # command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/mirrors.aliyun.com\/ubuntu-old-releases/g' /etc/apt/sources.list"
            # ------------ 163
            # command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/mirrors.163.com\/ubuntu-old-releases/g' /etc/apt/sources.list"
            # ------------ sohu
            # command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/mirrors.sohu.com\/ubuntu-old-releases/g' /etc/apt/sources.list"
            # ------------ tsinghua
            # command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn\/ubuntu-old-releases/g' /etc/apt/sources.list"
        else:
            # ------------ official
            command='#'
            # ------------ ustc
            command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/debian.ustc.edu.cn/g' /etc/apt/sources.list"
            # ------------ ustc debian
            command="RUN sed -i -re 's/us.archive.ubuntu.com|archive.ubuntu.com|security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list"   
            # ------------ tsinghua
            command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list"
            # ------------ bjtu
            # command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/mirror.bjtu.edu.cn\/cn/g' /etc/apt/sources.list"
        towrite=dockerfile_content.format(version=version,command=command,name=user_name,password=psw)
        if version in old_ubuntu_version:
            towrite=dockerfile_content1.format(version=version,command=command,name=user_name,password=psw)
        dockerfile=open('./dockerfile_{}'.format(ubuntu_libc.get(version)),'w')
        dockerfile.write(towrite)
        dockerfile.flush()
        dockerfile.close()
def build():
    for version in ubuntu_version:
        if version in been_built:
            continue
        print('docker build -f dockerfile_{} -t {} .'.format(ubuntu_libc.get(version),ubuntu_libc.get(version)))
        os.system('docker build -f dockerfile_{} -t {} .'.format(ubuntu_libc.get(version),ubuntu_libc.get(version)))

gen_dockerfile()
build()
