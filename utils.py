# utils
url: str = 'https://geodata-stnmt.tphcm.gov.vn/geoserver/tnmt/wms?service=WMS&request=GetFeatureInfo&version=1.1.1'

code2layer: dict = {
	'783': 'tnmt:ranhthua_cuchi',
	'785': 'tnmt:ranhthua_binhchanh',
	'765': 'tnmt:ranhthua_binhthanh',
	'786': 'tnmt:ranhthua_nhabe',
	'764': 'tnmt:ranhthua_govap',
	'784': 'tnmt:ranhthua_hocmon',
	'787': 'tnmt:ranhthua_cangio',
	'761': 'tnmt:ranhthua_q12',
	'768': 'tnmt:ranhthua_phunhuan',
	'777': 'tnmt:ranhthua_binhtan',
	'767': 'tnmt:ranhthua_tanphu',
	'762': 'tnmt:ranhthua_thuduc',
	'766': 'tnmt:ranhthua_tanbinh',
	'760': 'tnmt:ranhthua_q1',
	'769': 'tnmt:ranhthua_q2',
	'770': 'tnmt:ranhthua_q3',
	'773': 'tnmt:ranhthua_q4',
	'774': 'tnmt:ranhthua_q5',
	'775': 'tnmt:ranhthua_q6',
	'778': 'tnmt:ranhthua_q7',
	'776': 'tnmt:ranhthua_q8',
	'763': 'tnmt:ranhthua_q9',
	'771': 'tnmt:ranhthua_q10',
	'772': 'tnmt:ranhthua_q11',
	'def': 'tnmt:ranhthua_tphcm',
}

layer2src: dict = {
	# 'tnmt:ranhthua_cuchi': (10.91744, 106.54478),
	# 'tnmt:ranhthua_binhchanh': (10.74125, 106.54208),
	# 'tnmt:ranhthua_binhthanh': (10.81558, 106.72091),
	# 'tnmt:ranhthua_nhabe': (10.65635, 106.72882),
	# 'tnmt:ranhthua_govap': (10.83049, 106.64114),
	# 'tnmt:ranhthua_hocmon': (10.88824, 106.59809),
	# 'tnmt:ranhthua_cangio': (10.41042, 106.95332),
	# 'tnmt:ranhthua_q12': (10.83595, 106.62927),
	# 'tnmt:ranhthua_phunhuan': (10.79955, 106.67306),
	# 'tnmt:ranhthua_binhtan': (10.76548, 106.61729),
	# 'tnmt:ranhthua_tanphu': (10.79217, 106.63041),
	# 'tnmt:ranhthua_thuduc': (10.82857, 106.72851),
	# 'tnmt:ranhthua_tanbinh': (10.81986, 106.63198),
	'tnmt:ranhthua_q1': (10.77665, 106.70093),
	# 'tnmt:ranhthua_q2': (10.78412, 106.72712),
	# 'tnmt:ranhthua_q3': (10.77866, 106.68044),
	# 'tnmt:ranhthua_q4': (10.76306, 106.70499),
	# 'tnmt:ranhthua_q5': (10.76447, 106.68171),
	# 'tnmt:ranhthua_q6': (10.74315, 106.63282),
	# 'tnmt:ranhthua_q7': (10.72873, 106.72357),
	# 'tnmt:ranhthua_q8': (10.72412, 106.62205),
	# 'tnmt:ranhthua_q9': (10.82698, 106.81398),
	# 'tnmt:ranhthua_q10': (10.77718, 106.66876),
	# 'tnmt:ranhthua_q11': (10.76893, 106.65774),
	# 'tnmt:ranhthua_tphcm': (0, 0),
}


def get_bbox(u: tuple) -> str:
	return f'{u[1] - 4e-4},{u[0] - 4e-4},{u[1] + 4e-4},{u[0] + 4e-4}'


def get_layer_url(u: tuple) -> str:
	return f'{url}\
		&layers=tnmt%3Aranhphuong_pg&styles=&format=image%2Fpng&transparent=true&info_format=application/json\
		&tiled=true&width=1536&height=792&srs=EPSG:4326&bbox={get_bbox(u)}\
		&query_layers=tnmt%3Aranhphuong_pg&FEATURE_COUNT=1\&X=768&Y=396\
	'


def get_polygon_url(u: tuple, layer: str) -> str:
	return f'{url}\
		&layers={layer}&styles=&format=image%2Fpng&transparent=true&info_format=application/json\
		&tiled=true&width=1536&height=792&srs=EPSG:4326&bbox={get_bbox(u)}\
		&query_layers={layer}&FEATURE_COUNT=1&X=768&Y=396\
	'


def get_intent_url(u: tuple) -> str:
	return f'{url}\
		&layers=tnmt%3Aqhsdd2020&styles=&format=image%2Fpng&transparent=true&info_format=application/json\
		&tiled=true&width=1536&height=792&srs=EPSG:4326&bbox={get_bbox(u)}\
		&query_layers=tnmt%3Aqhsdd2020&FEATURE_COUNT=1&X=768&Y=396\
	'


def get_height_url(u: tuple) -> str:
	return f'{url}\
		&layers=tnmt%3Ahcm_dem&styles=&format=image%2Fpng&transparent=true&info_format=application/json\
		&tiled=true&width=1536&height=792&srs=EPSG:4326&bbox={get_bbox(u)}\
		&query_layers=tnmt%3Ahcm_dem&FEATURE_COUNT=1&X=768&Y=396\
	'


def get_velocity_url(u: tuple) -> str:
	return f'{url}\
		&layers=tnmt%3Avelocity&styles=&format=image%2Fpng&transparent=true&info_format=application/json\
		&tiled=true&width=1536&height=792&srs=EPSG:4326&bbox={get_bbox(u)}\
		&query_layers=tnmt%3Avelocity&FEATURE_COUNT=1&X=768&Y=396\
	'


def get_plan_url(u: tuple) -> str:
	return f'{url}\
		&layers=tnmt%3Akehoachsdd_hcm_2018&styles=&format=image%2Fpng&transparent=true&info_format=application/json\
		&tiled=true&width=1536&height=792&srs=EPSG:4326&bbox={get_bbox(u)}\
		&query_layers=tnmt%3Akehoachsdd_hcm_2018&FEATURE_COUNT=1&X=768&Y=396\
	'


def get_subdivision_url(u: tuple) -> str:
	return f'{url}\
		&layers=tnmt:QHPKSDD_SHAPE&styles=&format=image%2Fpng&transparent=true&info_format=application/json\
		&tiled=true&width=1536&height=792&srs=EPSG:4326&bbox={get_bbox(u)}\
		&query_layers=tnmt:QHPKSDD_SHAPE&FEATURE_COUNT=1&X=768&Y=396\
	'