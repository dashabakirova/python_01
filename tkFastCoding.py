def CSE(r=0, x1=0, y1=0, x2=0, y2=0):
	R = r * 0.66
	x, y, xx, yy = 0, 0, 0, 0

	if x1 > x2 and abs(y1 - y2) < 80 and abs(x1 - x2) > 80:
		x = -r
		xx = r

	elif x1 < x2 and abs(y1 - y2) < 80 and abs(x1 - x2) > 80:
		x = r
		xx = -r

	if y1 > y2 and abs(y1 - y2) > 80 and abs(x1 - x2) < 80:
		y = -r
		yy = r

	elif y1 < y2 and abs(y1 - y2) > 80 and abs(x1 - x2) < 80:
		y = r
		yy = -r

	if abs(y1 - y2) > 80 and abs(x1 - x2) > 80:
		if x1 < x2 and y1 > y2:
			x, y, xx, yy = R, -R, -R, R
		if x1 < x2 and y1 < y2:
			x, y, xx, yy = R, R, -R, -R
		if x1 > x2 and y1 < y2:
			x, y, xx, yy = -R, R, R, -R
		if x1 > x2 and y1 > y2:
			x, y, xx, yy = -R, -R, R, R

	return x1 + x, y1 + y, x2 + xx, y2 + yy


def packObject(obj, parent, x=0, y=0, parametrs={} ):
	res = obj(parent)
	res.pack(side='top')
	res.place(x=x, y=y)
	for par in parametrs:
		res[par] = parametrs[par]
	res.x = x
	res.y = y
	return res


def hide(*objects):
	for obj in objects:
		obj.place(x=-10000, y=-10000)


def show(*objects):
	for obj in objects:
		obj.place(x=obj.x, y=obj.y)


def sqr(x):
	return  x * x