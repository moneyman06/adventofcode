import copy
import queue


class IntCode:
    def __init__(self, raw_code, input_queue=None):
        self._original_code = list(map(lambda x: int(x), raw_code.strip().split(",")))
        self.input_queue = input_queue
        self.output_queue = queue.SimpleQueue()

    def run(self):
        self._code = copy.deepcopy(self._original_code)
        self._location = 0
        self._last_output = None
        self._done = False

        while not self._done:
            self._step()

        return self._last_output

    def _step(self):
        op = self._code[self._location]
        op_type = self._get_op_type(op)

        if op_type == 1:
            parameter_modes = self._get_parameter_modes(op, 2)
            parameters = self._get_parameters(parameter_modes)
            self._handle_add(parameters)
        elif op_type == 2:
            parameter_modes = self._get_parameter_modes(op, 2)
            parameters = self._get_parameters(parameter_modes)
            self._handle_mulitply(parameters)
        elif op_type == 3:
            self._handle_input()
        elif op_type == 4:
            parameter_modes = self._get_parameter_modes(op, 1)
            parameters = self._get_parameters(parameter_modes)
            self._handle_output(parameters)
        elif op_type == 5:
            parameter_modes = self._get_parameter_modes(op, 2)
            parameters = self._get_parameters(parameter_modes)
            self._handle_jump_if_true(parameters)
        elif op_type == 6:
            parameter_modes = self._get_parameter_modes(op, 2)
            parameters = self._get_parameters(parameter_modes)
            self._handle_jump_if_false(parameters)
        elif op_type == 7:
            parameter_modes = self._get_parameter_modes(op, 2)
            parameters = self._get_parameters(parameter_modes)
            self._handle_less_than(parameters)
        elif op_type == 8:
            parameter_modes = self._get_parameter_modes(op, 2)
            parameters = self._get_parameters(parameter_modes)
            self._handle_equal(parameters)
        elif op_type == 99:
            self._done = True
        else:
            msg = "Operation of type {} not supported".format(op_type)
            raise Exception(msg)

    def _get_op_type(self, op):
        return op % 100

    def _get_parameter_modes(self, op, require_n):
        l = list(map(lambda x: int(x), list(str(op)[:-2])))
        l.reverse()
        pad_n = require_n - len(l)
        l += [0] * pad_n
        return l

    def _get_parameters(self, parameter_modes):
        def map_func(x):
            idx, mode = x
            if mode == 0:
                return self._code[self._code[self._location + idx + 1]]
            elif mode == 1:
                return self._code[self._location + idx + 1]
            else:
                msg = "Parameter mode {} not recognized".format(mode)
                raise Exception(msg)

        return list(map(map_func, enumerate(parameter_modes)))

    def _handle_add(self, parameters):
        left = parameters[0]
        right = parameters[1]
        self._code[self._code[self._location + 3]] = left + right
        self._location += 4

    def _handle_mulitply(self, parameters):
        left = parameters[0]
        right = parameters[1]
        self._code[self._code[self._location + 3]] = left * right
        self._location += 4

    def _handle_input(self):
        inpt = self.input_queue.get()
        self._code[self._code[self._location + 1]] = inpt
        self._location += 2

    def _handle_output(self, parameters):
        value = parameters[0]
        self._last_output = value
        self.output_queue.put(value)
        self._location += 2

    def _handle_jump_if_true(self, parameters):
        flag = parameters[0]
        if flag != 0:
            self._location = parameters[1]
        else:
            self._location += 3

    def _handle_jump_if_false(self, parameters):
        flag = parameters[0]
        if flag == 0:
            self._location = parameters[1]
        else:
            self._location += 3

    def _handle_less_than(self, parameters):
        left = parameters[0]
        right = parameters[1]
        self._code[self._code[self._location + 3]] = 1 if left < right else 0
        self._location += 4

    def _handle_equal(self, parameters):
        left = parameters[0]
        right = parameters[1]
        self._code[self._code[self._location + 3]] = 1 if left == right else 0
        self._location += 4
