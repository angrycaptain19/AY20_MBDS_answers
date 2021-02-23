import matplotlib.pyplot as plt
import numpy as np


def read_file(path, read_header=False):
    f = open(path, "r+")
    rows = f.readlines()
    if not read_header:
        rows = rows[1:]
    cols = []
    for row in rows:
        col = str.split(row)
        if len(col) == 0:
            continue
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


def show(input_polygon_path, input_points_path):
    coords = np.array(read_file(input_polygon_path, read_header=True))
    coords = coords.transpose()
    x = coords[0]
    x = np.append(x, x[0])
    y = coords[1]
    y = np.append(y, y[0])
    plt.plot(x, y, color='r')
    plt.scatter(x, y, color='b')

    coords = np.array(read_file(input_points_path, read_header=True))
    coords = coords.transpose()
    x = coords[0]
    y = coords[1]
    plt.scatter(x, y, color='g')
    plt.show()


# detect a point  (old version using numpy)
# def is_point_in_polygon(polygon_coordinate, point):
#     numof_lines_in_polygon = polygon_coordinate.shape[0]
#     x, y = point
#     flag_left = 0
#     flag_right = 0
#     for i in range(numof_lines_in_polygon):
#         point1_in_polygon = polygon_coordinate[i]
#         if i == numof_lines_in_polygon - 1:
#             point2_in_polygon = polygon_coordinate[0]
#         else:
#             point2_in_polygon = polygon_coordinate[i + 1]
#         # point is one of the vertex
#         if point is point1_in_polygon or point is point2_in_polygon:
#             return True
#         # point located between two endpoints of polygon's edge
#         elif point1_in_polygon[1] > y > point2_in_polygon[1] or point2_in_polygon[1] > y > point1_in_polygon[1]:
#             # intersection_point is edge intersect with a horizontal line which through input point
#             if point1_in_polygon[0] == point2_in_polygon[0]:
#                 intersection_point_x = point1_in_polygon[0]
#             else:
#                 # y = kx + b...
#                 intersection_point_x = point2_in_polygon[0] + (y - point2_in_polygon[1]) / (
#                         (point2_in_polygon[1] - point1_in_polygon[1]) / (
#                         point2_in_polygon[0] - point1_in_polygon[0]))
#             if intersection_point_x == x:
#                 # point is a intersection_point
#                 return True
#             if intersection_point_x < x:
#                 flag_left += 1
#             else:
#                 flag_right += 1
#         # point and endpoint are horizontal
#         else:
#             if point2_in_polygon[1] == y:
#                 pass
#             elif point1_in_polygon[1] == y:
#                 # get first endpoint of last edge
#                 last_point1_in_polygon = polygon_coordinate[i - 1]
#                 if (point2_in_polygon[1] < y < last_point1_in_polygon[1]) or (
#                         last_point1_in_polygon[1] < y < point2_in_polygon[1]):
#                     if point1_in_polygon[0] < x:
#                         flag_left += 1
#                     else:
#                         flag_right += 1
#                 else:
#                     pass
#
#     if flag_right % 2 == 0:
#         return False
#     else:
#         return True


