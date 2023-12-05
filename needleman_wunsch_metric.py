 def needleman_wunsch_metric(self):
        """
        Applies Needleman–Wunsch algorithm as a measure for evaluating ocr final result accuracy in character level.
        rsc: https://github.com/alevchuk/pairwise-alignment-in-python
        intro: https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm
        :return:
        """
        m, n = len(self.real_string), len(self.predicted_string)  # length of two sequences

        # Generate DP table and traceback path pointer matrix
        score = self.zeros((m + 1, n + 1))  # the DP table

        # Calculate DP table
        for i in range(0, m + 1):
            score[i][0] = self.gap_penalty * i
        for j in range(0, n + 1):
            score[0][j] = self.gap_penalty * j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                match = score[i - 1][j - 1] + self.match_score(self.real_string[i - 1], self.predicted_string[j - 1])
                delete = score[i - 1][j] + self.gap_penalty
                insert = score[i][j - 1] + self.gap_penalty
                score[i][j] = max(match, delete, insert)

        # Traceback and compute the alignment
        align1, align2 = '', ''
        i, j = m, n  # start from the bottom right cell
        while i > 0 and j > 0:  # end toching the top or the left edge
            score_current = score[i][j]
            score_diagonal = score[i - 1][j - 1]
            score_up = score[i][j - 1]
            score_left = score[i - 1][j]

            if score_current == score_diagonal + self.match_score(self.real_string[i - 1], self.predicted_string[j - 1]):
                align1 += self.real_string[i - 1]
                align2 += self.predicted_string[j - 1]
                i -= 1
                j -= 1
            elif score_current == score_left + self.gap_penalty:
                align1 += self.real_string[i - 1]
                align2 += '-'
                i -= 1
            elif score_current == score_up + self.gap_penalty:
                align1 += '-'
                align2 += self.predicted_string[j - 1]
                j -= 1

        # Finish tracing up to the top left cell
        while i > 0:
            align1 += self.real_string[i - 1]
            align2 += '-'
            i -= 1
        while j > 0:
            align1 += '-'
            align2 += self.predicted_string[j - 1]
            j -= 1

        self.chle_needleman_wunsch_accuracy = self.finalize(align1, align2)
