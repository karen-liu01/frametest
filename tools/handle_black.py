# 处理下找元素时候发生的找不到的异常
# 一般找不到的情况：
# 1.出现弹框，需要将弹框叉掉
# 2.页面有历史记录，遮挡住了元素，点击下其他地方
from functools import wraps


def handle_black(func):
    # @wraps  如果装饰这个会报错
    def wrapper(*args, **kwargs):
        # 需要内部引入，否则到了basepage界面又需要引入handle_black，会报错循环引入
        from frametest.page.base_page import BasePage
        # instances是第一个参数self，也就是加了装饰器的函数func的对象本身
        instance: BasePage = args[0]
        try:
            # 如果没有问题，就把函数的执行结果返回去，并且设置下，找元素报错的次数为0
            result = func(*args, **kwargs)
            instance.error_count = 0
            return result
        except Exception as e:
            if instance.error_count > instance.max_num:
                raise e
            instance.error_count += 1
            # 遍历黑名单中的处理办法
            for black_ele in instance.black_list:
                ele = instance.driver.find_elements(*black_ele)
                if len(ele) > 0:
                    ele[0].click()
                    # 黑名单处理完成，再调用下wrapper去看是否还有异常
                    instance.driver.implicitly_wait(5)
                    return wrapper(*args, **kwargs)
            raise e

    # return的时候不能带括号，否则会报错，装饰器的固定写法
    return wrapper
