from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver


class MyWebElement(WebElement):
    def __init__(self, parent: WebDriver, id_: str) -> None:
        self.driver = parent
        self.id_ = id_
        super().__init__(parent, id_)

    def testt(self):
        return self.screenshot_as_png
