FROM public.ecr.aws/lambda/python:3.13

RUN pip install --no-cache-dir -r requirements.txt

COPY /entrypoints/app.py .

CMD ["app.lambda_handler"]