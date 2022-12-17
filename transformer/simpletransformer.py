import tensorflow as tf

query = tf.keras.layers.Input(shape=(None,3,))
value = tf.keras.layers.Input(shape=(4,2,)) 
key = tf.keras.layers.Input(shape=(4,3,))

x = tf.keras.layers.Attention()([query, value, key])
model = tf.keras.models.Model(inputs=[query, value, key], outputs=x)

temp_k = tf.constant([[[10,0,0],
                       [0,10,0],
                       [0,0,10],
                       [0,0,10]]], dtype=tf.float32)  # (4, 3)

temp_v = tf.constant([[[   1,0],
                       [  10,0],
                       [ 100,5],
                       [1000,6]]], dtype=tf.float32)  # (4, 2)

temp_q = tf.constant([[[0, 10, 0]]], dtype=tf.float32)  # (1, 3)

model.predict([temp_q,temp_v,temp_k])