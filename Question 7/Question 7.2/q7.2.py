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


def coords_to_index(input_coords, l):
    output_index = []
    for coord in input_coords:
        index = 0
        for i in range(len(l)):
            product = 1
            if i == 0:
                index += product * coord[i]
                continue
            for k in range(i):
                product *= l[k]
            index += product * coord[i]
        output_index.append([index])
    return output_index


def index_to_coords(input_index, l):
    output_coords = []
    for index in input_index:
        coord = [0 for _ in range(len(l))]
        for i in range(len(l) - 1, -1, -1):
            product = 1
            if i == 0:
                coord[i] = int(index / product)
                continue
            for k in range(i):
                product *= l[k]
            coord[i] = int(index / product)
            index = index % product
        output_coords.append(coord)
    return output_coords


def main():
    l = [4, 8, 5, 9, 6, 7]
    input_coords_path = "./input_coordinates_7_2.txt"
    input_index_path = "./input_index_7_2.txt"
    output_coords_path = "./output_coordinates_7_2.txt"
    output_index_path = "./output_index_7_2.txt"

    input_coords = read_file(input_coords_path, read_header=False)
    input_index = read_file(input_index_path, read_header=False)

    output_index = coords_to_index(input_coords, l)
    output_coords = index_to_coords(input_index, l)

    write_file(output_index_path, ['index'], output_index)
    head_coords = ['x' + str(i + 1) for i in range(len(l))]
    write_file(output_coords_path, head_coords, output_coords)


if __name__ == '__main__':
    main()
