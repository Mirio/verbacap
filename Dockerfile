FROM alpine:3.18

# Opencontainers Specs (https://github.com/opencontainers/image-spec/blob/main/annotations.md)
LABEL org.opencontainers.image.title="VerbaCap"
LABEL org.opencontainers.image.description="Podcast Manager"
LABEL org.opencontainers.image.source="https://github.com/Mirio/verbacap"
LABEL org.opencontainers.image.licenses="MIT"

ARG USERNAME="app"
ARG GITCLIFF_VERSION="1.4.0"
COPY nginx.conf /etc/nginx/nginx.conf

RUN apk add --no-cache bash ffmpeg python3 py3-pip nginx sudo wget && adduser -D -s "/bin/bash" "${USERNAME}" \
    && echo "app ALL = NOPASSWD: /bin/chown,/usr/sbin/nginx" > /etc/sudoers.d/app && chmod 400 /etc/sudoers.d/app \
    && chown -R app:app /var/lib/nginx && chown app:app /var/log/nginx && cd /tmp \
    && wget -q -O "gitcliff.tar.gz" "https://github.com/orhun/git-cliff/releases/download/v${GITCLIFF_VERSION}/git-cliff-${GITCLIFF_VERSION}-x86_64-unknown-linux-musl.tar.gz" \
    && tar xfz "gitcliff.tar.gz" && mv "git-cliff-${GITCLIFF_VERSION}/git-cliff" /usr/local/bin/ && rm -rf "git-cliff-${GITCLIFF_VERSION}" "gitcliff.tar.gz"

USER "${USERNAME}"
COPY . "/home/${USERNAME}"
COPY "entrypoint.bash" "/entrypoint.bash"
WORKDIR "/home/${USERNAME}"

RUN python3 -m venv "/home/${USERNAME}/venv" && . "/home/${USERNAME}/venv/bin/activate" \
    && pip install --no-cache-dir -r requirements.txt && mkdir logfiles tmp

EXPOSE 8080
VOLUME ["/persist", "/home/app/staticfiles"]

ENTRYPOINT ["bash", "/entrypoint.bash"]
