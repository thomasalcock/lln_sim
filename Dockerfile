# "Compile" image build stage
FROM python:3.9.5-slim-buster AS base

RUN mkdir /src
WORKDIR /src

# create new virtual env
ENV VIRTUAL_ENV=/src/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt


# Runtime image build stage
FROM python:3.9.5-slim-buster
RUN mkdir /src
WORKDIR /src

# Copy venv installed packages from build stage
# TODO: fix bug since site packages are not copied 
COPY --from=base /src/venv /src/venv/

COPY metric_stabilization_plot.py /src/metric_stabilization_plot.py
COPY metric_stabilization_plot_test.py /src/metric_stabilization_plot_test.py
COPY utils.py /src/utils.py
COPY app.py /src/app.py

# make 
ENV PATH="/src/venv/bin:$PATH"

EXPOSE 8051

CMD ["streamlit", "run", "app.py"]