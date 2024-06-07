FROM python:3.11.1

WORKDIR /src

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock /src/

# Poetry & 종속성 설치
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

ENV TZ=Asia/Seoul

EXPOSE 18000

ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--host=0.0.0.0", "--port=18000", "--reload"]
