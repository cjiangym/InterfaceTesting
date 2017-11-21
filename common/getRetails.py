import requests


def get_Retails(self):
    base_url_search = self.sheet2.cell_value (6, 2)  # 搜索促销商店
    params_search = {
        "districtid": "-2",  # 默认值
        "shoptypeid": "-1",  # 默认值
        "townid": "-2",  # 默认值
        "distance": "",
        "cityid": self.sheet2.cell_value (6, 5),
        "lon": self.sheet2.cell_value (6, 7),
        "lat": self.sheet2.cell_value (6, 8),
        "nextpage": "",
        "keyword": self.sheet2.cell_value (6, 6),
        "userid": self.sheet2.cell_value (6, 4)
    }
    response_search = requests.get (base_url_search, params=params_search)
    return response_search