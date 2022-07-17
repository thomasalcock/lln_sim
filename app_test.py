from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os, docker

app_container = os.getenv("APP_CONTAINER", "lln")
app_repo = os.getenv("APP_IMAGE", "talcock90/lln-simulator")
app_tag = os.getenv("APP_TAG", "v1.0_1977005258")
app_image = f"{app_repo}:{app_tag}"

selenium_container = os.getenv("SELENIUM_FIREFOX_CONTAINER", "selenium-firefox")
selenium_repo = os.getenv("SELENIUM_FIREFOX_IMAGE", "selenium/standalone-firefox")
selenium_tag = os.getenv("SELENIUM_TAG", "102.0")
selenium_image = f"{selenium_repo}:{selenium_tag}"

app_network = os.getenv("APP_NETWORK", "app-network")
client = docker.from_env()
local_images = client.images.list()
local_networks = client.networks.list()

print("Check if network exists")
if not any([obj.attrs.get("Name") == app_network for obj in local_networks]):
   print(f"{app_network} does not exist on host, creating network with bridge driver")
   client.networks.create(name = app_network, driver="bridge")
else:
   print(f"Network {app_network} already exists")

print(f"Check if app image {app_image} exists")
if not [obj.attrs.get("RepoTags")[0] == app_image for obj in local_images]:
   print(f"Pulling image {app_image}")
   client.images.pull(repository = app_repo, tag = app_tag)
else:
   print(f"Image {app_image} already exists")

print(f"Check if app image {selenium_image} exists")
if not [obj.attrs.get("RepoTags")[0] == selenium_image for obj in local_images]:
   print(f"Pulling image {selenium_image}")
   client.images.pull(repository = app_repo, tag = app_tag)
else:
   print(f"Image {selenium_image} already exists")


if client.containers.list(filters = {"name": app_container}) == []:
   print(f"Container {app_container} not running")
   print(f"Starting {app_container} from image {app_container}")
   client.containers.run(
      image = app_image, 
      detach = True,
      name = app_container, 
      network = app_network,
      ports = {"8501":"8501"}
   )
else:
   print(f"{app_container} is already running, performing health check")
   status = client.containers.get(app_container).attrs.get("State").get("Status")
   print(f"{app_container} has status: {status}")

if client.containers.list(filters = {"name": selenium_container}) == []:
   print(f"Container {selenium_container} not running")
   print(f"Starting {selenium_container} from image {selenium_image}")
   client.containers.run(
      image = selenium_image, 
      detach = True,
      name = selenium_container, 
      network = app_network,
      ports = {
         "4444":"4444",
         "7900":"7900"
      },
      shm_size = "2g"
   )
else:
   print(f"{selenium_container} is already running, performing health check")
   status = client.containers.get(app_container).attrs.get("State").get("Status")
   print(f"{selenium_container} has status: {status}")


print("Setup selenium driver")
driver = webdriver.Remote(
   command_executor='http://127.0.0.1:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.FIREFOX
)

print("Get app network ip")
app_network_ip = client.containers \
   .get(app_container).attrs \
   .get("NetworkSettings") \
   .get("Networks") \
   .get(app_network) \
   .get("IPAddress")

print(f"Use driver with {app_network_ip}")
driver.get(f"http://{app_network_ip}:8501/")
print(f"App title: {driver.title}")

# TODO: wait for app to load before interacting with it
# TODO: test basic functionality of app

print("Take screenshot of app")
with open("screenshots/sc.png", "wb") as f:
   f.write(driver.get_screenshot_as_png())

driver.quit()

print(f"Shutting down container {app_container}")
client.containers.get(app_container).remove(force=True)

print(f"Shutting down container {selenium_container}")
client.containers.get(selenium_container).remove(force=True)