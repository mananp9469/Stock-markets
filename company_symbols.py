import datapackage
import pandas as pd

data_url = 'https://datahub.io/core/nasdaq-listings/datapackage.json'

# to load Data Package into storage
package = datapackage.Package(data_url)

# to load only tabular data
resources = package.resources
c=0
for resource in resources:
    if resource.tabular:
      if c==1:
        data = pd.read_csv(resource.descriptor['path'])
        symbols = data['Symbol'].values.tolist()
      c+=1