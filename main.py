from shaper import *
from utils import *
from collections import deque
from json import dump
from cProfile import Profile
from pstats import Stats, SortKey
import asyncio, aiohttp


async def scrape_data(url: str, session):
	return await (await session.get(url)).json()


async def scrape_datas(datas: list, field: str, get_field_url, args: tuple, session) -> None:
	field_datas: list = [get_field_url(data['u'], *args) for data in datas]
	field_datas = [asyncio.create_task(scrape_data(url, session)) for url in field_datas]
	field_datas = await asyncio.gather(*field_datas, return_exceptions=True)

	for i in range(len(datas)):
		if field_datas[i] and not isinstance(field_datas[i], aiohttp.ServerDisconnectedError):
			datas[i][field] = field_datas[i]


async def scrape_lands(points: list, layer: str, session) -> list:
	datas: list = [{'u': u} for u in points]

	await scrape_datas(datas, 'layer_data', get_layer_url, (), session)
	datas = [
		data for data in datas
		if 'layer_data' in data and data['layer_data']['features']
		and code2layer.get(data['layer_data']['features'][0]['properties']['maquan'], code2layer['def']) == layer
	]

	await scrape_datas(datas, 'polygon_data', get_polygon_url, (layer,), session)
	datas = [
		data for data in datas
		if 'polygon_data' in data and data['polygon_data']['features']
	]

	# await scrape_datas(datas, 'intent_data', get_intent_url, (), session)
	# await scrape_datas(datas, 'height_data', get_height_url, (), session)
	# await scrape_datas(datas, 'velocity_data', get_velocity_url, (), session)
	# await scrape_datas(datas, 'plan_data', get_plan_url, (), session)
	# await scrape_datas(datas, 'subdivision_data', get_subdivision_url, (), session)

	datas = ({k: v['features'] for k, v in data.items() if k != 'u'} for data in datas)
	datas = (
		{
			**data,
			'layer_data': data['layer_data'][0]['properties'],
			'polygon_data': data['polygon_data'][0]['properties'],
			'id': data['polygon_data'][0]['id'],
			'polygon': data['polygon_data'][0]['geometry']['coordinates'][0],
		}
		for data in datas
	)

	return datas


def spread_lands(dq: deque, ring: LinearRing, polygon: Polygon, eps: float) -> None:
	for i in range(len(ring.coords)):
		for u in get_normal(ring.coords[i], ring.coords[(i + 1) % len(ring.coords)], eps):
			if polygon.contains(Point(*u)):
				continue

			dq.append(u)


async def scrape_map(layer: str, src: tuple) -> None:
	file = open(f'data/{layer.strip("tnmt:")}.json', 'w', encoding='utf-8').close()

	with open(f'data/{layer.strip("tnmt:")}.json', 'a', encoding='utf-8') as file:
		async with aiohttp.ClientSession() as session:
			await scrape_map_inner(layer, src, file, session)


async def scrape_map_inner(layer: str, src: tuple, file, session) -> None:
	batch_size: int = 10
	eps: float = 1e-4
	has_holes: bool = True

	dq: deque = deque([src])
	multipolygon: MultiPolygon = MultiPolygon()
	ids: set = set()

	lands: int = 0
	valid_lands: int = 0

	while eps >= 1e-8 and has_holes:
		while dq:
			if lands == 160:
				print(lands, valid_lands)
				dq.clear()
				return

			polygons: list = [multipolygon]
			points: list = []

			for _ in range(batch_size):
				while dq:
					u = dq.popleft()

					if not multipolygon.contains(Point(*u)):
						points.append(u)
						break

			datas: list = await scrape_lands(points, layer, session)
			lands += batch_size

			for data in datas:
				data_id: str = data['id']

				if data_id is None or data_id in ids:
					continue

				data_polygon: Polygon = Polygon(data['polygon'][0], holes=data['polygon'][1:])
				polygons.append(data_polygon)
				ids.add(data_id)

				dump(data, file, ensure_ascii=0, indent=4, separators=(',', ': '))
				file.write(',\n')

				valid_lands += 1
				print(layer, lands, valid_lands)

				spread_lands(dq, data_polygon.exterior, data_polygon, eps)
				for interior in data_polygon.interiors:
					spread_lands(dq, interior, data_polygon, eps)

			multipolygon = unary_union(polygons)
			multipolygon = MultiPolygon([multipolygon]) if multipolygon.geom_type == 'Polygon' else multipolygon

			if not multipolygon.is_valid:
				multipolygon = multipolygon.buffer(0)

		eps /= 5
		has_holes = False

		for polygon in multipolygon.geoms:
			for interior in polygon.interiors:
				has_holes = True

				spread_lands(dq, interior, multipolygon, eps)
				dq.append((interior.centroid.x, interior.centroid.y))

		plot(multipolygon)
		show_plot()


def main() -> None:
	with Profile() as profile:
		for layer, src in layer2src.items():
			asyncio.run(scrape_map(layer, src))

	stats = Stats(profile)
	stats.sort_stats(SortKey.TIME)
	stats.dump_stats('data/profile.prof')


if __name__ == '__main__':
	main()