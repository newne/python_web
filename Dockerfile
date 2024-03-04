#基础镜像
FROM python:3.9.16 as builder-image
COPY requirements.txt .
# 安装支持 （阿里云出现timeout的问题3次，换豆瓣）
RUN pip --default-timeout=100 install -r requirements.txt -i  http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
FROM python:3.9.16-slim
# 设置code文件夹是工作目录
WORKDIR /root/bin
# 相关信息及描述
LABEL MAINTAINER="ncgnewne" version="0.1" description="联想制冷项目指标展示页面"
COPY --from=builder-image /usr/local/bin /usr/local/bin
COPY --from=builder-image /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
# 解决ImportError: libgomp.so.1: cannot open shared object file: No such file or directory问题
RUN echo "" > /etc/apt/sources.list
RUN echo "deb http://mirrors.aliyun.com/debian buster main" >> /etc/apt/sources.list; \
    echo "deb http://mirrors.aliyun.com/debian-security buster/updates main" >> /etc/apt/sources.list ; \
    echo "deb http://mirrors.aliyun.com/debian buster-updates main" >> /etc/apt/sources.list ;
RUN apt-get update
RUN apt-get install libgomp1 --assume-yes
# 设置时区
ENV TZ=Asia/Shanghai
# 设置时区
RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo "${TZ}" > /etc/timezone
#代码添加到code文件夹，后面可以通过进入容器中看的
ADD . /root/bin

EXPOSE 9100
# set start command
ENTRYPOINT exec bash run.sh