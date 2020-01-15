

### tools

1. apktool: 反编译apk/回编译apk
2. jadx: 将apk反编译成java代码
3. apksigner: apk签名/验证
4. smail/baksmail
5. dexdump: 查看 .dex 的 Dalvik Byte Code



1. 获得apk的smail代码

    java.exe -Xmx256m -jar apktool.jar d -o \<outputdir> app.apk

2. 获得apk的java代码

    jadx.bat -r -d \<outputdir> app.apk

3. 再次编译

    java -Xmx256m -jar apktool.jar b \<outputdir>

4. apk签名

    apksigner sign --ks release.jks app.apk

5. apk签名验证

    apksigner verify --verbose app.apk



### debug环境

### jeb

网上有jeb3-android的破解版, 可用



#### apk profiler

比较新的版本的android studio可以直接打开apk, 并自动生成smali文件等, 可以在上面下断点, 但是不能修改文件内容, 不如用jeb



#### apktool

1. 准备工具
    1. android studio, smalidea(AS的插件)
    2. apksigner: 在AS/SDK/build-tools/SDK-version/lib目录下有
    3. adb: 在AS/platform-tools目录下
    4. apktool, jadx
2. apktool 解包, 修改AndroidManifest.xml, 在application标签中添加下面的属性, 然后再次打包, 并签名

```xml
<application android:debuggable="true" ... >
```

3. 启动android虚拟机, 在PC机上使用adb把apk安装在android虚拟机上, 并以调试模式启动apk

```bash
# 安装apk
adb install app.apk
# 调试模式启动apk: 例如 adb shell am start -D -n com.a.easyjni/.MainActivity
adb shell am start -D -n package/.activitiyname
```

4. 在PC机上设置端口转发

```bash
# 查看启动的apk程序的package的pid, 例如: adb.exe shell ps | grep com.a.easyjni
adb shell ps | grep package
# 转发, 例如 adb forward tcp:5050 jdwp:14168
adb forward tcp:PC_port jdwp:pid
```

5. android studio打开项目, 并将smail目录设置为"Source Root", 然后添加debug配置
    1. 打开菜单栏Run/Edit Configurations
    2. 点击"+"号, 添加一个Remote配置, 设置好IP和端口

