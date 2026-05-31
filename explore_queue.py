from sortedcontainers import SortedList


class ExploreQueue:

    def __init__(self):
        self._sl: SortedList = SortedList()
        self._entries: dict[tuple, tuple] = {}
        self._count: int = 0

    def add(self, pos: tuple, prob: int) -> None:
        if pos in self._entries:
            return
        entry = (prob, -self._count, pos)

        self._count += 1

        self._entries[pos] = entry
        self._sl.add(entry)

    def discard(self, pos: tuple) -> None:
        entry = self._entries.pop(pos, None)
        if entry is not None:
            self._sl.remove(entry)

    def peek(self) -> tuple | None:
        return self._sl[0][2] if self._sl else None

    def clear(self) -> None:
        self._sl.clear()
        self._entries.clear()
        self._count = 0
