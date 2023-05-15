FROM python:3.11.1

# Set the working directory
WORKDIR /app

# Install dependencies (using pip)
COPY requirements.txt app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r app/requirements.txt

# Copy the application code
COPY ./src /src
COPY ./tests /tests

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0" , "--port", "8000" , "--reload"]
