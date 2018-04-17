import numpy as np
import os
import struct
import warnings

warnings.filterwarnings("ignore")


def initialize_parameters(layer_dims):
    """

    :param layer_dims: an array of the dimensions of each layer in the network (layer 0 is the size of the flattened input, layer L is the output sigmoid)
    :return: a dictionary containing the initialized W and b parameters of each layer (W1…WL, b1…bL).

    Hint: Use the randn and zeros functions of numpy to initialize W and b, respectively
    """
    output = {}
    for i, layer_size in enumerate(layer_dims[:-1]):
        output["W%s" % (i + 1)] = np.random.randn(layer_dims[i + 1], layer_dims[i]) * 0.05
        output["b%s" % (i + 1)] = np.zeros((layer_dims[i + 1], 1))
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
    linear_cache = (A.copy(), W.copy(), b.copy())
    return Z, linear_cache


def sigmoid(Z):
    """

    :param Z: the linear component of the activation function
    :return: A – the activations of the layer
            activation_cache – returns Z, which will be useful for the backpropagation
    """
    A = 1 / (1 + np.exp(-Z))
    return A, Z.copy()


def relu(Z):
    """

    :param Z: the linear component of the activation function
    :return: A – the activations of the layer
            activation_cache – returns Z, which will be useful for the backpropagation
    """
    A = np.maximum(Z, 0)
    return A, Z.copy()


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
    Z, linear_cache = linear_forward(A_prev, W, B)
    A, activation_cache = activation_function(Z)
    return A, (linear_cache, activation_cache)


def L_model_forward(X, parameters):
    """
    Implement forward propagation for the [LINEAR->RELU]*(L-1)->LINEAR->SIGMOID computation
    :param X: the data, numpy array of shape (input size, number of examples)
    :param parameters: the initialized W and b parameters of each layer
    :return: AL – the last post-activation value
            caches – a list of all the cache objects generated by the linear_forward function
    """
    caches = []
    A_prev = X
    num_layers = (int)(len(parameters) / 2)
    for layer in range(1, num_layers + 1):
        if layer == num_layers:
            activation = "sigmoid"
        else:
            activation = "relu"
        A_prev, cache = linear_activation_forward(A_prev.copy(), parameters["W%s" % layer],
                                                  parameters["b%s" % layer],
                                                  activation)
        caches.append(cache)
    return A_prev, caches


def compute_cost(AL, Y):
    """
    Implement the cost function defined by equation
𝑐𝑜𝑠𝑡=−1/𝑚(Σ[(𝑦𝑖∗log(𝐴𝐿))+((1−𝑦𝑖)∗(1−𝐴𝐿))]) (see the slides of the first lecture for additional information if needed).
    :param AL: probability vector corresponding to your label predictions, shape (1, number of examples)
    :param Y: the labels vector (i.e. the ground truth)
    :return: cost – the cross-entropy cost
    """
    m = AL.shape[-1]
    cost = (-1 / m) * np.sum((np.multiply(Y, np.log(AL))) + np.multiply(1. - Y, np.log(1. - AL)))
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
    A_prev, W, b = cache
    m = A_prev.shape[1]

    dA_prev = np.dot(W.T, dZ)
    dW = (1. / m) * np.dot(dZ, A_prev.T)
    db = (1. / m) * np.sum(dZ, axis=1, keepdims=True)

    return dA_prev, dW, db


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
    if (activation == 'relu'):
        dZ = relu_backward(dA, cache[1])

    else:  # if activation is sigmoid
        dZ = sigmoid_backward(dA, cache[1])

    dA_prev, dW, db = linear_backward(dZ, cache[0])
    return dA_prev, dW, db


def relu_backward(dA, activation_cache):
    """
    Implements backward propagation for a ReLU unit
    :param dA: the post-activation gradient
    :param activation_cache: contains Z (stored during the forward propagation)
    :return: dZ – gradient of the cost with respect to Z
    """
    dZ = np.array(dA, copy=True)
    Z = activation_cache
    dZ[Z <= 0] = 0
    return dZ


