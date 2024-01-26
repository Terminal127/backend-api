FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application files to the container
COPY . .

RUN pip install -r ./requirements.txt

# Expose the default Flask port
EXPOSE 3000

# Run the Flask application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
