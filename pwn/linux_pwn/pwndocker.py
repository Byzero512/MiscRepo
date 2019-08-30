#!/usr/bin/env python
import os
import sys

# user_name=sys.argv[1]
# psw=sys.argv[2]
user_name='byzero'
psw='byzero512@gmail.com'
# old-releases.ubuntu.com
ubuntu_version=[
    '19.04','18.10',
    '18.04',
    '17.10','17.04','16.10',
    '16.04'
]
# supporting=[           # debian.ustc.edu.cn 
#     '19.04','18.10','18.04','17.10','17.04','16.04'
# ]
# mirrors.ustc.edu.cn/ubuntu-old-releases
not_support=[
    '16.10','17.04','17.10'
]


dockerfile_content="""
FROM ubuntu:{version}
{command}
RUN dpkg --add-architecture i386 && \
    apt-get clean && \
    apt-get update && \
    apt-get install less && \
    apt-get install -y sudo && \
    apt-get install -y vim && \
    apt-get install -y libc6:i386 libc6-dbg:i386 libc6-dbg  libpthread-stubs0-dev gcc-multilib && \
    apt-get install -y lib32stdc++6 g++-multilib && \
    apt-get install -y libssl-dev && \
    apt-get install -y build-essential strace ltrace && \
    apt-get install -y gcc g++ gdb && \
    apt-get install -y python-dev python-pip python3-dev python3-pip && \
    apt-get install -y tmux && \
    apt-get install -y netcat && \
    apt-get install -y qemu qemu-user qemu-system qemu-kvm && \
    apt-get install -y glibc-source && \
    tar -xvf /usr/src/glibc/glibc-*.tar.xz && \
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
    for i in range(len(ubuntu_version)):
        
        if ubuntu_version[i] in not_support:
            # command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list"
            command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/mirrors.ustc.edu.cn\/ubuntu-old-releases/g' /etc/apt/sources.list"
        else:
            # command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/debian.ustc.edu.cn/g' /etc/apt/sources.list"
            # command='#'
            command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list"
        # if ubuntu_version[i]=='17.04':
            # command="RUN sed -i -re 's/archive.ubuntu.com|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list"      # old-releases.ubuntu.com        
        towrite=dockerfile_content.format(version=ubuntu_version[i],command=command,name=user_name,password=psw)
        dockerfile=open('./dockerfile{}'.format(229-i),'w')
        dockerfile.write(towrite)
        dockerfile.flush()
        dockerfile.close()
def build():
    for i in range(len(ubuntu_version)):
        version=229-i
        if ubuntu_version[i]=='17.04':
            version='224_1704'
        os.system('docker build -f dockerfile{} -t {} .'.format(229-i,version))

gen_dockerfile()
build()