def sigmoid_backward(dA, activation_cache):
    """
    Implements backward propagation for a sigmoid unit
    :param dA: the post-activation gradient
    :param activation_cache: contains Z (stored during the forward propagation)
    :return: dZ – gradient of the cost with respect to Z
    """

    A, _ = sigmoid(activation_cache)
    dZ = dA * A * (1.0 - A)
    return dZ


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
    grads = {}
    num_layers = len(caches)
    Y = Y.reshape(AL.shape)

    dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))  # the output layer gradient
    # dAL = Y - AL

    # compute sigmoid layer gradient - only done once on the last layer
    curr_cache = caches[-1]
    tmp_A, temp_W, temp_b = linear_activation_backward(dAL, curr_cache, 'sigmoid')
    grads["dA%s" % num_layers] = tmp_A
    grads["dW%s" % num_layers] = temp_W
    grads["db%s" % num_layers] = temp_b

    # compute relu layers gradients
    for layer in reversed(range(1, num_layers)):
        curr_cache = caches[layer - 1]
        tmp_A, temp_W, temp_b = linear_activation_backward(grads["dA%s" % (layer + 1)], curr_cache, 'relu')
        grads["dA%s" % layer] = tmp_A
        grads["dW%s" % layer] = temp_W
        grads["db%s" % layer] = temp_b

    return grads


def Update_parameters(parameters, grads, learning_rate):
    """
    Updates parameters using gradient descent
    :param parameters: a python dictionary containing the DNN architecture’s parameters
    :param grads: a python dictionary containing the gradients (generated by L_model_backward)
    :param learning_rate: the learning rate used to update the parameters (the “alpha”)
    :return: parameters – the updated values of the parameters object provided as input
    """
    num_layers = round(len(parameters) / 2)  # because each layer has both b and W

    for layer in range(1, num_layers + 1):
        parameters["W%s" % layer] -= learning_rate * grads["dW%s" % layer]
        parameters["b%s" % layer] -= learning_rate * grads["db%s" % layer]
    return parameters


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
    costs = []
    parameters = initialize_parameters(layers_dims)
    for i in range(1, num_iterations + 1):
        AL, caches = L_model_forward(X, parameters)
        cost = compute_cost(AL, Y)
        if i % 100 == 0:
            print("Iteration %s: cost - %s" % (i, cost))
            costs.append(cost)
        grads = L_model_backward(AL, Y, caches)
        parameters = Update_parameters(parameters, grads, learning_rate)
    return parameters, costs


def Predict(X, Y, parameters):
    """
    The function receives an input data and the true labels and calculates the accuracy of the trained neural network on the data.
    :param X: the input data, a numpy array of shape (height*width, number_of_examples)
    :param Y: the “real” labels of the data, a vector of shape (1, number of examples)
    :param parameters: a python dictionary containing the DNN architecture’s parameters
    :return: accuracy – the accuracy measure of the neural net on the provided data
    """
    preds, caches = L_model_forward(X, parameters)
    preds = np.round(preds[0])
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for pred, actual in zip(preds, Y):
        if pred == actual and pred == 1:
            TP += 1
        elif pred == 1 and actual == 0:
            FP += 1
        elif pred == 0 and actual == 1:
            FN += 1
        elif pred == actual and pred == 0:
            TN += 1
    return (TP + TN) / (TP + TN + FP + FN)


def getData(path, fname_img, fname_lbl, relevant_lbls):
    """
    Reads the data files, and extracts only the relevant instances
    :param path: the path to folder containing the data
    :return: accuracy – the accuracy measure of the neural net on the provided data
    """
    with open(fname_lbl, 'rb') as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)

    with open(fname_img, 'rb') as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows, cols)

    X = []
    Y = []
    # Create an iterator which returns each image in turn
    for i in range(len(lbl)):
        curr_lbl = lbl[i]
        if (curr_lbl == relevant_lbls[0]):
            curr_img = np.array(img[i])
            X.append(curr_img.flatten())
            Y.append(0)  # will be 0 for 3\7

        if (curr_lbl == relevant_lbls[1]):
            curr_img = np.array(img[i])
            X.append(curr_img.flatten())
            Y.append(1)  # will be 1 for 8\9

    X_np = np.array(X)
    Y_np = np.array(Y)
    return X_np, Y_np


