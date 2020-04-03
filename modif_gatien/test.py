
"""Depeyre Gatien"""
l = ["a", "b", "c", "d"]
l.reverse()
print(l)
for e in l:
	print(e)
	if e == "a":
		l.remove("a")


print(l)