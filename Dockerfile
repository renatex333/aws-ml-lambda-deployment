FROM public.ecr.aws/lambda/python:3.10

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy function code
COPY src/lambda_function.py ${LAMBDA_TASK_ROOT}

# Copy model and encoder
COPY models/ ${LAMBDA_TASK_ROOT}/models/

# Install system dependencies
RUN yum install -y libstdc++ cmake gcc-c++ && \
    yum clean all && \
    rm -rf /var/cache/yum

# Install the specified packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.predict" ]