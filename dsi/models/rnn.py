import numpy as np
import tensorflow as tf


class Model():
    def __init__(self, batch_size, input_length, model_type):
        self.saver = tf.train.Saver()

        self.input_data = tf.placeholder(
            tf.float32, [batch_size, input_length])
        self.label_data = tf.placeholder(tf.int32, [batch_size])

    def save(self, session, filepath):
        return self.saver.save(session, filepath)

    def load(self, session, filepath):
        self.saver.restore(session, filepath)
        return filepath
