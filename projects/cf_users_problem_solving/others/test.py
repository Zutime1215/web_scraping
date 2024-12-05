from contests.codechef import codechef
from contests.codeforces import codeforces
from contests.leetcode import leetcode


def contest_msg():
	ojs = [codechef, codeforces, leetcode]
	for oj in ojs:
		x = oj(10)
		print(x)


contest_msg()