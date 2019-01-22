import threading
import time
import glob


path_list = glob.glob("nogeom_csv/*")
sema = threading.Semaphore(10)

def print_path(path):
    sema.acquire()

    print(path)

    time.sleep(2)
    sema.release()

def test():
    start = time.time()

    thread_list = [threading.Thread(target=print_path, args=(path,)) for path in path_list]

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print(time.time() - start)

def test_nothread():
    start = time.time()
    for path in path_list:
        print_path(path)

    print(time.time() - start)

if __name__ == "__main__":
    # test_nothread()
    test()
    pass
