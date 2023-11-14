from tensorflow.keras.layers import Input, Dense,Flatten,LSTM,RepeatVector,TimeDistributed,Dropout
from tensorflow.keras.models import Model
from tensorflow.keras import Sequential
    
class Autoencoder(Model):
    def __init__(self, input_shape, encode_size):
        super(Autoencoder, self).__init__()
        self.encoder = Sequential([
            LSTM(input_shape[1], input_shape=input_shape,activation='tanh',return_sequences=True),
            Dropout(0.3),
            LSTM(encode_size,activation='tanh',return_sequences=False),
            RepeatVector(input_shape[0]),
            Dense(encode_size,activation='tanh')
        ])
        self.decoder = Sequential([
            LSTM(encode_size,activation='tanh',return_sequences=True),
            Dropout(0.3),
            LSTM(input_shape[1],activation='tanh',return_sequences=True),
            TimeDistributed(Dense(input_shape[1],activation='tanh'))
        ])

    def call(self, X):
        encoded = self.encoder(X)
        decoded = self.decoder(encoded)
        return decoded