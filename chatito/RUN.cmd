docker build -t chatito .
docker run -v %cd%/data:/app/data -v %cd%/output:/app/result -it chatito