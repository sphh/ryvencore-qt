class Base:

    class IDCtr:
        def __init__(self):
            self.ctr = -1

        def count(self):
            """increases the counter and returns the new count. first time is 0"""
            self.ctr += 1
            return self.ctr

        def set_count(self, cnt):
            if cnt < self.ctr:
                raise Exception("Decreasing ID counters is illegal")
            else:
                self.ctr = cnt

    # all abstract components have a global ID
    global_id_ctr = IDCtr()

    # optional custom ID counter
    id_ctr = None

    def __init__(self):
        self.GLOBAL_ID = self.global_id_ctr.count()

        # ignore custom ID if it has already been set
        if self.id_ctr is not None and not (hasattr(self, 'ID') and self.ID is not None):
            self.ID = self.id_ctr.count()