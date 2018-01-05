CONTAINER_NAME=apache-cas-2
IMAGE=apca/apache-cas-client
VERSION=1.1

build:
	docker build -t ${IMAGE}:${VERSION} .

build-no-cache:
	 docker build --no-cache -t ${IMAGE}:${VERSION} .
run:
	docker run --rm --name ${CONTAINER_NAME} ${IMAGE}:${VERSION}

ip:
	docker inspect --format='http://{{.NetworkSettings.Networks.bridge.IPAddress}}' ${CONTAINER_NAME}
