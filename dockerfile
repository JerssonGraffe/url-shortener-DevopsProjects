FROM public.ecr.aws/lambda/python:3.13

COPY /entrypoints/app.py .

CMD ["app.lambda_handler"]