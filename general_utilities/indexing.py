def index_get(value, data):
    index_f_val = []
    index_p_val = []

    f_val = value[1]
    p_val = value[0]

    data = [*zip(*data)]
    feature = data[1]
    parameter = data[0]

    for i in range(len(feature)):
        if feature[i] == f_val:
            index_f_val.append(i)

    if len(index_f_val) == 0:
        pass
    else:
        for j in range(len(index_f_val)):
            check = index_f_val[j]
            if parameter[check] == p_val:
                index_p_val.append(check)

    return index_p_val
