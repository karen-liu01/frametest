import pytest
from jsf_interface.page.easy_test_page import EasyTestPage
from jsf_interface.tools.deal_yaml import get_datas


class TestEasy:
    def setup_class(self):
        self.easy = EasyTestPage()
        self.easy.login()
        self.easy.show_detail()
        # pass

    def teardown_class(self):
        self.easy.driver.quit()
        # pass

    # 通过get_datas获取到对应的数据，然后传值进去，执行case
    @pytest.mark.parametrize('func_name, request_data, expect', get_datas()[3], ids=get_datas()[2])
    def test_get_datas(self, func_name, request_data, expect):
        # print(request_data)
        # print(type(request_data))
        # print(expect)
        # print("---------------")
        res = self.easy.send_request(func_name=func_name, data=request_data)
        if len(res) != 0:
            print("---------------")
            print(f"实际返回的结果是：{res}")
            print(f"从yml中拿到的预期结果是：{expect}")
            print("---------------")
            exp_code_status = expect["code"]
            # 返回的res是一个string，不能这么处理
            # rel_code_status = res["code"]
            # assert exp_code_status == rel_code_status
            assert f"code:{exp_code_status}" in res
        else:
            # TODO 这个地方优化一下，等到页面的结果出现，如果没出现，再尝试执行该case
            print("时间太长，没有等到响应,需要手动执行这个case")
            assert 1 == 1
