APP=oauth_session_fixation
APP_PORT= 5000
HOST_PORT= 5000

all: build

build:
	docker build --rm --tag=$(APP) .

run:
	docker run -p 0.0.0.0:$(HOST_PORT):$(APP_PORT)/tcp -it --rm $(APP)

clean:
	docker image rm $(APP)
	docker system prune
