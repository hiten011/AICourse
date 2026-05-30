import heapq


class ExploreQueue:

    def __init__(self):
        self._heap: list[tuple] = []          
        self._valid: dict[tuple, int] = {}    

    def add(self, pos: tuple, prob: int) -> None:
        if pos in self._valid:
            return
        self._valid[pos] = prob
        heapq.heappush(self._heap, (prob, pos))

    def discard(self, pos: tuple) -> None:
        self._valid.pop(pos, None)  # O(1) — heap entry becomes stale, cleaned lazily

    def peek(self) -> tuple | None:
        while self._heap:
            prob, pos = self._heap[0]
            if self._valid.get(pos) == prob:
                return pos          # still valid
            heapq.heappop(self._heap)   # stale — drop it
        return None

    def clear(self) -> None:
        self._heap.clear()
        self._valid.clear()
