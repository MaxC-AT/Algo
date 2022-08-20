import random

MAXIMUM_INTEGER = 10 ** 3
LIST_SIZE = 10 ** 5
SOTRING_SPACE_SIZE = MAXIMUM_INTEGER + 1

class Node:
  def __init__(self, val=0, next=None):
    self.val = val
    self.next = next if next else None


class LinkedList:
  def __init__(self):
    self._dummy = Node()
    self._last = self._dummy # for O(1) insertion
    self.size = 0

  def head(self):
    return self._dummy.next

  def tail(self):
    return self._last

  def add(self, node):
    self._last.next = node
    self._last = self._last.next
    self.size += 1

  def print(self):
    vals = []
    curr = self.head()
    while curr:
      vals.append(str(curr.val))
      curr = curr.next
    print(" --> ".join(vals))


class RandomList(LinkedList):
  def __init__(self, size):
    super(RandomList, self).__init__()
    self._createList(size)

  def _createList(self, size):
    for _ in range(size):
      new_node = Node(val=self._randomInteger())
      self.add(new_node)

  def _randomInteger(self):
    return random.randint(0, MAXIMUM_INTEGER)


class SIS:
  @classmethod
  def sorted(cls, linked_list):
    sorting_space = cls._initilization()
    cls._selfIndexedArrangement(linked_list, sorting_space)
    return cls._orderPreservedCompression(sorting_space)

  @classmethod
  def _initilization(cls):
    return [LinkedList() for _ in range(SOTRING_SPACE_SIZE)]

  @classmethod
  def _selfIndexedArrangement(cls, linked_list, sorting_space):
    node = linked_list.head()
    while node:
      new_node = node if sorting_space[node.val].size == 0 else Node(val=node.val, next=None)
      sorting_space[node.val].add(new_node)

      # Avoid pointing to node in the list.
      # We have to assign node = node.next first
      # to keep ref. of rest of the linked list
      node = node.next
      new_node.next = None

  @classmethod
  def _orderPreservedCompression(cls, sorting_space):
    sorted_list = LinkedList()
    for linked_list in sorting_space:
      node = linked_list.head()
      cnt = linked_list.size
      while cnt:
        sorted_list.add(node)
        node = node.next
        cnt -= 1
    return sorted_list


class SIS_INT:
  @classmethod
  def sorted(cls, linked_list):
    sorting_space = cls._initilization()
    cls._selfIndexedArrangement(linked_list, sorting_space)
    cls._orderPreservedCompression(linked_list, sorting_space)
    return linked_list

  @classmethod
  def _initilization(cls):
    return [0 for _ in range(SOTRING_SPACE_SIZE)]

  @classmethod
  def _selfIndexedArrangement(cls, linked_list, sorting_space):
    node = linked_list.head()
    while node:
      sorting_space[node.val] += 1
      node = node.next

  @classmethod
  def _orderPreservedCompression(cls, linked_list, sorting_space):
    head = linked_list.head()
    for val, cnt in enumerate(sorting_space):
      while cnt:
        head.val = val
        head = head.next
        cnt -= 1


class QuickSort:
  @classmethod
  def sorted(cls, linked_list):
    cls._quickSort(linked_list.head(), linked_list.tail())
    return linked_list

  @classmethod
  def _partition(cls, start, end):
    if cls._stopCondition(start, end): return start

    prev, partition, curr = start, start, start
    pivot_val = end.val
    while curr is not end:
      if curr.val < pivot_val:
        cls._swapVal(curr, partition)
        prev = partition
        partition = partition.next
      curr = curr.next

    cls._swapVal(partition, end)
    return prev

  @classmethod
  def _quickSort(cls, start, end):
    if cls._stopCondition(start, end): return

    partition_prev = cls._partition(start, end)
    cls._quickSort(start, partition_prev)
    cls._quickSort(partition_prev.next, end)

  @classmethod
  def _stopCondition(cls, start, end):
    return start is None or start is end or start is end.next
  
  @classmethod
  def _swapVal(cls, node1, node2):
    node1.val, node2.val = node2.val, node1.val


def copyList(linked_list):
  new_list = LinkedList()
  head = linked_list.head()
  while head:
    new_list.add(Node(head.val))
    head = head.next
  return new_list


def validateSortedList(linked_list):
  if linked_list.head() is None: return
  curr = linked_list.head()
  while curr.next:
    if curr.val > curr.next.val:
      raise ValueError("List is not in asceding order!")
    curr = curr.next

if __name__ == '__main__':
  import time

  random_list_1 = RandomList(LIST_SIZE)
  random_list_2 = copyList(random_list_1)
  random_list_3 = copyList(random_list_1)
  # print("========== list before sort ==========")
  # random_list_1.print()
  # random_list_2.print()

  print("start SIS sorting......")
  start_time = time.perf_counter_ns()
  sorted_list_1 = SIS.sorted(random_list_1)
  time_taken_1 = time.perf_counter_ns() - start_time
  print("complete SIS sorting......\n")

  print("start SIS_INT sorting......")
  start_time = time.perf_counter_ns()
  sorted_list_2 = SIS_INT.sorted(random_list_2)
  time_taken_2 = time.perf_counter_ns() - start_time
  print("complete SIS_INT sorting......\n")

  print("start Quick sorting......")
  start_time = time.perf_counter_ns()
  sorted_list_3 = QuickSort.sorted(random_list_3)
  time_taken_3 = time.perf_counter_ns() - start_time
  print("complete Quick sorting......\n")

  print("Time spend for SIS sorting: {} ns".format(time_taken_1))
  print("Time spend for SIS_INT sorting: {} ns".format(time_taken_2))
  print("Time spend for Quick sorting: {} ns".format(time_taken_3))
  print("SIS sorting is {:.2f} faster than Quick sotring!".format(time_taken_3/time_taken_1))
  print("SIS_INT sorting is {:.2f} faster than Quick sotring!".format(time_taken_3/time_taken_2))
  # print("========== list after sort ==========")
  # sorted_list_1.print()
  # sorted_list_2.print()

  validateSortedList(sorted_list_1)
  validateSortedList(sorted_list_2)
  validateSortedList(sorted_list_3)

