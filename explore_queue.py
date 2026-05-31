import heapq


class ExploreQueue:

    def __init__(self):
        self._heap: list = []
        self._active: set = set()
        self._count: int = 0

    def add(self, pos: tuple, prob: int) -> None:
        if pos in self._active:
            return
        self._active.add(pos)
        heapq.heappush(self._heap, (prob, -self._count, pos))
        self._count += 1

    def discard(self, pos: tuple) -> None:
        self._active.discard(pos)

    def peek(self) -> tuple | None:
        while self._heap and self._heap[0][2] not in self._active:
            heapq.heappop(self._heap)
        return self._heap[0][2] if self._heap else None

    def clear(self) -> None:
        self._heap.clear()
        self._active.clear()
        self._count = 0
