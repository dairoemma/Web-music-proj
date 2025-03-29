# using official python runtime as the base image
FROM python:3.12

# set the working directory
WORKDIR /app

# copy the requirements.txt file
COPY requirements.txt .

#install all the dependencies in requiremnts.txt
RUN pip install --no-cache-dir -r requirements.txt

#copy the installed dependencies
COPY . .
#expose the 5000 port that the app.py should run on
EXPOSE 5000
ENV PYTHONUNBUFFERED=1

#install gunicorn eventlet for socket event
RUN pip install gunicorn eventlet

#run the app.py
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "app:app", "-b", "0.0.0.0:5000"]