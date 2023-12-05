def levenshtein_metric(self):
        """
        computes levenshtein distance between two strings as a measure for evaluating ocr final result accuracy in
         character level.
        rsc: https://stackoverflow.com/questions/2460177/edit-distance-in-python
        intro: https://en.wikipedia.org/wiki/Levenshtein_distance
        :return:
        """
        if len(self.real_string) > len(self.predicted_string):
            self.real_string, self.predicted_string = self.predicted_string, self.real_string

        distances = range(len(self.real_string) + 1)
        for i2, c2 in enumerate(self.predicted_string):
            distances_ = [i2 + 1]
            for i1, c1 in enumerate(self.real_string):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_

        error = distances[-1] / (self.real_string.__len__() + 1)
        self.chle_levenshtein_accuracy = 100 * (1 - error)
