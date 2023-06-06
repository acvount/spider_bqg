import time
import threading
from color_log import Log


class InvalidSystemClock(Exception):
    """
    时钟回拨异常
    """
    pass


class IdWorker(object):
    WORKER_ID_BITS = 5
    DATACENTER_ID_BITS = 5
    SEQUENCE_BITS = 12

    MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
    MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

    WOKER_ID_SHIFT = SEQUENCE_BITS
    DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

    SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

    TWEPOCH = 1288834974657

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, datacenter_id=None, worker_id=None, sequence=0):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    if datacenter_id is None:
                        datacenter_id = cls.get_thread_id() % (cls.MAX_DATACENTER_ID + 1)
                    if worker_id is None:
                        worker_id = cls.get_thread_id() % (cls.MAX_WORKER_ID + 1)
                    cls._instance = super(IdWorker, cls).__new__(cls)
                    cls._instance.__init__(datacenter_id, worker_id, sequence)
        return cls._instance

    def __init__(self, datacenter_id, worker_id, sequence=0):
        if worker_id > self.MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        if datacenter_id > self.MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id值越界')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1

    @staticmethod
    def gen_timestamp():
        return int(time.time() * 1000)

    @staticmethod
    def get_thread_id():
        return threading.get_ident()

    def get_id(self):
        timestamp = self.gen_timestamp()

        if timestamp < self.last_timestamp:
            Log().error(f'clock is moving backwards. Rejecting requests until {self.last_timestamp}')
            raise InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - self.TWEPOCH) << self.TIMESTAMP_LEFT_SHIFT) | \
                 (self.datacenter_id << self.DATACENTER_ID_SHIFT) | \
                 (self.worker_id << self.WOKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        timestamp = self.gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self.gen_timestamp()
        return timestamp


if __name__ == '__main__':
    worker = IdWorker(10, 1)
    print(worker.get_id())
