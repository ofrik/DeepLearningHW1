# DeepLearningHW1
simple implementation of neural network

# TODO
## Forward propagation
- [x] initialize_parameters(layer_dims)
- [x] linear_forward(A, W, b) - not tested
- [x] sigmoid(Z) - not tested
- [x] relu(Z) - not tested
- [x] linear_activation_forward(A_prev, W, B, activation) - not tested
- [x] L_model_forward(X, parameters) - not tested
- [ ] compute_cost(AL, Y)
## Backward propagation
- [ ] linear_backward(dZ, cache)
- [ ] linear_activation_backward(dA, cache, activation)
- [ ] relu_backward (dA, activation_cache)
- [ ] sigmoid_backward (dA, activation_cache)
- [ ] L_model_backward(AL, Y, caches)
- [ ] Update_parameters(parameters, grads, learning_rate)
## Training and prediction
- [ ] L_layer_model(X, Y, layers_dims, learning_rate, num_iterations)
- [ ] Predict(X, Y, parameters)
## Toy use case
- [ ] extract two types of images from MNIST dataset
- [ ] create binary classifier for the types and run the experiments according to the instructions
- [ ] write a report about the experiment