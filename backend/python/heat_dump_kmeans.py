import settings
import dataset
import json
import sklearn.cluster as cluster
import numpy as np
from sqlalchemy.exc import ProgrammingError

db = dataset.connect(settings.CONNECTION_STRING)
result = db.query("SELECT lat,lng FROM geocoords")

data = []
for row in result:
	data.append([float(row['lat']),float(row['lng'])])

kmeans = cluster.KMeans(n_clusters=100).fit(data)
centers =  kmeans.cluster_centers_.tolist()
blank, count = np.unique(kmeans.labels_, return_counts= True)
size = count.tolist()
size = [float(i)/max(size) for i in size]
for row in range(len(centers)):
	try:
		db['heatmap'].insert(dict(
		    lat=centers[row][0],
		    lng=centers[row][1],
		    size=size[row]
		))
	except ProgrammingError as err:
		print(err)