def read_file(path, read_header=False):
    f = open(path, "r+")
    rows = f.readlines()
    if not read_header:
        rows = rows[1:]
    cols = []
    for row in rows:
        col = str.split(row)
        if len(col) == 1:
            cols.append(int(col[0]))
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


def coords_to_index(input_coords, l1, l2):
    output_index = []
    for coord in input_coords:
        x1, x2 = coord
        index = [x1 + x2 * l1]
        output_index.append(index)
    return output_index


def index_to_coords(input_index, l1, l2):
    output_coords = []
    for index in input_index:
        x1 = index % l1
        x2 = int(index / l1)
        coord = [x1, x2]
        output_coords.append(coord)
    return output_coords


def main():
    l1, l2 = 50, 57
    input_coords_path = "./input_coordinates_7_1.txt"
    input_index_path = "./input_index_7_1.txt"
    output_coords_path = "./output_coordinates_7_1.txt"
    output_index_path = "./output_index_7_1.txt"

    input_coords = read_file(input_coords_path, read_header=False)
    input_index = read_file(input_index_path, read_header=False)

    output_index = coords_to_index(input_coords, l1, l2)
    output_coords = index_to_coords(input_index, l1, l2)

    write_file(output_index_path, ['index'], output_index)
    write_file(output_coords_path, ['x1', 'x2'], output_coords)


if __name__ == '__main__':
    main()
