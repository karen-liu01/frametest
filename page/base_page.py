from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from frametest.tools.handle_black import handle_black


class BasePage:
    """
    基类的功能:
    1.初始化driver  放在init中，只要继承调用，就会初始化或者传递
    2.初始化查找方法   先分成find和finds两个方法
    3.便于不同page之间传递driver
    4.后续看下，driver要不要写成内部变量，不允许外部修改
    5.封装显式等待
    """
    base_url = ""
    # 定义成空列表，每增加一对接口名和别名，就append进去，便于easytest平台取数据
    basic_data = []
    # 处理异常需要的参数
    # black_list 的第一个参数是页面的顶部位置，点一下防止页面遮挡； 第二个是弹框的位置确认按钮  第三个是弹框的X按钮
    black_list = [(By.XPATH, "/html/body/div[2]/h4") ]
    error_num = 0
    max_num = 5

    def __init__(self, driver: WebDriver = None):
        # 处理driver
        if driver is None:
            self.driver = webdriver.Chrome()
        else:
            self.driver = driver
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

        # 将url放在基类中，子类可以赋值，然后初始化的时候就可以打开对应的界面

        if self.base_url != "":
            self.driver.get(url=self.base_url)

    # 先写两个查找方法，后续再优化
    @handle_black
    def find(self, by, locator=None):
        if locator is None:
            result = self.driver.find_element(*by)
        else:
            result = self.driver.find_element(by, locator)
        return result

    @handle_black
    def finds(self, by, locator=None):
        if locator is None:
            result = self.driver.find_elements(*by)
        else:
            result = self.driver.find_elements(by, locator)
        return result

    # @handle_black
    def find_by_text(self, locator):
        return self.driver.find_element_by_xpath(locator)

    # TODO 显示等待，找时间再封装,后续把sleep强制等待都去掉，变成显示等待
    def wait_until_click(self, locator, timeout=10):
        element: WebElement = WebDriverWait(self.driver, timeout).until(
            expected_conditions.element_to_be_clickable(locator))
        return element
