FROM alpine:3.18

# Opencontainers Specs (https://github.com/opencontainers/image-spec/blob/main/annotations.md)
LABEL org.opencontainers.image.title="VerbaCap"
LABEL org.opencontainers.image.description="Podcast Manager"
LABEL org.opencontainers.image.source="https://github.com/Mirio/verbacap"
LABEL org.opencontainers.image.licenses="MIT"

ARG USERNAME="app"

RUN apk add --no-cache bash ffmpeg python3 py3-pip && adduser -D -s "/bin/bash" "${USERNAME}"

USER "${USERNAME}"
COPY --chown="${USERNAME}:${USERNAME}" . "/home/${USERNAME}"
COPY "entrypoint.bash" "/entrypoint.bash"
WORKDIR "/home/${USERNAME}"

RUN python3 -m venv "/home/${USERNAME}/venv" && . "/home/${USERNAME}/venv/bin/activate" \
    && pip install --no-cache-dir -r requirements/local.txt

EXPOSE 8080
VOLUME ["/persist"]

ENTRYPOINT ["bash", "/entrypoint.bash"]
