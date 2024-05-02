def flatten(lis):
    _list = []
    for item in lis:
        if type(item) == list:
            item = flatten(item)
            for i in item:
                _list.append(i)
        else:
            _list.append(item)
    return _list