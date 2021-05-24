IMAGE_BASE=lln_simulator
VERSION=0.1.0
IMAGE=$(IMAGE_BASE):$(VERSION)
CONTAINER=lln


build:
	DOCKER_BUILDKIT=1 docker build -t $(IMAGE) .


run:
	docker run -d --name $(CONTAINER) -p 8501:8501 $(IMAGE)


rm:
	docker rm -f $(CONTAINER)

it:
	docker exec -it $(CONTAINER) bash

prune:
	docker rmi $(shell docker images -f "dangling=true" -q)