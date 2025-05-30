FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /application
# Install the application dependencies.
RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --all-groups --frozen

# Copy application code
COPY app/ /application/app

ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd nonroot \
    && useradd -u ${USER_UID} -g nonroot -m -s /bin/zsh nonroot
USER nonroot

ENV PATH="/application/.venv/bin:${PATH}"
WORKDIR /application/app
ENV PYTHONPATH=/application/app

CMD ["uv","run", "main.py"]