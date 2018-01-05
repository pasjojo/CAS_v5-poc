CONTAINER_NAME=apache-cas-1
IMAGE=apca/apache-cas-client
VERSION=1.0

build:
	docker build -t ${IMAGE}:${VERSION} .

run:
	docker run --rm --name ${CONTAINER_NAME} ${IMAGE}:${VERSION}

ip:
	docker inspect --format='http://{{.NetworkSettings.Networks.bridge.IPAddress}}' ${CONTAINER_NAME}
