docker build -t chatito .
docker run -v %cd%/data:/app/data -v %cd%/output:/app/results -it chatito
python convert.py
notepad NLU-Data.md