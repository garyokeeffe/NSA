FROM public.ecr.aws/lambda/python:3.8

# Update package list, install build dependencies, upgrade pip, and install wheel
RUN yum install -y \
    pkgconfig \
    gcc \
    make \
    && rm -rf /var/lib/apt/lists/* \
    && /var/lang/bin/python3.8 -m pip install --upgrade pip \
    && pip install wheel

# Add the current directory contents into the container at /app
COPY ./app/ ${LAMBDA_TASK_ROOT}

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}" \
    && pip install awslambdaric --target "${LAMBDA_TASK_ROOT}"

# Setting environment variables
RUN chmod -R 755 ${LAMBDA_TASK_ROOT}

# Run gunicorn when the container launches
CMD [ "app.handler" ]



