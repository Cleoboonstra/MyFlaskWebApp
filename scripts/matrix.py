# pandas and numpy for data manipulation
import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.embed import components
from app import *

from bokeh.models import Panel


def matrix_tab(filename):
	myDataFrame = pd.read_csv(filename)
	author_list = myDataFrame.iloc[:, 0]

	m = [None] * (author_list.size)
	author = [None] * (author_list.size)
	i = 0
	while i < author_list.size:
		m[i] = author_list[i].split(";")
		i += 1

	i = 0
	while i < (author_list.size):
		n = m[i][1:-1]
		author[i] = m[i][0]
		m[i] = n
		i += 1

	i = 0
	while i < author_list.size:
		j = 0
		while j < author_list.size:
			m[i][j] = float(m[i][j])
			j += 1
		i += 1

	arrayM = np.array(m)
	p = figure(x_range=(0, 2), y_range=(0, 2))
	ds = ColumnDataSource(data=dict(image=[arrayM]))
	p.image(image='image', x=0, y=0, dw=2, dh=2, source=ds, palette="Spectral11")


	dfM = pd.DataFrame(m)

	dfM['sum'] = dfM[list(dfM.columns)].sum(axis=1)

	minimum = 100
	maximum = 150

	dfMFilter = dfM[(dfM['sum'] >= minimum) & (dfM['sum'] <= maximum)]

	dfM = dfM.sort_values(by='sum', ascending=0)
	del dfM['sum']
	del dfMFilter['sum']

	dfM = dfM.reindex(columns=dfM.index)
	mReorder = dfM.as_matrix(columns=None)
	arrayMReorder = np.array(mReorder)

	dfMFilter = dfMFilter.reindex(columns=dfMFilter.index)
	mFilterReorder = dfMFilter.as_matrix(columns=None)
	arrayMFilterReorder = np.array(mFilterReorder)

	pReorder = figure(x_range=(0, 2), y_range=(0, 2))
	pReorder.image(image=[arrayMReorder], x=0, y=0, dw=2, dh=2, palette="Spectral11")

	dfAuthor = pd.DataFrame(author)
	dfAuthor = dfAuthor.reindex(index=dfM.index)
	authorReorder = dfAuthor[0]


	# script, div = components(p)

	return p

	#tab = Panel(child =p, title ='Matrix')

	#return tab