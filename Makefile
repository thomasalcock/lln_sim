IMAGE_BASE ?= talcock90/lln-simulator
VERSION ?= v0.1.0_1018859444
IMAGE = $(IMAGE_BASE):$(VERSION)
CONTAINER ?= lln

stop:
	docker stop $(CONTAINER)

build:
	docker build --no-cache -t $(IMAGE) .


run:
	docker run -d --name $(CONTAINER) -p 8501:8501 $(IMAGE)


rm:
	docker rm -f $(CONTAINER)

it:
	docker exec -it $(CONTAINER) bash

prune:
	docker rmi -f $(IMAGE)
	docker rmi $(shell docker images -f "dangling=true" -q)


debug:
	docker run --rm -it $(IMAGE) bash
