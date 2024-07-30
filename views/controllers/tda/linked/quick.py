class QuickSort:
    def partition(self, array, low, high, attribute, ascending=True):
        pivot = array[high]
        i = low - 1
        
        for j in range(low, high):
            # Obtener el valor del atributo para comparar
            value_j = getattr(array[j], attribute)
            value_pivot = getattr(pivot, attribute)
            
            if ascending:
                if value_j <= value_pivot:
                    i += 1
                    array[i], array[j] = array[j], array[i]
            else:
                if value_j >= value_pivot:
                    i += 1
                    array[i], array[j] = array[j], array[i]
        
        array[i + 1], array[high] = array[high], array[i + 1]
        return i + 1

    def quick_sort(self, array, low, high, attribute, ascending=True):
        if low < high:
            pi = self.partition(array, low, high, attribute, ascending)
            self.quick_sort(array, low, pi - 1, attribute, ascending)
            self.quick_sort(array, pi + 1, high, attribute, ascending)
        return array

    def sort_models_ascendent(self, array, attribute):
        return self.quick_sort(array, 0, len(array) - 1, attribute, ascending=True)

    def sort_models_descendent(self, array, attribute):
        return self.quick_sort(array, 0, len(array) - 1, attribute, ascending=False)