import yaml


# 获取yaml中的数据,并且将需要的数据组装返回当参数
def get_datas():
    file = "../testdatas/deal_datas.yaml"
    with open(file, encoding="utf-8") as f:
        datas = yaml.safe_load(f)
    d = []
    case_name = []
    fuc_names = []
    # 拿到别名，方法名、目前先支持一个
    alias_name = list(datas.keys())[0]
    for j in range(0, len(datas[alias_name])):
        func_name = list(datas[alias_name].keys())[j]
        fuc_names.append(func_name)
        tmp = datas[alias_name][func_name]
        # print(len(tmp))
        n = len(tmp["ids_name"])
        # print(n)
        for i in range(0, n):
            d.append([func_name, tmp["request_data"][i], tmp["expect"][i]])
            case_name.append(tmp["ids_name"][i])

    return alias_name, fuc_names, case_name, d
