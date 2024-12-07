class ListAligner:

    def __init__(self, **kwargs):

        list__key: list = kwargs["list__key"]

        self._dict__result = {key: [] for key in list__key}
        self._num = 0

    def __len__(self):
        return self._num

    def append(self, **kwargs):

        dict__result: dict = kwargs["dict__result"]

        assert set(self._dict__result.keys()) == set(
            dict__result.keys()
        ), "Keys mismatch: \n\t+ Existing keys: {}\n\t+ New keys: {}".format(
            set(self._dict__result.keys()), set(dict__result.keys())
        )
        assert (
            len(set(len(_) for _ in dict__result.values())) == 1
        ), "Number of elements between fields must be the same"

        for key, value in dict__result.items():
            self._dict__result[key].extend(value)

        self._num += len(value)

    def get_key(self, **kwargs):

        key: str = kwargs["key"]

        return self._dict__result[key]

    def pop__indexes(self, **kwargs):
        """Remove a list of indexes."""

        list__index__to_pop: list = kwargs["list__index__to_pop"]

        list__index__to_keep = [
            _ for _ in range(self._num) if _ not in list__index__to_pop
        ]
        for key, value in self._dict__result.items():
            self._dict__result[key] = [value[_] for _ in list__index__to_keep]

        self._num = len(list__index__to_keep)

    def item(self):
        return self._dict__result

    @staticmethod
    def from_dict(**kwargs):

        dict__result: dict = kwargs["dict__result"]

        list__key = list(dict__result.keys())
        list_aligner = ListAligner(list__key=list__key)
        list_aligner.append(dict__result=dict__result)

        return list_aligner
