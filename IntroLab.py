def sleep_in(weekday, vacation):
  return True if not weekday or vacation else False

def monkey_trouble(a_smile, b_smile):
  return True if a_smile and b_smile or not a_smile and not b_smile else False

def sum_double(a, b):
  return a*4 if a == b else a + b

def diff21(n):
  return 21-n if n <= 21 else (n-21)*2

def near_hundred(n):
  return True if abs(100 - n) <= 10 or abs(200 - n) <= 10 else False

def parrot_trouble(talking, hour):
  return True if talking == True and hour < 7 or talking == True and hour > 20 else False

def pos_neg(a, b, negative):
  return True if negative and (a < 0 and b < 0) or not negative and ((a<0 and b>0) or (a>0 and b<0)) else False

def makes10(a, b):
  return True if a == 10 or b == 10 or a+b == 10 else False

def hello_name(name):
  return "Hello " + name + "!"

def make_abba(a, b):
  return a + b + b + a

def make_tags(tag, word):
  return "<" + tag + ">" + word + "</" + tag + ">"

def make_out_word(out, word):
  return out[:(len(out))//2] + word + out[(len(out))//2:]

def extra_end(str):
  return str[len(str) - 2:] + str[len(str) - 2:] + str[len(str) - 2:]

def first_two(str):
  return str if len(str) < 2 else str[:2]

def first_half(str):
  return str[:(len(str))//2]

def without_end(str):
  return str[1:-1]

def first_last6(nums):
  return True if nums[0] == 6 or nums[len(nums)-1] == 6 or nums[0] == "6" or nums[len(nums)-1] == "6" else False

def same_first_last(nums):
  return True if len(nums) >= 1 and nums[0] == nums[len(nums)-1] else False

def make_pi(n):
  return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7][:n]

def common_end(a, b):
  return True if a[0] == b[0] or a[len(a)-1] == b[len(b)-1] else False

def sum3(nums):
  return sum(nums)

def rotate_left3(nums):
  return [nums[x + 1] if x < len(nums) - 1 else nums[0] for x in range(len(nums))]

def reverse3(nums):
  return nums[::-1]

def max_end3(nums):
  return [max(nums[0], nums[-1])] * len(nums)

def cigar_party(cigars, is_weekend):
  return True if is_weekend and cigars >= 40 or 40 <= cigars <= 60 else False

def date_fashion(you, date):
  return 0 if you <= 2 or date <= 2 else 2 if you >= 8 or date >= 8 else 1

def squirrel_play(temp, is_summer):
  return True if is_summer and 60 <= temp <= 100 or 60 <= temp <= 90 else False

def caught_speeding(speed, is_birthday):
  return 1 if (is_birthday and 66 <= speed <= 85) or (not is_birthday and 61 <= speed <= 80) else 2 if (is_birthday and speed >= 86) or (not is_birthday and speed >= 81) else 0

def sorta_sum(a, b):
  return 20 if  10 <= a + b <= 19 else a+b


def alarm_clock(day, vacation):
  return "off" if vacation and (day == 0 or day == 6) else "10:00" if vacation or (day == 0 or day == 6) else "7:00"

def love6(a, b):
  return a == 6 or b == 6 or a + b == 6 or abs(a - b) == 6

def in1to10(n, outside_mode):
  return (outside_mode and (n <= 1 or n >= 10)) or (not outside_mode and 1 <= n <= 10)


