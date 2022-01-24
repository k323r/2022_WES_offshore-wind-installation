import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from glob import glob
from os import path
import logging

from config import parse_args

def plot_track(vessel_track : pd.DataFrame, wind_farms : pd.DataFrame = pd.DataFrame(), margin = 1, figsize=(9,9), save_fig = None, verbose = False, transparent = True):
	# create new figure, axes instances.
	fig = plt.figure(figsize=figsize)

	if transparent:
		fig.patch.set_alpha(0)

	min_lat = vessel_track.latitude.min() - margin
	max_lat = vessel_track.latitude.max() + margin
	min_lon = vessel_track.longitude.min() - margin
	max_lon = vessel_track.longitude.max() + margin
	if verbose:
		print(f'min_lat: {min_lat} min_lon: {min_lon} max_lat: {max_lat} max_lon: {max_lon}')

	m = Basemap(llcrnrlon=min_lon,
				llcrnrlat=min_lat,
				urcrnrlon=max_lon,
				urcrnrlat=max_lat,
				resolution='h',
				projection='merc',
				lat_0=(max_lat - min_lat)/2,
				lon_0=(max_lon - min_lon)/2,
			   )

	m.drawcoastlines()
	m.fillcontinents()
	# m.drawcountries()
	m.drawstates()
	m.drawmapboundary(fill_color='#46bcec')
	m.fillcontinents(color = 'white',lake_color='#46bcec')
	# draw parallels
	m.drawparallels(np.arange(-90,90,2),labels=[1,1,1,1])
	# draw meridians
	m.drawmeridians(np.arange(-180,180,2),labels=[1,1,1,1])

	lons, lats = m(vessel_track.longitude, vessel_track.latitude)
	m.scatter(lons, lats, marker = 'o', color='tab:red', zorder=5, s=2)

	print(type(wind_farms))

	if not wind_farms.empty:
		lons_wf, lats_wf = m(wind_farms.longitude, wind_farms.latitude)
		m.scatter(lons_wf, lats_wf, marker = 's', color='tab:green', zorder = 5, s = 50)

	fig.tight_layout()

	if save_fig:
		plt.savefig(save_fig, dpi=300)

	if not save_fig:
		plt.show()

def main():

	config = parse_args()


	logging.basicConfig(
		filename=config['logfile'],
		level=logging.DEBUG if config['verbose'] else logging.WARNING,
		format='%(levelname)s: %(asctime)s %(message)s',
		datefmt='%Y%m%dT%H%M%S%z',
	)

	logging.debug('done parsing command line arguments')

	vessel_files = glob(path.join(config['input_dir'], config['input_pattern']))
	logging.debug(f'found {len(vessel_files)}: {vessel_files}')
	vessels = dict()

	for v_file in vessel_files:
		logging.debug(f'processing {v_file}')
		vessel = v_file.split('/')[-1].split('.')[0]
		vessels[vessel] = pd.read_csv(v_file)
		vessels[vessel].set_index('epoch', inplace = True)
		logging.debug(f'{vessels[vessel].info()}')
	
	for vessel, data in vessels.items():
		plot_path = path.join(config['output_dir'], f'{vessel}.png')
		logging.debug(f'exporting plot to {plot_path}')
		plot_track(data, vessel, save_fig=plot_path )
				

if __name__ == "__main__":
	main()
