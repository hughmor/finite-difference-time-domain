import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

"""
TODO:
	- choose render based on chosen quantity (Ex right now)
"""

quants = {
	'Ex': 0,
	'Ey': 1,
	'Ez': 2,
	'Hx': 3,
	'Hy': 4,
	'Hz': 5,
	'E': 6,
	'H': 7
}


class SimulationRender:
	
	def __init__(self, simulation, quantity='Ex'):
		self.quantity = quantity
		self.sim = simulation
		self.colorscale = self.convert_viridis_to_plotly_colorscale()
		self.duration = 25

	@staticmethod
	def convert_viridis_to_plotly_colorscale():
		viridis = plt.get_cmap('viridis')
		vals = np.linspace(0, 1, viridis.N)
		colors = [[round(256*channel) for channel in color] for color in viridis.colors]
		colorscale = [
			[val, 'rgb({},{},{})'.format(*rgb)] for val, rgb in zip(vals, colors)
		]
		return colorscale

	def get_layout(self):
		title = 'Animation of 2D FDTD'
		return {
			"title": title,
			"autosize": True,
			"height": 600,
			"width": 600,
			"hovermode": 'closest',
			"xaxis": dict(range=[0, self.sim.size[0]], autorange=True),
			"yaxis": dict(range=[0, self.sim.size[1]], autorange=True),
			"showlegend": False,
			"sliders": {
				"args": [
					"transition",
					{
						"duration": self.duration,  # ms?
						"easing": "cubic-in-out"  # may want to change this
					}
				],
				"initialValue": 0,
				"plotlycommand": "animate",
				"values": list(range(len(self.sim.history))),
				"visible": True  # probably want false
			},
			"updatemenus": [
				{
					"buttons": [
						{
							"args": [
								None,
								{
									"frame": {"duration": self.duration, "redraw": True},
									"fromcurrent": True,
									"transition": {
										"duration": self.duration,
										"easing": "quadratic-in-out"
									}
								}
							],
							"label": "Play",
							"method": "animate"
						},
						{
							"args": [
								[None],
								{
									"frame": {"duration": 0, "redraw": True},
									"mode": "immediate",
									"transition": {"duration": 0}
								}
							],
							"label": "Pause",
							"method": "animate"
						}
					],
					"direction": "left",
					"pad": {"r": 10, "t": 87},
					"showactive": False,
					"type": "buttons",
					"x": 0.1,
					"xanchor": "right",
					"y": 0,
					"yanchor": "top"
				}
			]
		}

	def get_frames(self, z, zmax, layout):
		frames = []
		sliders_dict = {
			"active": 0,
			"yanchor": "top",
			"xanchor": "left",
			"currentvalue": {
				"font": {"size": 20},
				"prefix": "Time:",
				"suffix": " fs",
				"visible": True,
				"xanchor": "right"
			},
			"transition": {"duration": self.duration, "easing": "cubic-in-out"},
			"pad": {"b": 10, "t": 50},
			"len": 0.9,
			"x": 0.1,
			"y": 0,
			"steps": []
		}
		for t, hm in enumerate(z):
			frame = {
				"data": [
					go.Heatmap(z=hm,
							   zmin=0,
							   zmax=zmax,
							   colorscale=self.colorscale,
							   colorbar=dict(thickness=20, ticklen=4))
				],
				"name": str(t + 1)
			}
			frames.append(frame)

			slider_step = {
				"args": [
					[str(t + 1)],
					{"frame": {"duration": self.duration, "redraw": False},
					 "mode": "immediate",
					 "transition": {"duration": self.duration}}
				],
				"label": str(t + 1),
				"method": "animate"}
			if not t == 0:
				sliders_dict["steps"].append(slider_step)
		layout["sliders"] = [sliders_dict]
		return frames

	def get_data(self, layout):
		z = []
		zmaxa = []
		for t, snap in enumerate(self.sim.history):
			field = snap.Ex()
			z.append(field)
			zmaxa.append(np.max(field))
		zmax = max(zmaxa)

		frames = self.get_frames(z, zmax, layout)
		frame0 = frames.pop(0)
		data = frame0["data"]

		return data, frames

	def generate_animation(self):

		layout = self.get_layout()

		data, frames = self.get_data(layout)

		fig = go.Figure(dict(data=data, layout=layout, frames=frames))
		fig.show()
