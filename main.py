#!/usr/bin/env python3
# coding: utf-8


"""Рекурсивная отрисовка фрактала из окружностей в svg"""


import random
from math import cos, sin, pi
import svgwrite as svg  # https://pypi.org/project/svgwrite/


class setup():
	"""Настройки программы"""

	def __init__(self, coords=(500,500), radius=250, size=(1000,1000), step=15, rcoef=0.5, depth=100, style={"fill":"none", "scolor":"blue", "swidth":"1"}):
		"""Инициализация настроек:
			coords - координаты центра начальной окружности;
			radius - радиус начальной окружности;
			size - размеры холста;
			step - шаг по углу;
			rcoef - коэффициент умножения окружности;
			depth - глубина рекурсии;
			style - параметры отрисовки окружности {заполнение, цвет линии, толщина линии}."""
		assert (type(coords) == tuple) and (len(coords) == 2), "Неверный формат координат центра окружности"
		assert (type(size) == tuple) and (len(size) == 2), "Неверный формат размеров холста"
		assert (radius <= size[0]) and (radius <= size[1]), "Радиус исходной окружности превышает размеры холста"
		assert (step <= 180) and (step >= 1) and (type(step) == int), "Неверно задан шаг движения по окружности. Введите целое значение от 1 до 180 градусов."
		assert (not (rcoef > 10 and radius > 1)), "Слишком большой коэффициент умножения для заданного радиуса"
		self.xcoord, self.ycoord = coords
		self.radius = radius
		self.height, self.width = size
		self.step = step
		self.rcoef = rcoef
		self.depth = depth
		self.fill = style["fill"]
		self.scolor = style["scolor"]
		self.swidth = style["swidth"]
		self.coords = coords
		self.size = size
		self.style = style


def move(x, y, r, a):
	"""Вычисляет координаты движения исходной точки x,y по окружности радиуса r
	на угол a. Возвращает координаты центра новой окружности."""
	x = x + cos(a) * r
	y = y + sin(a) * r
	return (x, y)


def circle(x, y, r, style):
	"""Возвращает svg-окружность с заданными геометрическими и графическими параметрами"""
	fill, scolor, swidth = style["fill"], style["scolor"], style["swidth"]
	return svg.shapes.Circle((x, y), r=r, fill=fill, stroke=scolor, stroke_width=swidth)


def circles(fractal, size, style):
	"""Возвращает svg-окружности с заданными геометрическими и графическими параметрами из фрактального списка"""
	canvas = svg.Drawing(size=size)
	for f in fractal:
		canvas.add(circle(*f, style))
	return canvas


def colored_circles(fractal, size, style, colors):
	"""Случайным образом разукрашивает возвращаемые svg-окружности"""
	canvas = svg.Drawing(size=size)
	for f in fractal:
		style["scolor"] = random.choice(colors)
		canvas.add(circle(*f, style))
	return canvas


def angles(step):
	"""Вычисляет список углов в радианах по заданному в градусах шагу"""
	degrees = range(0, 360, step)
	radians = [pi * i / 180 for i in degrees]
	return radians


def recursion(coords, radius, angle, rcoef, fractal=None, depth=1):
	"""Рекурсивное вычисление координат и радиусов окружностей, составляющих фрактал."""

	x, y = coords
	r = radius

	if (fractal == None):
		fractal = [(x, y, r)]

	while (depth > 0):
		depth -= 1
		rc = r * rcoef
		if (rc <= 1) or (rc > 10000):
			break
		for a in angle:
			xc, yc = move(x, y, r, a)
			fractal.append((xc, yc, rc))
			fractal = recursion((xc, yc), rc, angle, rcoef, fractal, depth)
	return fractal


if __name__ == "__main__":
	"""Формирование и вывод фрактала в svg-файл"""

	style = {"fill":"none", "scolor":"blue", "swidth":"1"}  # Стиль оформления окружности
	colors = ["red", "blue", "green", "yellow"]  # Список цветов для функции colored_circles
	myconf = setup(coords=(400,400), radius=200, size=(800,800), step=15, rcoef=0.5, depth=2, style=style)  # Настройка параметров
	fract = recursion(myconf.coords, myconf.radius, angles(myconf.step), myconf.rcoef, depth=myconf.depth)  # Формирование фрактала
	dwg = circles(fract, myconf.size, myconf.style)  # Возвращает холст с svg-объектами окружностей
	# dwg = colored_circles(fract, myconf.size, myconf.style, colors)  # Возвращает холст с svg-объектами окружностей разукрашенных случайным образом

	# Запись данных в файл
	with open("temp/recCircle_out.svg", 'w', encoding="utf-8") as file:
		dwg.write(file)
