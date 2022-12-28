FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /code/DjangoBlog/
RUN  apt-get install  default-libmysqlclient-dev -y && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
COPY . .
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple &&  \
    pip install -Ur requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple &&  \
    pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple &&  \
    pip cache purge && chmod -R 755 /code/DjangoBlog/bin/

#ENTRYPOINT ["/code/DjangoBlog/bin/docker_start.sh"]
CMD [ "sh", "/code/DjangoBlog/bin/docker_start.sh"]
