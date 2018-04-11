# DeepLearningHW1
simple implementation of neural network

# TODO
## Forward propagation
- [x] initialize_parameters(layer_dims)
- [x] linear_forward(A, W, b)
- [x] sigmoid(Z)
- [x] relu(Z)
- [x] linear_activation_forward(A_prev, W, B, activation)
- [x] L_model_forward(X, parameters)
- [x] compute_cost(AL, Y)
## Backward propagation
- [ ] linear_backward(dZ, cache) - nir
- [ ] linear_activation_backward(dA, cache, activation) - nir
- [ ] relu_backward (dA, activation_cache) - nir
- [ ] sigmoid_backward (dA, activation_cache) - nir
- [ ] L_model_backward(AL, Y, caches) - nir
- [ ] Update_parameters(parameters, grads, learning_rate) - nir
## Training and prediction
- [ ] L_layer_model(X, Y, layers_dims, learning_rate, num_iterations) - ofri
- [ ] Predict(X, Y, parameters) - ofri
## Toy use case
- [ ] extract two types of images from MNIST dataset - nir
- [ ] create binary classifier for the types and run the experiments according to the instructions - nir
- [ ] write a report about the experiment - nir