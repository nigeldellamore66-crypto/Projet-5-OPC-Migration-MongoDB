FROM python:3.11-bullseye

WORKDIR /app

# Mise à jour pip/setuptools/wheel
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip install --prefer-binary -r prerequis.txt

COPY . .


CMD ["python","-m", "src.run"]
