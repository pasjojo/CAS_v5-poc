CONTAINER_NAME=python-cas-1
IMAGE=apca/python-cas
VERSION=1.0

build:
	docker build -t ${IMAGE}:${VERSION} .

build-no-cache:
	docker build --no-cache -t ${IMAGE}:${VERSION} .

run:
	docker run --rm --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE}:${VERSION}

ip:
	docker inspect --format='http://{{.NetworkSettings.Networks.bridge.IPAddress}}:5000' ${CONTAINER_NAME}
