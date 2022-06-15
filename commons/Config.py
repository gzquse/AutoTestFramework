
import configparser
import os


def get_config(selector):
    """
    读取配置文件的方法
    :param selector: selcetor = 'str', selector = 'options.item'
    :return:
    """
    conf = configparser.ConfigParser()
    # 获取当前文件所在的目录
    # print(__file__)
    curr_path = os.path.dirname(os.path.realpath(__file__))
    # print(curr_path)
    config_path = os.path.join(curr_path, "config.ini")
    # print(config_path)
    conf.read(config_path, encoding='utf-8')

    if '.' in selector:
        # conf.get('options', 'url')  # 'opitons.url'
        return conf.get(selector.split('.')[0], selector.split('.')[1])
    else:
        # conf.items('database')
        return conf.items(selector)


if __name__ == '__main__':
    print(get_config('database'))
    # print(get_config('options.url'))