def tests():
    #### Build tests NN
    parameters = initialize_parameters([784, 20, 7, 5, 1])
    assert parameters is not None
    assert len(parameters) == 4 * 2
    assert parameters["W1"].shape == (20, 784)
    assert parameters["b1"].shape == (20, 1)
    assert parameters["W2"].shape == (7, 20)
    assert parameters["b2"].shape == (7, 1)
    assert parameters["W3"].shape == (5, 7)
    assert parameters["b3"].shape == (5, 1)
    assert parameters["W4"].shape == (1, 5)
    assert parameters["b4"].shape == (1, 1)
    #### Forward tests
    assert len(sigmoid(np.random.rand(10))[0]) == 10
    assert len(relu(np.random.rand(10))[0]) == 10
    Z, _ = linear_forward(np.random.randn(3, 1), np.random.randn(4, 3), np.random.randn(4, 1))
    assert Z.shape == (4, 1)
    AL, cache = L_model_forward(np.random.randn(784, 40), parameters)
    assert AL.shape == (1, 40)
    cost = compute_cost(AL, np.random.random_integers(0, 1, 40))
    assert isinstance(cost, float)
    #### Backward tests
    # relu_backward()
    # sigmoid_backward()
    #### Predict tests
    acc = Predict(np.random.randn(784, 1000), np.random.random_integers(0, 1, 1000), parameters)
    print(acc)
    assert 0.45 < acc < 0.55
    ### Train tests
    trained_parameters, costs = L_layer_model(np.random.randn(784, 1000), np.random.random_integers(0, 1, 1000),
                                              [784, 20, 7, 5, 1], 0.009, 3000)
    acc_trained = Predict(np.random.randn(784, 1000), np.random.random_integers(0, 1, 1000), trained_parameters)
    print(acc_trained)
    assert acc_trained > acc
    assert len(costs) == 30


if __name__ == '__main__':
    path = './'

    # tests()

    #### Load training Data
    fname_img_train = os.path.join(path, 'train-images.idx3-ubyte')
    fname_lbl_train = os.path.join(path, 'train-labels.idx1-ubyte')

    X_train_3_8, Y_train_3_8 = getData(path, fname_img_train, fname_lbl_train, [3, 8])
    X_train_7_9, Y_train_7_9 = getData(path, fname_img_train, fname_lbl_train, [7, 9])

    #### Load testing Data
    fname_img_test = os.path.join(path, 't10k-images.idx3-ubyte')
    fname_lbl_test = os.path.join(path, 't10k-labels.idx1-ubyte')

    X_test_3_8, Y_test_3_8 = getData(path, fname_img_test, fname_lbl_test, [3, 8])
    X_test_7_9, Y_test_7_9 = getData(path, fname_img_test, fname_lbl_test, [7, 9])
    # np.random.seed(1)
    print("%s Classifier for MNIST 3 and 8 %s" % ("#" * 40, "#" * 40))
    params_classifier_1, costs_1 = L_layer_model(X_train_3_8.T, Y_train_3_8,
                                                 [784, 20, 7, 5, 1], 0.009, 3000)
    accuracy_1 = Predict(X_test_3_8.T, Y_test_3_8, params_classifier_1)
    print("Accuracy: %s\n\n" % accuracy_1)
    print("%s Classifier for MNIST 7 and 9 %s" % ("#" * 40, "#" * 40))
    params_classifier_2, costs_2 = L_layer_model(X_train_7_9.T, Y_train_7_9,
                                                 [784, 20, 7, 5, 1], 0.009, 3000)
    accuracy_2 = Predict(X_test_7_9.T, Y_test_7_9, params_classifier_2)
    print("Accuracy: %s" % accuracy_2)
