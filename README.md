# DeepLearningHW1
simple implementation of neural network

# TODO
## Forward propagation
- [x] initialize_parameters(layer_dims) - ofri
- [x] linear_forward(A, W, b) - ofri
- [x] sigmoid(Z) - ofri
- [x] relu(Z) - ofri
- [x] linear_activation_forward(A_prev, W, B, activation) - ofri
- [x] L_model_forward(X, parameters) - ofri
- [x] compute_cost(AL, Y) - ofri
## Backward propagation
- [x] linear_backward(dZ, cache) - nir
- [x] linear_activation_backward(dA, cache, activation) - nir
- [x] relu_backward (dA, activation_cache) - nir
- [x] sigmoid_backward (dA, activation_cache) - nir
- [x] L_model_backward(AL, Y, caches) - nir
- [x] Update_parameters(parameters, grads, learning_rate) - nir
## Training and prediction
- [x] L_layer_model(X, Y, layers_dims, learning_rate, num_iterations) - ofri
- [x] Predict(X, Y, parameters) - ofri
## Toy use case
- [x] extract two types of images from MNIST dataset - nir
- [x] create binary classifier for the types and run the experiments according to the instructions - nir
- [ ] write a report about the experiment - nir + ofri