# Use an official Python runtime as a parent image
FROM python:3.10-slim as build
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
	      build-essential gcc 

# Set the working directory to /app
WORKDIR /usr

# Create an virtual environment
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.10-slim
RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python
RUN mkdir /usr/app && chown python:python /usr/app
WORKDIR /usr/app

# Copy the venv from the build stage
COPY --chown=python:python --from=build /usr/app/venv ./venv
# Copy the current directory contents into the container
COPY --chown=python:python . .

USER 999

# Use the virtual environment
ENV PATH="/usr/app/venv/bin:$PATH"

# Make port 5000 available to the world outside this container
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app.py when the container launches
CMD ["streamlit", "run", "streamlitPrototype.py" , "--server.port=8501", "--server.address=0.0.0.0"]
