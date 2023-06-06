import hashlib




class Proxy:

    def dynamic_ips(self, num: int = None):
        pass

    def alone_ip(self):
        pass


class JvLiang(Proxy):

    class JvLiangParams:
        """
        巨量IP代理内部参数类 （巨量IP 每天一千个免费IP 不用白不用 兄弟们！）
        用于定义巨量IP代理的内部参数
        """
        trade_no: str = '1765244755300652'  # 由巨量系统生成的业务编号，全局唯一。示例值：1765244755300652
        num: int = 1  # 获取数量 单次提取数量，目前最大单次提取数量为100。
        result_type: str = 'json'  # 接口返回内容的格式要求 text：文本格式[默认] json：json格式 xml: xml格式 示例值：json
        pt: int = None  # 提取IP支持的代理类型 1：HTTP代理[默认] 2：SOCK代理 示例值：2
        split: int = None  # 提取结果列表中每个结果的分隔符 1：\r\n分割 [默认] 2：\n分割 3：空格分割 4：|分割 示例值：3
        city_name: int = None  # 返回的数据中携带IP归属城市名称 不带此参数代表不过滤 固定值：1 示例：112.84.17.21:31114,江苏徐州
        city_code: int = None  # 返回的数据中携带IP归属城市邮政编码 不带此参数代表不过滤 固定值：1 示例：114.98.162.2:48581,340281
        ip_remain: int = None  # 返回的数据中携带IP剩余可用时长（秒） 不带此参数代表不过滤 固定值：1 示例：114.98.162.2:48581,281
        area: str = None  # 按照需求地区提取IP，支持多地区，用英文逗号分割 不带此参数代表不过滤 示例：北京,上海,广州
        no_area: str = None  # 排序指定地区的IP，支持多地区，用英文逗号分割 不带此参数代表不过滤 示例：深圳,南昌,武汉
        ip_seg: str = None  # 筛选以特定部分开头的IP 不带此参数代表不过滤 示例：114.98.,112.84.
        no_ip_seg: str = None  # 排除以特定部分开头的IP 不带此参数代表不过滤 示例：114.98.,112.84.
        isp: str = None  # 筛选以特定运营商提供的IP 不带此参数代表不过滤 可选值：电信，联通，移动 示例：电信
        filter: int = None  # 过滤今天提取过的IP 不带此参数代表不过滤 固定值：1

        def __init__(self, result_type: str = 'json', num: int = 1):
            self.result_type: str = result_type
            self.num: int = num

        def _get_not_none_attrs(self):
            return [attr for attr, value in self.__dict__.items() if value is not None]

        def gen_not_none_params(self):
            return {attr: getattr(self, attr) for attr in self._get_not_none_attrs()}

        def gen_sign(self, key: str = None):
            """
            生成签名
            :return:
            """
            if key is None:
                raise ValueError('key must be not None')
            param_list = [f'{attr}={getattr(self, attr)}' for attr in self._get_not_none_attrs()]
            param_list.sort(key=lambda x: x.split('=')[0])
            param_list.append(f'key={key}')
            return hashlib.md5('&'.join(param_list).encode('utf-8')).hexdigest()

    url: str = 'http://v2.api.juliangip.com/'  # 巨量IP代理API接口地址

    def __init__(self, jl_param: JvLiangParams = None, trade_no: str = None, key: str = None):
        self.jl_param = jl_param
        from util.request import Request
        self.req = Request()
        self.trade_no = trade_no
        self.key = key

    def dynamic_ips(self, num: int = None):
        dynamic_url = self.url + 'dynamic/getips'
        trade_no = self.trade_no
        if num: self.jl_param.num = num
        if trade_no:
            trade_no = self.jl_param.trade_no
            if trade_no: raise ValueError('trade_no must not be None')
        if self.key: raise ValueError('key must not be None')
        self.jl_param.trade_no = trade_no
        params = self.jl_param.gen_not_none_params()
        params['sign'] = self.jl_param.gen_sign(self.key)
        result = self.req.get_request(dynamic_url, params=params).json()
        if result['code'] != 200:
            raise ValueError(result['msg'])
        return result['data']['proxy_list']

    def alone_ip(self, trade_no: str = None, key: str = None):
        dynamic_url = self.url + 'alone/getips'
        if trade_no:
            trade_no = self.trade_no
            if trade_no is None:
                trade_no = self.jl_param.trade_no
            if trade_no is None:
                raise ValueError('trade_no must not be None')
        if key is None:
            key = self.key
            if key is None:
                raise ValueError('key must not be None')
        self.jl_param.trade_no = trade_no
        self.jl_param.num = None
        params = self.jl_param.gen_not_none_params()
        params['sign'] = self.jl_param.gen_sign(key)
        result = self.req.get_request(dynamic_url, params=params).json()
        if result['code'] != 200:
            raise ValueError(result['msg'])
        return result['data']


if __name__ == '__main__':
    res = JvLiang(JvLiang.JvLiangParams(), trade_no='1499339606099157', key='bfacd99488fa48168b00118021c68c4f')\
        .dynamic_ips()
    print(res)
