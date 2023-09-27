### Builder
FROM certbot/certbot AS builder

RUN apk add --no-cache git grep
RUN pip install -U pip build

RUN git clone https://github.com/tmuncks/certbot-dns-powerdns.git /tmp/certbot-dns-powerdns

WORKDIR /tmp/certbot-dns-powerdns
RUN python3 -m build

### Runtime
FROM certbot/certbot

COPY --from=builder /tmp/certbot-dns-powerdns/dist/certbot_dns_powerdns*.whl /

# FIXME: Some of our requirements fail to build with Cython 3.x, so add constraint
#        on Cython version when installing the package

#RUN pip install /certbot_dns_powerdns*.whl
RUN echo "Cython<3" > /cython_constraint.txt
RUN PIP_CONSTRAINT=/cython_constraint.txt pip install /certbot_dns_powerdns*.whl

COPY src/main.py /

ENTRYPOINT ["python3", "-u", "/main.py"]
CMD []
