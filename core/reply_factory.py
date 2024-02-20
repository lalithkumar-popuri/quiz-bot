
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    current_question = PYTHON_QUESTION_LIST[current_question_id]

    # Validate if the answer provided by the user is correct
    if answer == current_question['answer']:
        # If the answer is correct, store it in the session
        session['answers'] = session.get('answers', {})
        session['answers'][current_question_id] = answer
        session.save()
        return True, ""  # Success
    else:
        return False, "Sorry, that's not the correct answer. Please try again."


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    next_question_id = current_question_id + 1

    # Check if there is a next question available
    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question_text']
        return next_question, next_question_id
    else:
        return None, None


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = sum(1 for answer in session.get('answers', {}).values() if answer)
    score = (correct_answers / total_questions) * 100

    final_response = f"You have completed the quiz! Your score is {score:.2f}%."
    return final_response
