import numpy as np

coordinate_list = []


def read_file(path, read_header=False):
    f = open(path, "r+")
    rows = f.readlines()
    if not read_header:
        rows = rows[1:]
    cols = []
    for row in rows:
        col = str.split(row)
        if len(col) == 1:
            cols.append([int(col[0])])
        else:
            cols.append([int(c) for c in col])
    return cols


def write_file(path, header, data):
    f = open(path, "w+")
    if header is not None:
        row = ""
        for h in header:
            row += "\t" + h
        row = row[1:] + "\n"
        f.write(row)
    for cols in data:
        row = ""
        for col in cols:
            row += "\t" + str(col)
        row = row[1:] + "\n"
        f.write(row)
    f.close()


def set_value(matrix, value):
    global coordinate_list
    for coord in coordinate_list:
        matrix[coord[0], coord[1], 1] = value


def _4_recursive(matrix, x, y):
    cur = matrix[x, y]
    if cur[0] == 0:
        return
    if cur[1] > 0:
        return
    global coordinate_list
    if (x, y) in coordinate_list:
        return
    coordinate_list.append((x, y))
    m, n, _ = matrix.shape
    right = [0, 0] if y == n - 1 else matrix[x, y + 1]
    left = [0, 0] if y == 0 else matrix[x, y - 1]
    down = [0, 0] if x == m - 1 else matrix[x + 1, y]
    up = [0, 0] if x == 0 else matrix[x - 1, y]

    if right[0] == 1:
        _4_recursive(matrix, x, y + 1)
        if left[0] == 1:
            _4_recursive(matrix, x, y - 1)
            if up[0] == 1:
                _4_recursive(matrix, x - 1, y, )
                if down[0] == 1:
                    _4_recursive(matrix, x + 1, y)
                else:
                    return
            else:
                if down[0] == 1:
                    _4_recursive(matrix, x + 1, y)
                else:
                    return
        else:
            if up[0] == 1:
                _4_recursive(matrix, x - 1, y)
                if down[0] == 1:
                    _4_recursive(matrix, x + 1, y)
                else:
                    return
            else:
                if down[0] == 1:
                    _4_recursive(matrix, x + 1, y)
                else:
                    return
    else:
        if left[0] == 1:
            _4_recursive(matrix, x, y - 1)
            if up[0] == 1:
                _4_recursive(matrix, x - 1, y)
                if down[0] == 1:
                    _4_recursive(matrix, x + 1, y)
                else:
                    return
            else:
                if down[0] == 1:
                    _4_recursive(matrix, x + 1, y)
                else:
                    return
        else:
            if up[0] == 1:
                _4_recursive(matrix, x - 1, y)
                if down[0] == 1:
                    _4_recursive(matrix, x + 1, y)
                else:
                    return
            else:
                if down[0] == 1:
                    _4_recursive(matrix, x + 1, y)
                else:
                    return
    return


def _4_connectivity(matrix):
    m, n, _ = matrix.shape
    count = 0
    global coordinate_list
    for i in range(m):
        for j in range(n):
            _4_recursive(matrix, i, j)
            if len(coordinate_list) > 0:
                count += 1
                set_value(matrix, count)
                coordinate_list = []
    return matrix[:, :, 1]


def _8_connectivity(matrix):
    ...
    return matrix[:, :, 1]


def main():
    input_path = "./input_question_4"
    origial_matrix = np.array(read_file(input_path, read_header=True))
    matrix = np.expand_dims(origial_matrix, axis=2)
    zero_matrix = np.zeros(matrix.shape, dtype=int)
    matrix = np.concatenate((matrix, zero_matrix), axis=2)
    output_4 = _4_connectivity(matrix)
    print(output_4)
    write_file("output_question_4_implement_4_connectivity", None, output_4)

    # output_8 = _8_connectivity(matrix)
    # print(output_8)
    # write_file("output_question_4_implement_8_connectivity", None, output_8)


if __name__ == '__main__':
    main()
