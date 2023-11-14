from app.src.models import autofarmbase as atdb
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from app.src.ml import Autoencoder
import plotly.express as px
df = atdb.get_samples('ADAUSDT',20000)
df = df.set_index('OpenTime')
print(df.describe())
print(df.dtypes)


scaler = ((df - df.mean()) / df.std())
part1_mean = df.mean()
part1_std = df.std()
data = (scaler - scaler.min()) / (scaler.max() - scaler.min())

part2_min = scaler.min()
part3_max = scaler.max()

print(data)

data = data.to_numpy()
dados = data.reshape(data.shape[0],1,data.shape[1])


model  = Autoencoder(input_shape=(dados.shape[1],dados.shape[2]),encode_size= 1)


model.compile(optimizer='adam', loss='mean_squared_error',metrics=['accuracy'])


model.fit(dados,dados,batch_size=128,shuffle=True,epochs=200,validation_split=0.1)

pred = model.predict(dados)
print(pred)
pred = np.reshape(pred,(pred.shape[0],pred.shape[2]))
pred = (pred * (part3_max.to_numpy() - part2_min.to_numpy()))  +  part2_min.to_numpy()

pred = (pred * part1_std.to_numpy()) + part1_mean.to_numpy()
 
print(pred)
df[['predc','predo','predh','predl','predv']] = pred

# data = ((pred + 1) * df.std()) + df.mean()

# fig  = make_subplots(
#     rows=1, cols=6,
#     )

print(df.describe())

fig = px.line(df)
fig.show()
# fig = make_subplots(rows=2, cols=2)

# fig.add_trace(go.Scatter(x=df['OpenTime'], y=df['Close']),
#               row=1, col=1,)

# fig.add_trace(go.Scatter(x=df['OpenTime'], y=df['Close'].rolling(120).mean()),
#               row=1, col=2)

# # fig.add_trace(go.Scatter(x=df['OpenTime'], y=df['High']),
# #               row=1, col=2)

# # fig.add_trace(go.Scatter(x=df['OpenTime'], y=df['Low']),
# #               row=2, col=1)

# fig.show()




# from pymongo import MongoClient


# df = pd.read_csv('./data/ada_process.csv')

# df['OpenTime'] = pd.to_datetime(df['OpenTime'],format='%Y-%m-%d %H:%M')



# df.loc[df['Volume'] < 1, 'Volume'] = df['Volume'].median()
# atdb.insert_samples(df,'ADAUSDT')


# mongo_url = "mongodb://root:example@localhost:27017/"
# db_client = MongoClient(mongo_url)

# auto_farm_base_client =  db_client['AutoFarmBase']
# auto_farm_client = db_client['AutoFarm']



# collection = auto_farm_base_client.create_collection('ADAUSDT', timeseries={ 'timeField': 'OpenTime' })
# collection.insert_many(df.to_dict('records'))

# df.to_csv('ameba.csv')
# df = pd.DataFrame(auto_farm_base_client['ADAUSDT'].find({},{"_id": 0}))