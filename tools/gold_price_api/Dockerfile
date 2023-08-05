FROM python:3.8.2

# 对于3.7以上版本: 标准输出stdout和标准错误stderr全部采用unbuffered 不用配置 PYTHONUNBUFFERED 1
#ENV PYTHONUNBUFFERED 1
WORKDIR /code/gold_price_api/
RUN  apt install default-libmysqlclient-dev -y && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
COPY ./requirements.txt /code/gold_price_api/

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple &&  \
    pip install -Ur requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple &&  \
    pip install channels["daphne"] -i https://pypi.tuna.tsinghua.edu.cn/simple &&  \
    pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple &&  \
    pip cache purge

COPY . .

RUN chmod -R 755 /code/gold_price_api/

CMD ["python3", "custom-crawler/crawler.py"]
