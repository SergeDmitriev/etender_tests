
def page_switch_times(count_records):
    i = 0

    if count_records > 10:
        if count_records % 10 > 0:
            i = count_records // 10 + 1
        else:
            i = count_records // 10
            print(i)
    elif 0 < count_records <= 10:
        i = 1

    for j in range(i):
        # print('get_method worked {0} times', j+1)
        j += 1
    return j


def f(p):
    for x in range(1, p+1):
        yield x


if __name__ == "__main__":
    # print(page_switch_times(115))
    for i in f(page_switch_times(115)):
        print(i)
