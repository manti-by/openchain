FROM python:3.6

RUN mkdir -p /srv/openchain/
RUN mkdir -p /var/lib/openchain/

COPY requirements.txt /etc/openchain/requirements.txt
RUN pip install --trusted-host pypi.org --no-cache-dir -r /etc/openchain/requirements.txt

RUN apt-get autoremove --purge && apt-get clean

WORKDIR /srv/openchain
RUN git init
RUN git remote add origin https://bitbucket.org/manti_by/openchain.git

CMD ["python", "run.py"]