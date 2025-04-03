import pytest
from model import Question, Choice

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('', False)
    with pytest.raises(Exception):
        question.add_choice('a' * 101, False)

def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', False)

    assert len(question.choices) == 3
    assert question.choices[0].text == 'a'
    assert question.choices[1].text == 'b'
    assert question.choices[2].text == 'c'
    assert not question.choices[0].is_correct
    assert question.choices[1].is_correct
    assert not question.choices[2].is_correct

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)

    question.remove_choice_by_id(choice1.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == choice2.id
    assert question.choices[0].text == 'b'

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a', False)
    question.add_choice('b', True)
    question.add_choice('c', False)

    question.remove_all_choices()

    assert len(question.choices) == 0

def test_select_choices_within_limit():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)
    choice3 = question.add_choice('c', True)

    selected = question.select_choices([choice2.id, choice3.id])

    assert len(selected) == 2
    assert choice2.id in selected
    assert choice3.id in selected

def test_select_choices_exceeding_limit():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)

    with pytest.raises(Exception):
        question.select_choices([choice1.id, choice2.id])

def test_set_correct_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)

    question.set_correct_choices([choice1.id])

    assert question.choices[0].is_correct
    assert not question.choices[1].is_correct

def test_invalid_choice_id():
    question = Question(title='q1')
    choice = question.add_choice('a', False)

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_choice_ids_are_sequential():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', False)

    assert choice1.id == 1
    assert choice2.id == 2
    assert choice3.id == 3

    question.remove_choice_by_id(choice2.id)
    choice4 = question.add_choice('d', False)

    assert choice4.id == 4  # IDs should still increment, not reuse deleted IDs