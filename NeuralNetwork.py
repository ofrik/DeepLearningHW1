import numpy as np
import math


def initialize_parameters(layer_dims):
    """

    :param layer_dims: an array of the dimensions of each layer in the network (layer 0 is the size of the flattened input, layer L is the output sigmoid)
    :return: a dictionary containing the initialized W and b parameters of each layer (W1…WL, b1…bL).

    Hint: Use the randn and zeros functions of numpy to initialize W and b, respectively
    """
    output = {}
    for i, layer_size in enumerate(layer_dims[:-1]):
        output[i] = (np.random.randn(layer_dims[i + 1], layer_dims[i]), np.zeros(layer_dims[i]))
    return output


def linear_forward(A, W, b):
    """
    Implement the linear part of a layer's forward propagation.
    :param A: the activations of the previous layer
    :param W: the weight matrix of the current layer (of shape [size of current layer, size of previous layer])
    :param b: the bias vector of the current layer (of shape [size of current layer, 1])
    :return: Z – the linear component of the activation function (i.e., the value before applying the non-linear function)
            linear_cache – a dictionary containing A, W, b and Z (stored for making the backpropagation easier to compute)
    """
    Z = np.dot(W, A) + b
    linear_cache = {}
    return Z, linear_cache


def sigmoid(Z):
    """

    :param Z: the linear component of the activation function
    :return: A – the activations of the layer
            activation_cache – returns Z, which will be useful for the backpropagation
    """
    A = 1 / (1 + math.exp(-Z))
    return A, Z


def relu(Z):
    """

    :param Z: the linear component of the activation function
    :return: A – the activations of the layer
            activation_cache – returns Z, which will be useful for the backpropagation
    """
    A = np.maximum(Z, 0)
    return A, Z


def linear_activation_forward(A_prev, W, B, activation):
    """
    Implement the forward propagation for the LINEAR->ACTIVATION layer
    :param A_prev: activations of the previous layer
    :param W: the weights matrix of the current layer
    :param B: the bias vector of the current layer
    :param activation: the activation function to be used (a string, either “sigmoid” or “relu”)
    :return: A – the activations of the current layer
            linear_cache – the dictionary generated by the linear_forward function
    """
    if activation == "sigmoid":
        activation_function = sigmoid
    else:
        activation_function = relu
    return activation_function(linear_forward(A_prev, W, B))


def L_model_forward(X, parameters):
    """
    Implement forward propagation for the [LINEAR->RELU]*(L-1)->LINEAR->SIGMOID computation
    :param X: the data, numpy array of shape (input size, number of examples)
    :param parameters: the initialized W and b parameters of each layer
    :return: AL – the last post-activation value
            caches – a list of all the cache objects generated by the linear_forward function
    """
    AL = []
    caches = []
    for item in X:
        A_prev = item
        for key, (W, b) in parameters:
            if key == len(parameters) - 1:
                activation = "sigmoid"
            else:
                activation = "relu"
            A_prev, cache = linear_activation_forward(A_prev, W, b, activation)
            caches.append(cache)
        AL.append(A_prev)
    return np.asarray(AL), caches


def compute_cost(AL, Y):
    """
    Implement the cost function defined by equation
𝑐𝑜𝑠𝑡=−1/𝑚(Σ[(𝑦𝑖∗log(𝐴𝐿))+((1−𝑦𝑖)∗(1−𝐴𝐿))]) (see the slides of the first lecture for additional information if needed).
    :param AL: probability vector corresponding to your label predictions, shape (1, number of examples)
    :param Y: the labels vector (i.e. the ground truth)
    :return: cost – the cross-entropy cost
    """
    m = len(AL)
    cost = (-1 / m) * sum([(Y[i] * np.log(AL)) + ((1 - Y[i]) * (1 - AL)) for i in range(m)])
    return cost


def linear_backward(dZ, cache):
    """
    Implements the linear part of the backward propagation process for a single layer
    :param dZ: the gradient of the cost with respect to the linear output of the current layer (layer l)
    :param cache: tuple of values (A_prev, W, b) coming from the forward propagation in the current layer
    :return: dA_prev -- Gradient of the cost with respect to the activation (of the previous layer l-1), same shape as A_prev
dW -- Gradient of the cost with respect to W (current layer l), same shape as W
db -- Gradient of the cost with respect to b (current layer l), same shape as b
    """
    pass


