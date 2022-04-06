import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from datetime import datetime
import yaml


if __name__ == "__main__":
    with open("config.yaml") as file:
        cfg = yaml.load(file, Loader=yaml.SafeLoader)

    current_time = str(time.time())

    tensorboard = TensorBoard(log_dir=datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"))
    earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min')
    mcp_save = ModelCheckpoint('../../../bin/models/nn_{}'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")),
                               save_best_only=True,
                               monitor='val_loss',
                               mode='min')

    data = pd.read_csv(cfg['train_data_path'])
    train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)

    x_train = tf.keras.utils.normalize(train_set.drop(['Home-Team-Win'], axis=1).values.astype(float), axis=1)
    y_train = np.asarray(train_set['Home-Team-Win'])

    x_test = tf.keras.utils.normalize(test_set.drop(['Home-Team-Win'], axis=1).values.astype(float), axis=1)
    y_test = np.asarray(test_set['Home-Team-Win'])

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(512, activation=tf.nn.relu6))
    model.add(tf.keras.layers.Dense(256, activation=tf.nn.relu6))
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu6))
    model.add(tf.keras.layers.Dense(2, activation=tf.nn.softmax))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, epochs=50, validation_split=0.1, batch_size=32,
              callbacks=[tensorboard, earlyStopping, mcp_save])
    score = model.evaluate(x_test, y_test, batch_size=32)
    print(score)
