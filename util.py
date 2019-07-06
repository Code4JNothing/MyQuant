"""
常用公共函数
"""


def stock_code_change(code):
    """
    添加股票代码标识，如6000000.SH、0000001.SZ分表标识上证、深证
    :param code: 六位股票代码
    :return: 添加沪深标识后缀的股票代码
    """
    code = code.strip()
    if code.isdigit() and len(code) == 6:
        if str(code).startswith('6'):
            return str(code) + '.SH'
        else:
            return str(code) + '.SZ'

