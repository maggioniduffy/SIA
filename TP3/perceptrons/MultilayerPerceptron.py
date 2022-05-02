from utils import * 

class NeuronLayer:
    def __init__(self, neurons_qty, inputs=None, activation="tanh"):
        self.neurons_qty = neurons_qty
        self.inputs = inputs
        (f, df) = self.get_functions(activation)
        self.f = f
        self.df = df
        self.weights = None
        self.h = None
        self.v = None

    def init_weights(self, inputs=None):
        self.inputs = inputs if inputs is not None else self.inputs
        print()
        if inputs is None:
            print("inputs + 1 = ", self.inputs+1)
        else:
            print("inputs + 1 = ", inputs+1)
        print("neurons qty = ", self.neurons_qty)
        self.weights = 2 * np.random.random((self.neurons_qty, self.inputs+1)) - 1
        print(self.weights)

    def get_functions(self, activation_function):
        f = tanh_act
        df = der_tanh_act
        return f, df

    def forward(self, a_input):
        a_input_biased = np.insert(a_input, 0, 1)
        output = np.matmul(self.weights, np.transpose(a_input_biased)) 
        output = np.transpose(output)
        self.h = output
        output = self.f(output)
        self.v = output
        return output

    def back_propagate(self, dif, v, eta):
        v = np.insert(v, 0, 1)
        delta = np.multiply(self.df(self.h), dif)
        aux = v.reshape((-1,1))
        d_w = eta*v.reshape((-1,1))*delta
        self.weights = self.weights + np.transpose(d_w)
        return delta


class MultiLayerPerceptron:
    def __init__(self, neuron_layers, eta=0.01, delta=0.049):
        self.eta = eta
        self.delta = delta
        self.neuron_layers = neuron_layers
        self._init_layers()

    def _init_layers(self):
        for i in range(len(self.neuron_layers)):
            if i != 0: 
                self.neuron_layers[i].init_weights(inputs=self.neuron_layers[
                    i - 1].neurons_qty)
            else:
                self.neuron_layers[i].init_weights()

    def predict(self, a_input):
        res = a_input
        for i in range(len(self.neuron_layers)):
            res = self.neuron_layers[i].forward(res)
        return res

    def calculate_mean_square_error(self, training_set, expected_set):
        sum = 0
        for i in range(len(training_set)):
            x = training_set[i]
            y = expected_set[i]

            predicted = self.predict(x)
            aux = np.linalg.norm(predicted - y, ord=2) ** 2
            sum += aux
        return sum / len(training_set)

    def back_propagate(self, predicted, x, y):
        delta = None
        for i in reversed(range(len(self.neuron_layers))):
            if i == 0:
                v = x
            else:
                v = self.neuron_layers[i-1].v
            if i != len(self.neuron_layers)-1:
                dif = np.matmul(np.transpose(self.neuron_layers[i+1].weights[:, 1:]), np.transpose(delta))
                dif = np.transpose(dif)
                dif = np.array(dif)
            else:
                dif = y - predicted

            delta = self.neuron_layers[i].back_propagate(dif, v, self.eta)
        return delta


    def train(self, training_set, expected_set,test_set, expected_test_set, subitem, error_epsilon=0, iterations_qty=10000, print_data=True):
        training_set = np.array(training_set)
        expected_set = np.array(expected_set)
        ii = 0
        i = 0
        print(len(training_set))
        shuffled_list = [a for a in range(0, len(training_set))]
        random.shuffle(shuffled_list)
        p = len(training_set)
        l = len(test_set)
        Error = 1
        min_error = 2 * p
        min_error_test = 2*l
        errors = []
        training_accuracies = []
        epochs = []
        training_correct_cases = 0
        test_correct_cases = 0
        mean_square_error = 0
        test_accuracies = []
        while ii < iterations_qty and Error > error_epsilon:
            j = 0
            training_correct_cases = 0
            test_correct_cases = 0
            while j < len(training_set):
                print("LEN", len(expected_set))
                print("SHUFFLED", shuffled_list)
                print("J", j)
                x = training_set[shuffled_list[j]]
                y = expected_set[shuffled_list[j]]

                predicted_value = self.predict(x)

                error = self.back_propagate(predicted_value, x, y)
                aux_training = 0
                if subitem == 3:
                    max_index = np.where(predicted_value == np.amax(predicted_value))
                    if max_index[0] == shuffled_list[j]:
                        training_correct_cases += 1
                else:
                    for i in range(len(error)):
                        if error[i] < self.delta:
                            aux_training += 1
                    if aux_training == len(error):
                        training_correct_cases += 1

                j += 1
            training_accuracies.append(training_correct_cases/len(training_set))
            Error = self.calculate_mean_square_error(training_set, expected_set)
            if Error < min_error:
                min_error = Error
            errors.append(Error)

            aux_test = 0
            for i in range(len(test_set)):
                if subitem == 3:
                    res = self.predict(np.array(test_set[i]))
                    max_index = np.where(res == np.amax(res))
                    if max_index[0] == i:
                        test_correct_cases += 1
                else:
                    if expected_test_set[i] == 1:
                        error = expected_test_set[i] - self.predict(test_set[i])
                    else:
                        error = expected_test_set[i] + self.predict(test_set[i])
                    if error < self.delta:
                        test_correct_cases += 1

            test_accuracies.append(test_correct_cases/len(test_set))
            mean_square_error = self.calculate_mean_square_error(test_set, expected_test_set)
            if mean_square_error < min_error_test:
                min_error_test = mean_square_error

            epochs.append(ii)
            ii += 1

        return min_error, errors, epochs, training_accuracies, test_accuracies, min_error_test

    def test(self, test_set, expected_test):
        return self.calculate_mean_square_error(test_set, expected_test)
