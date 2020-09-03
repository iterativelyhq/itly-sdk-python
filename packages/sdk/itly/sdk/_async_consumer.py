import queue
from datetime import datetime, timedelta
from threading import Thread, Event
from typing import Optional, Callable, List, Tuple, NamedTuple, Any

AsyncConsumerMessage = NamedTuple("AsyncConsumerMessage", [("message_type", str), ("data", Any)])

_dummy_event = Event()


class AsyncConsumer(Thread):
    @staticmethod
    def create_queue():
        # type: () -> queue.Queue
        return queue.Queue(maxsize=10000)

    def __init__(self, message_queue, do_upload, flush_queue_size, flush_interval):
        # type: (queue.Queue, Callable[[List[AsyncConsumerMessage]], None], int, timedelta) -> None
        """Create a consumer thread."""
        Thread.__init__(self)
        # Make consumer a daemon thread so that it doesn't block program exit
        self._daemon = True
        self._do_upload = do_upload
        self._upload_size = flush_queue_size
        self._flush_interval_ms = flush_interval
        self._queue = message_queue
        self._pending_message = None  # type:  Optional[AsyncConsumerMessage]
        self._running = True

    def run(self):
        # type: () -> None
        while self._running:
            self.upload()

    def pause(self):
        # type: () -> None
        self._running = False

    def upload(self):
        # type: () -> None
        batch, event = self.next()
        if len(batch) == 0:
            if event is not None:
                event.set()
            return

        try:
            self._do_upload(batch)
        except Exception:
            pass
        finally:
            if event is not None:
                event.set()
            # mark items as acknowledged from queue
            for _ in batch:
                self._queue.task_done()

    def next(self):
        # type: () -> Tuple[List[AsyncConsumerMessage], Optional[Event]]
        start = datetime.now()
        items = [self._pending_message] if self._pending_message is not None else []  # type: List[AsyncConsumerMessage]
        self._pending_message = None

        now = datetime.now()
        while len(items) < self._upload_size and now - start < self._flush_interval_ms:
            try:
                timeout = (self._flush_interval_ms - (now - start)).total_seconds()
                item = self._queue.get(block=True, timeout=timeout)
                if isinstance(item.data, type(_dummy_event)):
                    return items, item.data
                if len(items) > 0 and items[-1].message_type != item.message_type:
                    self._pending_message = item
                    break
                items.append(item)
                now = datetime.now()
            except queue.Empty:
                break

        return items, None

    def flush(self):
        # type: () -> None
        event = Event()
        self._queue.put(AsyncConsumerMessage(message_type='flush', data=event))
        event.wait()

    def shutdown(self):
        # type: () -> None
        self.pause()
        try:
            self.join()
        except RuntimeError:
            # consumer thread has not started
            pass
