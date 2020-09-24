Follow the instructions at: 
https://dev.to/sahilrajput/install-flask-and-create-your-first-web-application-2dba
to setup a virtual environment to run Flask in. 

Following this:
1. Place the flaskr folder in the directory you created for the virtual environment.
2. Change global variables (explained in above link)
3. flask run 
  > if working, should report that the webapp is running on a loopback (127.0.0.1:5000), and can be accessed via browser.
  
  
  
Instructions for running on Docker:
To follow this, make sure you have Docker installed on your system.

1. Run "make" on the terminal to create the docker image.
2. Run "make run" to start the server.
3. Now you can go on browser and goto localhost:8000 and page will show.

NOTE: In the makefile you can change the host port to whatever you want.

   Alternative commands for building & running dockerized app:
   1. docker build --rm --tag="whatevername"
   2. docker run -p 0.0.0.0:"whatever_host_port":"docker_port"/tcp -it --rm "whatevername"
