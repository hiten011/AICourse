import heapq


class ExploreQueue:
    
    def __init__(self):
        self._heap: list[tuple] = []
        self._valid: dict[tuple, tuple] = {} 
        self._count: int = 0

    def add(self, pos: tuple, prob: int) -> None:
        if pos in self._valid:
            return
        neg_count = -self._count
        self._count += 1
        self._valid[pos] = (prob, neg_count)
        heapq.heappush(self._heap, (prob, neg_count, pos))

    def discard(self, pos: tuple) -> None:
        self._valid.pop(pos, None) 

    def peek(self) -> tuple | None:
        while self._heap:
            prob, neg_count, pos = self._heap[0]
            if self._valid.get(pos) == (prob, neg_count):
                return pos          
            heapq.heappop(self._heap)
        return None

    def clear(self) -> None:
        self._heap.clear()
        self._valid.clear()
        self._count = 0