def linear_activation_backward(dA, cache, activation):
    """
    Implements the backward propagation for the LINEAR->ACTIVATION layer. The function first computes dZ and then applies the linear_backward function.
    :param dA: post activation gradient of the current layer
    :param cache: contains both the linear cache and the activations cache
    :param activation:
    :return: dA_prev – Gradient of the cost with respect to the activation (of the previous layer l-1), same shape as A_prev
dW – Gradient of the cost with respect to W (current layer l), same shape as W
db – Gradient of the cost with respect to b (current layer l), same shape as b
    """
    pass


def relu_backward(dA, activation_cache):
    """
    Implements backward propagation for a ReLU unit
    :param dA: the post-activation gradient
    :param activation_cache: contains Z (stored during the forward propagation)
    :return: dZ – gradient of the cost with respect to Z
    """
    pass


def sigmoid_backward(dA, activation_cache):
    """
    Implements backward propagation for a sigmoid unit
    :param dA: the post-activation gradient
    :param activation_cache: contains Z (stored during the forward propagation)
    :return: dZ – gradient of the cost with respect to Z
    """
    pass


def L_model_backward(AL, Y, caches):
    """
    Implement the backward propagation process for the entire network.
    :param AL: the probabilities vector, the output of the forward propagation (L_model_forward)
    :param Y: the true labels vector (the “ground truth” – true classifications)
    :param caches: list of caches containing for each layer: a) the linear cache; b) the activation cache
    :return: Grads – a dictionary with the gradients
grads["dA" + str(l)] = ...
grads["dW" + str(l)] = ...
grads["db" + str(l)] = ...
    """
    pass


def Update_parameters(parameters, grads, learning_rate):
    """
    Updates parameters using gradient descent
    :param parameters: a python dictionary containing the DNN architecture’s parameters
    :param grads: a python dictionary containing the gradients (generated by L_model_backward)
    :param learning_rate: the learning rate used to update the parameters (the “alpha”)
    :return: parameters – the updated values of the parameters object provided as input
    """
    pass


def L_layer_model(X, Y, layers_dims, learning_rate, num_iterations):
    """
    Implements a L-layer neural network. All layers but the last should have the ReLU activation function, and the final layer will apply the sigmoid activation function. The network should only address binary classification.
    Hint: the function should use the earlier functions in the following order: initialize -> L_model_forward -> compute_cost -> L_model_backward -> update parameters
    :param X: the input data, a numpy array of shape (height*width , number_of_examples)
Comment: since the input is in grayscale we only have height and width, otherwise it would have been height*width*3
    :param Y: the “real” labels of the data, a vector of shape (1, number of examples)
    :param layers_dims: a list containing the dimensions of each layer, including the input
    :param learning_rate:
    :param num_iterations:
    :return: parameters – the parameters learnt by the system during the training (the same parameters that were updated in the update_parameters function).
costs – the values of the cost function (calculated by the compute_cost function). One value
is to be saved after each 100 training iterations (e.g. 3000 iterations -> 30 values).
    """
    pass


def Predict(X, Y, parameters):
    """
    The function receives an input data and the true labels and calculates the accuracy of the trained neural network on the data.
    :param X: the input data, a numpy array of shape (height*width, number_of_examples)
    :param Y: the “real” labels of the data, a vector of shape (1, number of examples)
    :param parameters: a python dictionary containing the DNN architecture’s parameters
    :return: accuracy – the accuracy measure of the neural net on the provided data
    """
    pass


if __name__ == '__main__':
    layers = initialize_parameters([784, 20, 7, 5, 1])
    assert layers is not None
    assert len(layers) == 4
    assert list(layers.keys()) == [0, 1, 2, 3]
    assert layers[0][0].shape == (20, 784)
    assert layers[0][1].shape == (784,)
    assert layers[1][0].shape == (7, 20)
    assert layers[1][1].shape == (20,)
    assert layers[2][0].shape == (5, 7)
    assert layers[2][1].shape == (7,)
    assert layers[3][0].shape == (1, 5)
    assert layers[3][1].shape == (5,)
    pass
