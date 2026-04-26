import tensorflow as tf

# Define a simple model
x = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='x')
y_true = tf.constant([1.0, 3.0, 5.0, 7.0, 9.0, 11.0], shape=[2, 3], name='y_true')

# Define a simple linear model
def linear_model(x):
    return tf.matmul(x, [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])

# Define the loss function
def loss(y_pred, y_true):
    return tf.reduce_mean(tf.square(y_pred - y_true))

# Define the optimizer
optimizer = tf.optimizers.SGD(learning_rate=0.01)

# Define the training operation
with tf.GradientTape() as tape:
    y_pred = linear_model(x)
    loss_value = loss(y_pred, y_true)

# Compute gradients
grads = tape.gradient(loss_value, x)

# Update the weights
optimizer.apply_gradients(zip(grads, [x]))

# Evaluate the model
y_pred = linear_model(x)
loss_value = loss(y_pred, y_true)

print("Loss:", loss_value.numpy())