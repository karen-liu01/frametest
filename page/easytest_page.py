from time import sleep

import pytest
from selenium.webdriver.common.by import By

from jsf_interface.page.base_page import BasePage


class EasyTestPage(BasePage):
    """
    实现的功能：在easytest平台，使用UI自动化实现模拟接口自动化，测对应的jsf接口
    后续要优化的点：
    1.实现数据驱动
    2.实现步骤驱动
    """
    # easytest平台测试jsf接口的url地址，一定要放在外面，这样初始化的时候才会打开这个地址
    base_url = "http://easytest.com/"

    # 必须登录，不登录的话，加载出来的页面是花的，无法定位到需要的元素，有问题
    # @pytest.fixture()
    def login(self):
        # 输入用户名、密码进行登录
        self.find(By.ID, "username").send_keys("zhangsan")
        self.find(By.ID, "password").send_keys("123456")
        self.find(By.CSS_SELECTOR, ".formsubmit_btn").click()
        sleep(3)
        self.driver.get("http://easytest.com/XXX")

    # 添加装饰器，在执行这个方法之前执行登录方法  目前无法使用
    # @pytest.mark.usefixtures("login")
    def show_detail(self):
        # 先用接口和别名把方法名称列表找出来，再完成下一步
        # 这块一会用driver传递优化一下
        self.basic_data = [{"keya": "aaa"}]
        for i in range(0, len(self.basic_data)):
            for k, v in self.basic_data[i].items():
                # 输入方法名
                self.find(By.ID, "interfaceName").send_keys(k)
                # 点击页面的其他位置 避免有页面遮挡
                # self.find(By.XPATH, "/html/body/div[2]/h4").click()
                # sleep(2)
                # 通过文字去定位,点击解析接口
                # self.find_by_text('//*[text()="解析接口"]').click()
                sleep(2)
                self.find(By.XPATH, '//*[text()="解析接口"]').click()
                sleep(2)
                # 输入别名
                self.find(By.ID, "group").send_keys(v)
                # 输入别名后，会自动将页面加载出来，给个加载时间
                # sleep(5)
                # 将页面的滑动条滑动到最下面，下面这条语句可用
                # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # 点击方法名称输入框，将对应的方法名输入,然后点击搜索框中出现的li，触发解析，开始测试
                self.find(By.ID, "s2id_methodName").click()
                sleep(3)
                # self.find(By.XPATH, '//*[@id="s2id_methodName"]/a').click()
                # self.find(By.CSS_SELECTOR, ".select2-input").send_keys("tt")
                # sleep(3)
                # self.find(By.XPATH, '//*[@id ="select2-drop"]/ul/li[1]').click()

    # 将request_data传过来就行，方法将响应返回了，可以用于断言
    def send_request(self, func_name, data):
        # 实现的功能：
        # 1.为了兼容不同的方法，要先在下拉框中出入方法名，然后再输入参数  2.点击调用接口 3.拿到返回值，并且返回
        # 找到方法名,判断和传入的是否一致，一致就继续执行后面的代码，不一致，换成新得方法名
        a = self.find(By.ID, "s2id_methodName").text
        print(a)
        print(func_name)
        if a != func_name:
            # 下拉框需要用这种方式去解决，先在下拉框输入方法名
            # self.find(By.ID, "s2id_methodName").clear()
            element = self.driver.find_element(By.XPATH, f"//*[text()='{func_name}']")
            print(element.text)
            element.click()
        # self.driver.execute_script("arguments[0].click", element)
        sleep(2)
        # 先将参数输入框清空，然后再输入
        self.find(By.ID, "params").clear()
        self.find(By.ID, "returnValue").clear()
        self.find(By.ID, "params").send_keys(f'{data}')
        sleep(2)
        self.find_by_text('//*[text()="调用接口"]').click()
        sleep(10)
        #  这个地方可以封装一个显示等待，等待响应中有内容出现
        responese_data = self.find(By.ID, "returnValue").text
        res = responese_data.replace('\n', '').replace(' ', '').replace('\"', '').strip()
        # print(res)
        # print("*****")
        # print(type(res))
        # print("*****")
        return res

    def jiexi(self):
        # 测试下解析接口的这种定位方式行不行
        sleep(2)
        self.find(By.ID, "params").send_keys(1111)
        sleep(5)
        self.find_by_text('//*[text()="调用接口"]').click()
        sleep(3)
        responese_data = self.find(By.ID, "returnValue").text
        print(responese_data)
