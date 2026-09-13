import pytest
from selenium import webdriver

from utilities.custom_logger import Log_Maker

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                      help="Specify the browser: chrome or firefox or edge")

@pytest.fixture()
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(params=["chrome", "firefox", "edge"])
def setup(request):
    browser = request.param
    global driver
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError("Unsupported browser")
    return driver

def pytest_configure(config):
    logger = Log_Maker.log_gen()
    logger.info("=== Test session started ===")

def pytest_sessionfinish(session, exitstatus):
    logger = Log_Maker.log_gen()
    logger.info(f"=== Test session finished with exit status {exitstatus} ===")

def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        driver = item.funcargs.get("setup")
        if driver:
            driver.save_screenshot(f"screenshots/{item.name}.png")

def pytest_collection_modifyitems(items):
    # Example: run smoke tests first
    items.sort(key=lambda item: "smoke" not in item.keywords)