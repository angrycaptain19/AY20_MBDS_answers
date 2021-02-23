def sort_dict_list(dict_list):
    return sorted(dict_list, key=lambda x: x["num"], reverse=True)


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
            row += " " + str(col)
        row = row[1:] + "\n"
        f.write(row)
    f.close()


def scan_point(matrix, x, y):
    left = "" if x == 0 else matrix[y][x - 1]
    right = "" if x == len(matrix[0]) - 1 else matrix[y][x + 1]
    up = "" if y == 0 else matrix[y - 1][x]
    down = "" if y == len(matrix) - 1 else matrix[y + 1][x]
    return left, up, right, down


def get_color_from_dict_list(dict_list, matrix, i, j):
    matrix[i][j] = dict_list[0]["color"]
    dict_list[0]["num"] -= 1


def minimal_penaty(matrix_size, color_dict_list):
    matrix_total = matrix_size ** 2
    color_total = 0
    for dict in color_dict_list:
        color_total += dict["num"]
    assert color_total == matrix_total
    dict_list = sort_dict_list(color_dict_list)
    matrix = [["" for _ in range(matrix_size)] for _ in range(matrix_size)]
    for j in range(matrix_size):
        for i in range(matrix_size):
            if i == 0 and j == 0:
                matrix[0][0] = dict_list[0]["color"]
                dict_list[0]["num"] -= 1
                dict_list = sort_dict_list(dict_list)
            else:
                left, up, right, down = scan_point(matrix, i, j)
                # 第一行的时候
                if j == 0:
                    # 拿出所有颜色
                    color_list = [dict["color"] for dict in dict_list if dict["num"] > 0]
                    for k, color in enumerate(color_list):
                        # 不等于左边的颜色时
                        if color != left:
                            assert dict_list[k]["color"] == color
                            matrix[j][i] = color
                            dict_list[k]["num"] -= 1
                            dict_list = sort_dict_list(dict_list)
                            break
                    if matrix[j][i] == "":
                        # 没有符合要求的 把第0个放到marix
                        matrix[j][i] = dict_list[0]["color"]
                        dict_list[0]["num"] -= 1
                        dict_list = sort_dict_list(dict_list)
                else:
                    color_list = [dict["color"] for dict in dict_list if dict["num"] > 0]
                    for k, color in enumerate(color_list):
                        # 第一列的时候 只看up
                        if i == 0:
                            if color != up:
                                assert dict_list[k]["color"] == color
                                matrix[j][i] = color
                                dict_list[k]["num"] -= 1
                                dict_list = sort_dict_list(dict_list)
                                break
                        else:
                            if color != up and color != left:
                                assert dict_list[k]["color"] == color
                                matrix[j][i] = color
                                dict_list[k]["num"] -= 1
                                dict_list = sort_dict_list(dict_list)
                                break
                    if matrix[j][i] == "":
                        # 没有符合要求的 把第0个放到marix
                        matrix[j][i] = dict_list[0]["color"]
                        dict_list[0]["num"] -= 1
                        dict_list = sort_dict_list(dict_list)
    return matrix


def cal_penaty(matrix):
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            color = matrix[i][j]
            left, up, right, down = scan_point(matrix, j, i)
            if color == left:
                count += 1
            if color == right:
                count += 1
            if color == up:
                count += 1
            if color == down:
                count += 1
    return count / 2


def main():
    out_path1 = "./output_question_5_1"
    out_path2 = "./output_question_5_2"
    result1 = minimal_penaty(matrix_size=5, color_dict_list=[{"color": "R", "num": 12},
                                                             {"color": "B", "num": 13}])
    result2 = minimal_penaty(matrix_size=64, color_dict_list=[{"color": "R", "num": 139},
                                                             {"color": "B", "num": 1451},
                                                             {"color": "G", "num": 977},
                                                             {"color": "W", "num": 1072},
                                                             {"color": "Y", "num": 457}])
    penaty_count = cal_penaty(result1)
    print(penaty_count)
    penaty_count = cal_penaty(result2)
    print(penaty_count)
    write_file(out_path1, None, result1)
    write_file(out_path2, None, result2)


if __name__ == '__main__':
    main()
