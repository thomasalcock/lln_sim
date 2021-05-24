FROM python:3.9.5-slim-buster
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt
COPY metric_stabilization_plot.py /src/metric_stabilization_plot.py
COPY metric_stabilization_plot_test.py /src/metric_stabilization_plot_test.py
COPY utils.py /src/utils.py
COPY app.py /src/app.py
EXPOSE 8051
CMD ["streamlit", "run", "app.py"]