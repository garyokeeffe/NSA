FROM public.ecr.aws/lambda/python:3.8

#WORKDIR ${LAMBDA_TASK_ROOT}

# Update package list and install build dependencies
RUN yum install -y \
    pkgconfig \
    gcc \
    make \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install wheel
RUN /var/lang/bin/python3.8 -m pip install --upgrade pip
RUN pip install wheel

# Add the current directory contents into the container at /app
COPY ./app/ ${LAMBDA_TASK_ROOT}

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN pip install awslambdaric --target "${LAMBDA_TASK_ROOT}"


# Setting environment variables
ENV NOSTR_PRIVATE_KEY="placeholder nsec"
RUN chmod -R 755 ${LAMBDA_TASK_ROOT}

# Run gunicorn when the container launches
CMD [ "app.handler" ]


