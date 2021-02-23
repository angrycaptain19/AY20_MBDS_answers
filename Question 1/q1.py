def n_steps_for_target(n, target, max):
    """
    the sum of n numbers from [1,max] equal to target
    :return: list of n numbers
    """
    # example: n_steps_for_target(2, 6, 5) return: [[1,5],[2,4],[3,3]]
    result = []
    if n == 1:
        if target < max:
            return [[target]]
        else:
            return []
    elif n == 2:
        for i in range(1, int(target / 2) + 1):
            if target - i <= max:
                l = [i, target - i]
                result.append(l)
        return result
    else:
        for i in range(1, max + 1):
            # recursive
            lists = n_steps_for_target(n - 1, target - i, max)
            for list in lists:
                list.extend([i])
            return lists


def cal_oper(row, col, target, out_path):
    with open(out_path, "a+") as f:
        # sum of 1 column [1, row]
        sum_col = int((1 + row) * row / 2)
        # number of horizontal point except 1 column
        num_col = col - 1
        for t in target:
            # target_rest is equal to target minus the sum of one column, and the sum is mandatory in any time
            target_rest = t - sum_col
            base_point = min(col, target_rest)
            max_numof_base_point = num_col
            sum_lists = []
            # point from 1 to col
            for point in range(1, col + 1):
                while max_numof_base_point * point > target_rest:
                    max_numof_base_point = max_numof_base_point - 1
                for num in range(1, max_numof_base_point):
                    base_point_list = [point for i in range(num)]
                    base_point_list.extend([i for i in range(1, row + 1)])

                    new_target_rest = target_rest - point * num
                    # list for new_target_rest with num of numbers and max number
                    sum_list = n_steps_for_target(num_col - num, new_target_rest, row)
                    for l in sum_list:
                        l.extend(base_point_list)
                        l.sort()
                        if l not in sum_lists:
                            sum_lists.extend([l])
            opers = lists_convert_to_oper(sum_lists, t)
            for oper in opers:
                output = str(t) + " " + oper + "\n"
                f.write(output)
            print(t, target_rest, base_point, num_col, max_numof_base_point, sum_lists, opers)
        f.write("\n")


def cal_oper_one_answer(row, col, target, out_path):
    with open(out_path, "a+") as f:
        # sum of 1 column [1, row]
        sum_col = int((1 + row) * row / 2)
        # number of horizontal point except 1 column
        num_col = col - 1
        for t in target:
            # target_rest is equal to target minus the sum of one columnn, and the sum is mandatory in any time
            target_rest = t - sum_col
            if target_rest % num_col == 0:
                base_point = target_rest / num_col
            else:
                base_point = int(target_rest / num_col) + 1
            max_numof_base_point = num_col - 1
            sum_lists = []
            while max_numof_base_point * base_point > target_rest:
                max_numof_base_point = max_numof_base_point - 1
            base_point_list = [base_point for _ in range(max_numof_base_point)]
            base_point_list.extend([i for i in range(1, row + 1)])

            new_target_rest = target_rest - base_point * max_numof_base_point
            # list for new_target_rest with num of numbers and max number
            sum_list = n_steps_for_target(num_col - max_numof_base_point, new_target_rest, row)
            # if sum_list is not None:
            for l in sum_list:
                l.extend(base_point_list)
                l.sort()
                if l not in sum_lists:
                    sum_lists.extend([l])
            opers = lists_convert_to_oper(sum_lists, t, 1)
            for oper in opers:
                output = str(t) + " " + oper + "\n"
                f.write(output)
            # print(t, target_rest, base_point, num_col, max_numof_base_point, sum_lists, opers)
            print(t, opers)


def lists_convert_to_oper(lists, target, max_numof_result=-1):
    """
    convert path to operations
    """
    result_opers = []
    for l in lists:
        sum = 0
        result_oper = ""
        for i in range(len(l) - 1):
            sum += l[i]
            result_oper += 'R' if l[i] == l[i + 1] else 'D'
        sum += l[i + 1]
        # assertion
        assert sum == target
        result_opers.append(result_oper)
        if len(result_opers) == max_numof_result:
            return result_opers
    if not result_opers:
        result_opers = ["None"]
    return result_opers


def main():
    out_put_path = "./output_question_1.txt"

    cal_oper(9, 9, [65, 72, 90, 110], out_put_path)
    # output only one result for a input number
    cal_oper_one_answer(90_000, 100_000, [87_127_231_192, 5_994_891_682], out_put_path)


if __name__ == '__main__':
    main()
