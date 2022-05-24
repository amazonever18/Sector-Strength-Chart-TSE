from app.models.value import factory_value_class


# DBのデータをまとめて管理するデータフレームクラス
class DataFrameValue(object):

    def __init__(self, duration):
        self.duration = duration
        self.value_cls = factory_value_class(self.duration)
        self.values = []

    # 上記のリストにDBから取得したデータをセット
    def set_all_values(self, limit=1000):
        self.values = self.value_cls.get_all_values(limit)
        return self.values

    # データを辞書型にキャスト（フロントエンドに送る時に便利）
    @property
    def dict(self):
        return {
            'duration': self.duration,
            'values': [c.dict for c in self.values]
        }
