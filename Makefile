IMAGE_BASE ?= lln_simulator
VERSION ?= 0.2.0
IMAGE = $(IMAGE_BASE):$(VERSION)
CONTAINER ?= lln


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