FROM alpine:3.18

# Opencontainers Specs (https://github.com/opencontainers/image-spec/blob/main/annotations.md)
LABEL org.opencontainers.image.title="VerbaCap"
LABEL org.opencontainers.image.description="Podcast Manager"
LABEL org.opencontainers.image.source="https://github.com/Mirio/verbacap"
LABEL org.opencontainers.image.licenses="MIT"

ARG USERNAME="app"
COPY nginx.conf /etc/nginx/nginx.conf

RUN apk add --no-cache bash ffmpeg python3 py3-pip nginx sudo && adduser -D -s "/bin/bash" "${USERNAME}" \
    && echo "app ALL = NOPASSWD: /bin/chown,/usr/sbin/nginx" > /etc/sudoers.d/app && chmod 400 /etc/sudoers.d/app \
    && chown -R app:app /var/lib/nginx && chown app:app /var/log/nginx

USER "${USERNAME}"
COPY . "/home/${USERNAME}"
COPY "entrypoint.bash" "/entrypoint.bash"
WORKDIR "/home/${USERNAME}"

RUN python3 -m venv "/home/${USERNAME}/venv" && . "/home/${USERNAME}/venv/bin/activate" \
    && pip install --no-cache-dir -r requirements.txt && mkdir logfiles tmp

EXPOSE 8080
VOLUME ["/persist", "/home/app/staticfiles"]

ENTRYPOINT ["bash", "/entrypoint.bash"]
