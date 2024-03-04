FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc g++

COPY app/requirements.txt /
RUN pip install -r /requirements.txt

RUN apt-get remove -y gcc g++
RUN apt-get -y autoremove

RUN groupadd -r nonroot && useradd --no-log-init --create-home --system --shell /bin/bash --gid nonroot nonroot
COPY ./app /app
RUN chmod +x /app/start.sh
RUN chown -R nonroot:nonroot /app
RUN chmod 755 /app
USER nonroot
WORKDIR /app/
ENV PYTHONPATH=/app
EXPOSE 8888
# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["bash","-x","start.sh"]