# detect a point do not use numpy
def is_point_in_polygon_no_numpy(polygon_coordinate_x, polygon_coordinate_y, point):
    numof_lines_in_polygon = len(polygon_coordinate_x)
    x, y = point
    flag_left = 0
    flag_right = 0
    for i in range(numof_lines_in_polygon):
        point1_in_polygon = [polygon_coordinate_x[i], polygon_coordinate_y[i]]
        if i == numof_lines_in_polygon - 1:
            point2_in_polygon = [polygon_coordinate_x[0], polygon_coordinate_y[0]]
        else:
            point2_in_polygon = [polygon_coordinate_x[i + 1], polygon_coordinate_y[i + 1]]
            # point is one of the vertex
        if point is point1_in_polygon or point is point2_in_polygon:
            return True
        # point located between two endpoints of polygon's edge
        elif point1_in_polygon[1] > y > point2_in_polygon[1] or point2_in_polygon[1] > y > point1_in_polygon[1]:
            # intersection_point is edge intersect with a horizontal line which through input point
            if point1_in_polygon[0] == point2_in_polygon[0]:
                intersection_point_x = point1_in_polygon[0]
            else:
                # y = kx + b...
                intersection_point_x = point2_in_polygon[0] + (y - point2_in_polygon[1]) / (
                        (point2_in_polygon[1] - point1_in_polygon[1]) / (
                        point2_in_polygon[0] - point1_in_polygon[0]))
            if intersection_point_x == x:
                # point is a intersection_point
                return True
            if intersection_point_x < x:
                flag_left += 1
            else:
                flag_right += 1
        # point and endpoint are horizontal
        else:
            if point2_in_polygon[1] == y:
                pass
            elif point1_in_polygon[1] == y:
                # get first endpoint of last edge
                last_point1_in_polygon = [polygon_coordinate_x[i - 1], polygon_coordinate_y[i - 1]]
                if (point2_in_polygon[1] < y < last_point1_in_polygon[1]) or (
                        last_point1_in_polygon[1] < y < point2_in_polygon[1]):
                    if point1_in_polygon[0] < x:
                        flag_left += 1
                    else:
                        flag_right += 1
                else:
                    pass

    if flag_right % 2 == 0:
        return False
    else:
        return True


# detect points (old version using numpy)
# def is_points_in_polygon(polygon_coordinate, points_coordinate):
#     numof_points = points_coordinate.shape[0]
#     result = ["" for _ in range(numof_points)]
#     x_max, y_max = np.max(polygon_coordinate, axis=0)
#     x_min, y_min = np.min(polygon_coordinate, axis=0)
#
#     for i in range(numof_points):
#         x, y = points_coordinate[i]
#         # detect border
#         if x < x_min or x > x_max or y < y_min or y > y_max:
#             result[i] = 'outside'
#         else:
#             if is_point_in_polygon(polygon_coordinate, points_coordinate[i]):
#                 result[i] = 'inside'
#             else:
#                 result[i] = 'outside'
#     return result


# detect points do not use numpy
def is_points_in_polygon_no_numpy(polygon_coordinate_list, points_coordinate_list):
    numof_points = len(points_coordinate_list)
    result = ["" for _ in range(numof_points)]
    polygon_coordinate_x = []
    polygon_coordinate_y = []
    points_coordinate_x = []
    points_coordinate_y = []
    for coord in polygon_coordinate_list:
        polygon_coordinate_x.append(coord[0])
        polygon_coordinate_y.append(coord[1])
    for coord in points_coordinate_list:
        points_coordinate_x.append(coord[0])
        points_coordinate_y.append(coord[1])
    x_max, y_max = max(polygon_coordinate_x), max(polygon_coordinate_y)
    x_min, y_min = min(polygon_coordinate_x), min(polygon_coordinate_y)

    for i in range(numof_points):
        x, y = points_coordinate_x[i], points_coordinate_y[i],
        # detect border
        if x < x_min or x > x_max or y < y_min or y > y_max:
            result[i] = 'outside'
        else:
            if is_point_in_polygon_no_numpy(polygon_coordinate_x, polygon_coordinate_y,
                                            [points_coordinate_x[i], points_coordinate_y[i]]):
                result[i] = 'inside'
            else:
                result[i] = 'outside'
    return result


def main():
    polygon_path = "./input_question_6_polygon"
    points_path = "./input_question_6_points"
    output_path = "./output_question_6"
    # show(polygon_path, points_path)
    polygon_coordinate_list = read_file(polygon_path, read_header=True)
    # polygon_coordinate = np.array(polygon_coordinate_list)
    points_coordinate_list = read_file(points_path, read_header=True)
    # points_coordinate = np.array(points_coordinate_list)

    result = is_points_in_polygon_no_numpy(polygon_coordinate_list, points_coordinate_list)
    # result = is_points_in_polygon(polygon_coordinate, points_coordinate)

    print(polygon_coordinate_list)
    print(points_coordinate_list)
    print(result)

    with open(output_path, "w+") as f:
        for i in range(len(result)):
            data = ""
            for j in points_coordinate_list[i]:
                data += str(j) + "\t"
            data += result[i] + "\n"
            f.write(data)
    f.close()


if __name__ == '__main__':
    main()
