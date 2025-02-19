# This file attempts to implement the custom node function as explained in the supplement to the original superflexPy paper
# https://gmd.copernicus.org/articles/14/7047/2021/gmd-14-7047-2021-supplement.pdf here. However the current implementation 
# is not working and the internal/external routing methods are not functional. 

from superflexpy.framework.node import Node

class RoutedNode(Node):
    def _internal_routing(self, flux):
        t_internal = self.get_parameters(names=[self._prefix_local_parameters + 't_internal'])

        flux_out = []
        for f in flux:
            flux_out.append(self._route(f, t_internal))
            return flux_out

    def external_routing(self, flux):
        t_external = self.get_parameters(names=[self._prefix_local_parameters + 't_external'])
        flux_out = []
        for f in flux:
            flux_out.append(self._route(f, t_external))
            return flux_out


    def _route(self, flux, time):
        state = np.zeros(int(np.ceil(time)))

        weight = self._calculate_weight(time)


        out = []
        for value in flux:
            state = state + weight * value
            out.append(state[0])
            state[0] = 0
            state = np.roll(state, shift=-1)
        return np.array(out)


    def _calculate_weight(self, time):
        weight = []


        array_length = np.ceil(time)
        for i in range(int(array_length)): weight.append(self._calculate_lag_area(i + 1, time)
                                                         - self._calculate_lag_area(i, time))
        return weight @ staticmethod


    def _calculate_lag_area(portion, time):
        half_time = time / 2


        if portion <= 0:
            value = 0
        elif portion < half_time:
            value = 2 * (portion / time) ** 2
        elif portion < time:
            value = 1 - 2 * ((time - portion) / time) ** 2
        else:
            value = 1
        return value