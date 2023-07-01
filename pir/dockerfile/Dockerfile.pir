FROM ubuntu:latest

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip git

# Clone the repository and install requirements
RUN git clone https://github.com/casafurix/PIR-Sensor-Ditto.git && \
    cd pir-sensor-ditto/requirements && \
    chmod +x install_requirements.sh && \
    bash ./install_requirements.sh && \
    cd ..

# Go to the dir of the script
WORKDIR /app/pir-sensor-ditto/pir/

# Run the script
CMD ["python3", "send_data_rpi_pir.py"]