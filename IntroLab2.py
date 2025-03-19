def string_times(str, n):
 return str * n

def front_times(str, n):
  return str[:3] * n

def string_bits(str):
  return str[0::2]

def string_splosion(str):
  return ''.join([str[:i+1] for i in range(len(str))])

def last2(str):
  return sum(1 for i in range(len(str)-2) if  str[-2:] == str[i:i+2])

def array_count9(nums):
  return nums.count(9)

def array_front9(nums):
  return True if nums[:4].count(9) else False

def array123(nums):
  return True in [nums[x:x+3] == [1, 2, 3] for x in range(len(nums)-2)]

def string_match(a, b):
  return sum(1 for i in range(min(len(a), len(b))-1) if a[i:i+2] == b[i:i+2])

def count_code(str):
    return sum([1 for index in range(len(str) - 3) if str[index:index+2] == "co" and str[index + 3] == "e"])

def end_other(a, b):
  return a.lower().endswith(b.lower()) or b.lower().endswith(a.lower())

def xyz_there(str):
    return 'xyz'in(str[:3],)or any(str[i-1]!='.'and str[i:i+3]=='xyz'for i in range(len(str)-2))

def count_evens(nums):
  return sum([1 for x in nums if x % 2 == 0])

def big_diff(nums):
  return max(nums) - min(nums)

def centered_average(nums):
  return sum(sorted(nums)[1:-1]) // (len(sorted(nums)) - 2)

def sum13(nums):
  return sum(nums[i] for i in range(len(nums)) if nums[i] != 13 and (i == 0 or nums[i - 1] != 13))

def double_char(str):
  return "".join(str[i]*2 for i in range(len(str)))

def count_hi(str):
  return str.count("hi")

def cat_dog(str):
  return True if str.count("cat") == str.count("dog") else False

def sum67(nums):
  return sum([x for index, x in enumerate(nums) if (((nums[(index - nums[index::-1].index(6)):].index(7) + (index - nums[index::-1].index(6))) < index) if (6 in nums[:index+1]) else True)])

def has22(nums):
  return (".2.2.") in ("." + ".".join(map(str,nums)) + ".")

def make_bricks(small, big, goal):
  return (goal%5)<=small and (goal-(big*5))<=small

def lone_sum(a, b, c):
  return sum(v for v in (a, b, c) if (a, b, c).count(v) == 1)

def lucky_sum(a, b, c):
  return sum([a,b,c]) if 13 not in [a,b,c] else sum([a,b,c][:[a,b,c].index(13)])

def no_teen_sum(a, b, c):
  return sum(x for x in [a,b,c] if x not in [13,14,17,18,19])

def round_sum(a, b, c):
  return sum([x + 10 - (x % 10) if x % 10 >= 5 else x - (x % 10) for x in [a, b, c]])

def close_far(a, b, c):
  return (abs(b-a)<2)^(abs(c-a)<2)and abs(b-c)>1

def make_chocolate(small, big, goal):
  return [-1, goal - min(goal // 5, big) * 5][goal % 5 <= small and goal <= big * 5 + small]

  

#Gus Simanson, period 2, 2025