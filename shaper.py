# imports
from shapely.geometry import Point, LineString, LinearRing, Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.affinity import rotate, scale
import matplotlib.pyplot as plt


# utils
def get_normal(point1: tuple, point2: tuple, length: float) -> list:
	normal: LineString = rotate(LineString([point1, point2]), 90)

	if normal.length <= length:
		return []

	return scale(normal, length / normal.length, length / normal.length).coords


def plot_point(point: tuple) -> None:
	plt.plot([point[0]], [point[1]], 'rx')


def plot(multipolygon: MultiPolygon) -> None:
	for polygon in multipolygon.geoms:
		plt.fill(*polygon.exterior.xy)

		for interior in polygon.interiors:
			plt.fill(*interior.xy, color='white')


def show_plot() -> None:
	plt.show()