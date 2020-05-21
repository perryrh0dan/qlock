import time


def timing(method):
    def timed(self, *args):
        ts = time.time()
        result = method(self, *args)
        te = time.time()

        print(method.__name__ + ': ' + str((te - ts) * 1000))
        return result
    return timed

