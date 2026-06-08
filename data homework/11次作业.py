import heapq

class MedianFinder:
    def __init__(self):
        # 大顶堆（用负数模拟）
        self.maxHeap = []
        # 小顶堆
        self.minHeap = []

    def addNum(self, num: int) -> None:
        # 先加入大顶堆
        heapq.heappush(self.maxHeap, -num)
        
        # 将大顶堆的最大值移到小顶堆（保持小顶堆的元素都 >= 大顶堆）
        max_val = -heapq.heappop(self.maxHeap)
        heapq.heappush(self.minHeap, max_val)
        
        # 如果小顶堆过大，移回大顶堆以保持大小平衡
        if len(self.minHeap) > len(self.maxHeap):
            min_val = heapq.heappop(self.minHeap)
            heapq.heappush(self.maxHeap, -min_val)

    def findMedian(self) -> float:
        if len(self.maxHeap) > len(self.minHeap):
            return float(-self.maxHeap[0])
        else:
            return (-self.maxHeap[0] + self.minHeap[0]) / 2.0
        
mf = MedianFinder()
mf.addNum(3)      # 中位数: 3
print(mf.findMedian())  # 3.0
mf.addNum(1)      # 中位数: 2
print(mf.findMedian())  # 2.0
mf.addNum(4)      # 中位数: 3
print(mf.findMedian())  # 3.0
mf.addNum(1)      # 中位数: 2
print(mf.findMedian())  # 2.0
mf.addNum(5)      # 中位数: 3
print(mf.findMedian())  # 3.0