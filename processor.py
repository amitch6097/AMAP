import multiprocessing as mp


def add_processes(key, values):
    return values

def add_batch(batch_obj):
    pool = mp.Pool(processes=4)
    results = [pool.apply_async(add_processes, args=(key, batch_obj[key])) for key in batch_obj]
    output = [p.get() for p in results]
    print(output)


if __name__ == '__main__':
    dic = {'key':[1, 2, 3], 'key2':[1, 2 ,3]}
    add_batch(dic)
