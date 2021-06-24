FROM python:3

WORKDIR /app

ARG GITHUB_PAT=abcde
ARG ALM_CLIENT_ID=abcde
ARG ALM_CLIENT_SECRET=abcde

ENV GITHUB_PAT=$GITHUB_PAT
ENV ALM_CLIENT_ID=$ALM_CLIENT_ID
ENV ALM_CLIENT_SECRET=$ALM_CLIENT_SECRET

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]