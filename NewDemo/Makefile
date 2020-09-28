APP=oauth_session_fixation
APP_PORT= 5000
HOST_PORT= 5000

all: build

# This build only installs python requirements and is only required to build once
# This should be used with "make runv"
build:
	docker build --file ./DockerfileFast --rm --tag=$(APP) .

# This build copies whole Oauth source code into container and builds
slow:
	docker build --file ./DockerfileSlow --rm --tag=$(APP) .
	
# Mounts source code to container when begin running container
# Do not need to rebuild container if using this
# Everytime change code just stop current docker and run this again	
run:
	docker run -v $(PWD)/OauthDemo/:/vulnerable_oauthapp/OauthDemo/ -p 0.0.0.0:$(HOST_PORT):$(APP_PORT)/tcp -it --rm $(APP) sh

# The default cmd for running container
start:
	docker run -p 0.0.0.0:$(HOST_PORT):$(APP_PORT)/tcp -it --rm $(APP)



clean:
	docker image rm $(APP)
	docker system prune
