class Lecture(object):
    def __init__(self, _pass, title, scores):
        self.__pass: int = _pass
        self.__title: str = title
        self.__scores: [] = scores

    @property
    def scores(self):
        return self.__scores

    @property
    def _pass(self):
        return self.__pass

    def average(self) -> []:
        return self.__scores

    def evaluate(self) -> str:
        return f'Pass: {self.pass_count()} Fail: {self.fail_count()}'

    def fail_count(self) -> int:
        return len(self.__scores) - self.pass_count()

    def pass_count(self) -> int:
        passed = []
        for _ in self.scores:
            if _ >= self.__pass:
                passed.append(_)
        return len(passed)
        # return len([_ for _ in self.scores if _ >= self.__pass])

    def stats(self):
        return f'Title: {self.__title}, Evaluation Method: {self.get_evaluation_method()}'

    def get_evaluation_method(self) -> str:
        return 'Pass or Fail'


class Grade(object):
    def __init__(self, name, upper, lower):
        self.__name: str = name
        self.__upper: int = upper
        self.__lower: int = lower

    @property
    def name(self) -> str:
        return self.__name

    def is_name(self, name: str) -> bool:
        return self.__name == name

    def include(self, score: int) -> bool:
        return self.__lower <= score <= self.__upper


class GradeLecture(Lecture):
    def __init__(self, _pass, title, scores, grades):
        super().__init__(_pass, title, scores)
        self.__grades: [] = grades

    def evaluate(self) -> str:
        return super(GradeLecture, self).evaluate() + ', ' + self._grades_statistics()

    def _grades_statistics(self) -> str:
        formatted = [self._formatter(grade) for grade in self.__grades]
        return ' '.join(formatted)

    def _formatter(self, grade: Grade) -> str:
        return f'{grade.name}: {self._grade_count(grade)}'

    def _grade_count(self, grade: Grade) -> int:
        tmp = []
        for _ in self.scores:
            if grade.include(_):
                tmp.append(_)
        return len(tmp)


class Professor(object):
    def __init__(self, name, lecture):
        self.__name: str = name
        self.__lecture: Lecture = lecture

    def compile_statistics(self):
        return f'{self.__name}, {self.__lecture.evaluate()}, {self.__lecture.average()}'


class FormattedGradeLecture(GradeLecture):
    def __init__(self, _pass, grades, scores, title):
        super().__init__(_pass, title, scores, grades)

    def format_average(self):
        return f'Avg: {super().average()}'


if __name__ == '__main__':
    # lecture = Lecture(_pass=70, title='test', scores=[81, 95, 75, 50, 45])
    # evaluate = lecture.evaluate()
    # print(evaluate)

    # gradelecture = GradeLecture(title='test', _pass=70,
    #                             scores=[Grade('A', 100, 95), Grade('B', 94, 80), Grade('C', 79, 70),
    #                                     Grade('D', 69, 50), Grade('F', 49, 0)],
    #                             grades=[81, 95, 75, 50, 45])
    #
    # gradelecture.evaluate()
    professor = Professor('다익스트라', GradeLecture(title='알고리즘', _pass=70,
                                                grades=[Grade('A', 100, 95), Grade('B', 94, 80), Grade('C', 79, 70),
                                                        Grade('D', 69, 50), Grade('F', 49, 0)],
                                                scores=[81, 95, 75, 50, 45]))
    statistics = professor.compile_statistics()

    formatted_grade_lecture = FormattedGradeLecture(_pass=70, title='테스트', scores=[81, 95, 75, 50, 45],
                                                    grades=[Grade('A', 100, 95), Grade('B', 94, 80), Grade('C', 79, 70),
                                                            Grade('D', 69, 50), Grade('F', 49, 0)])
    print(formatted_grade_lecture.format_average())
