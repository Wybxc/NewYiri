FROM bitnami/pytorch:2.0.0
WORKDIR /app
COPY . /app
USER root
RUN pip install -r requirements.txt -i https://mirrors.pku.edu.cn/pypi/web/simple
ENV NEW_YIRI_MODEL wybxc/new-yiri
ENV NEW_YIRI_REVISION main
CMD ["python", "-m", "neoyiri"]
