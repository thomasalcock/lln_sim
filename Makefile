IMAGE_BASE ?= talcock90/lln-simulator
VERSION ?= v1.0_1977005258
IMAGE = $(IMAGE_BASE):$(VERSION)
CONTAINER ?= lln

SELENIUM_IMAGE ?= selenium/standalone-firefox:102.0
SELENIUM_CONTAINER = selenium-firefox

NETWORK = app-network

run:
	make run_app
	make run_sl

rm:
	make rm_app
	make rm_sl

run_sl:
	docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" \
		--network $(NETWORK) --name $(SELENIUM_CONTAINER) $(SELENIUM_IMAGE)

rm_sl:
	docker rm -f $(SELENIUM_CONTAINER)

stop_app:
	docker stop $(CONTAINER)

build_app:
	docker build --no-cache -t $(IMAGE) .


run_app:
	docker run -d --name $(CONTAINER) \
	--network $(NETWORK) -p 8501:8501 $(IMAGE)


rm_app:
	docker rm -f $(CONTAINER)

it_app:
	docker exec -it $(CONTAINER) bash

prune_app:
	docker rmi -f $(IMAGE)
	docker rmi $(shell docker images -f "dangling=true" -q)

debug_app:
	docker run --rm -it $(IMAGE) bash
