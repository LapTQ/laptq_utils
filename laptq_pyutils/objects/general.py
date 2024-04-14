class ListAligner:

    def __init__(self, list__key: list):

        self._dict__result = {key: [] for key in list__key}
        self._num = 0

    def __len__(self):
        return self._num

    def _check__keys(self, other: dict):

        assert set(self._dict__result.keys()) == set(
            other.keys()
        ), "Keys mismatch: \n\t+ Existing keys: {}\n\t+ New keys: {}".format(
            set(self._dict__result.keys()), set(other.keys())
        )

    def append(self, dict__result: dict):
        """Append single element"""

        # assert
        self._check__keys(dict__result)

        for key, value in dict__result.items():
            self._dict__result[key].append(value)

        self._num += 1

    def extend(self, dict__result: dict):

        # assert
        self._check__keys(dict__result)
        assert (
            len(set(len(_) for _ in dict__result.values())) == 1
        ), "Number of elements between fields must be the same"

        for key, value in dict__result.items():
            self._dict__result[key].extend(value)

        self._num += len(value)

    def get__key(self, key: str):
        return self._dict__result[key]

    def get__index(self, i: int):
        return {key: value[i] for key, value in self._dict__result}

    def pop__indexes(self, list__index__to_pop: list):
        """Remove a list of indexes."""

        list__index__to_keep = [
            _ for _ in range(self._num) if _ not in list__index__to_pop
        ]
        for key, value in self._dict__result.items():
            self._dict__result[key] = [value[_] for _ in list__index__to_keep]

        self._num = len(list__index__to_keep)

    def item(self):
        return self._dict__result

    @staticmethod
    def from_dict(dict__result: dict):

        list__key = list(dict__result.keys())
        list_aligner = ListAligner(list__key=list__key)
        list_aligner.extend(dict__result=dict__result)

        return list_aligner

    def add__key(self, key: str, value: list):

        assert key not in self._dict__result, "Key already exists"
        assert len(value) == self._num, "Number of elements mismatch"

        self._dict__result[key] = value
