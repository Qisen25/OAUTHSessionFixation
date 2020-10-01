APP=oauth_session_fixation
PROV=our_dodgy_provider
APP_PORT= 5000
HOST_PORT= 5000

all: build

# This build only installs python requirements and is only required to build once
# This should be used with "make runv"
build:
	docker build --file ./DockerfileFast --rm --tag=$(APP) .
	docker build --file ./steves_dodgy_oauth_provider/DockerfileFast --rm --tag=$(PROV) .

# This build copies whole Oauth source code into container and builds
slow:
	docker build --file ./DockerfileSlow --rm --tag=$(APP) .
	docker build --file ./steves_dodgy_oauth_provider/DockerfileSlow --rm --tag=$(PROV) .
	
# Mounts source code to container when begin running container
# Do not need to rebuild container if using this
# Everytime change code just stop current docker and run this again	
run:
	docker run -v "$(PWD)/steves_dodgy_oauth_provider/DodgyProvider/:/vulnerable_oauthapp/Provider/" --network host -p 0.0.0.0:8001:8001/tcp -d --name $(PROV) --rm $(PROV)
	docker run -v "$(PWD)/OauthDemo/:/vulnerable_oauthapp/OauthDemo/" --network host -p 0.0.0.0:$(HOST_PORT):$(APP_PORT)/tcp -it --name $(APP) --rm $(APP) sh
	
	

# The default cmd for running container
start:
	docker run -p 0.0.0.0:$(HOST_PORT):$(APP_PORT)/tcp -it --rm $(APP)

stop:
	docker stop $(PROV)
	#docker stop $(APP)
	
clean:
	docker image rm $(APP)
	docker image rm $(PROV)
	docker system prune
