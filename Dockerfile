FROM alpine:3.20

ARG USERNAME="app"
COPY nginx.conf /etc/nginx/nginx.conf

RUN apk upgrade --no-cache && apk add --no-cache bash ffmpeg python3 py3-pip nginx sudo wget && adduser -D -s "/bin/bash" "${USERNAME}" \
    && echo "app ALL = NOPASSWD: /bin/chown,/usr/sbin/nginx" > /etc/sudoers.d/app && chmod 400 /etc/sudoers.d/app \
    && chown -R app:app /var/lib/nginx && chown app:app /var/log/nginx

USER "${USERNAME}"
COPY . "/home/${USERNAME}"
COPY "entrypoint.bash" "/entrypoint.bash"
WORKDIR "/home/${USERNAME}"

RUN python3 -m venv "/home/${USERNAME}/venv" && . "/home/${USERNAME}/venv/bin/activate" && pip install -U pip && pip install -U setuptools \
    && pip install --no-cache-dir -r requirements.txt && mkdir logfiles tmp

EXPOSE 8080
VOLUME ["/persist", "/home/app/staticfiles"]

ENTRYPOINT ["bash", "/entrypoint.bash"]
