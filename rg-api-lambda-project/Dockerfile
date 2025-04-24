FROM public.ecr.aws/lambda/python:3.12 as dev
LABEL maintainer="Rahul Gangadharan <rahul.gangadharan@transformco.com>"
LABEL purpose="rg test docker file for api-lambda"
COPY . ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

FROM public.ecr.aws/lambda/python:3.12
COPY --from=dev ${LAMBDA_TASK_ROOT}/src ${LAMBDA_TASK_ROOT}/src
COPY --from=dev ${LAMBDA_TASK_ROOT}/requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install -r requirements.txt
CMD [ "src.index.lambda_handler" ]