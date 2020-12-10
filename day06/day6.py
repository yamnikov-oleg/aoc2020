from dataclasses import dataclass, field
from typing import Dict, List, Set


@dataclass
class PersonAnswers:
    answered_yes_to: List[str] = field(default_factory=list)


@dataclass
class GroupAnswers:
    people_answers: List[PersonAnswers] = field(default_factory=list)

    @property
    def anyone_answered_yes_to(self) -> Set[str]:
        answered_yes_to = set()
        for person_answers in self.people_answers:
            answered_yes_to.update(person_answers.answered_yes_to)
        return answered_yes_to

    @property
    def everyone_answered_yes_to(self) -> Set[str]:
        count_answers: Dict[str, int] = {}
        for person_answers in self.people_answers:
            for question in person_answers.answered_yes_to:
                count_answers.setdefault(question, 0)
                count_answers[question] += 1

        answered_yes_to = set()
        for question, answers_count in count_answers.items():
            if answers_count == len(self.people_answers):
                answered_yes_to.add(question)
        return answered_yes_to


def parse_answers(input: str) -> List[GroupAnswers]:
    groups = []
    group_inputs = input.split('\n\n')
    for group_input in group_inputs:
        group = GroupAnswers()
        people_inputs = group_input.strip().split('\n')
        for person_input in people_inputs:
            person_answers = PersonAnswers(answered_yes_to=list(person_input.strip()))
            group.people_answers.append(person_answers)
        groups.append(group)
    return groups


def get_sum_of_anyone_answered_yes_to(groups: List[GroupAnswers]) -> int:
    sum_of_answers = 0
    for group in groups:
        sum_of_answers += len(group.anyone_answered_yes_to)
    return sum_of_answers


def get_sum_of_everyone_answered_yes_to(groups: List[GroupAnswers]) -> int:
    sum_of_answers = 0
    for group in groups:
        sum_of_answers += len(group.everyone_answered_yes_to)
    return sum_of_answers


def main():
    with open('./input.txt') as f:
        groups = parse_answers(f.read())

    sum_of_answers_anyone = get_sum_of_anyone_answered_yes_to(groups)
    print(f"Sum of question anyone answered yes to: {sum_of_answers_anyone}")

    sum_of_answers_everyone = get_sum_of_everyone_answered_yes_to(groups)
    print(f"Sum of question everyone answered yes to: {sum_of_answers_everyone}")


if __name__ == "__main__":
    main()
