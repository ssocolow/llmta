# grab what the model needs to use to formulate its answer
# lab spec, student code, unit test code, grade report


# function to read a file
def readfile(s):
    try:
        with open(s, 'r') as file:
            file_contents = file.read()
            # or use file_contents = file.readlines() to get a list of lines

        return file_contents

    except FileNotFoundError:
        print(f"The file '{s}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


# returns the prompt for the llm based on the cli args
def generate_prompt(args):
    LAB_SPEC = readfile(args.spec)

    STUDENT_CODE_file_path = args.usercode

    STUDENT_CODE = readfile(STUDENT_CODE_file_path)

    GRADE_REPORT = readfile(args.result)

    #generate unit test errors, stored in errors_result.txt
    # command = "python test_mathoperations.py 2> errors_result.txt"
    # import os
    # os.system(command)

    # ERRORS = readfile("errors_result.txt")

    # using system message now
    #intro = "You are a teaching assistant for a computer science class. You will respond with questions to the student that will help inform the student. Be constructive and concise. I will tip you $200 if you do well. You will be given the lab specification containing information about their assignment, their code, their grade report, and optionally the code that generated the grade report. "

    spec = "Here is the lab assignment information: [ " + LAB_SPEC + " ]. "

    student_code = "Here is the student's code: [ " + STUDENT_CODE + " ]. "

    grade_report = "Here is their grade report: [ " + GRADE_REPORT + " ]. If there are more than a couple issues, FOCUS ON THE MOST IMPORTANT ONES that will help the student learn computer science principles. "

    # unit_code = "Here is the code of the unit test that failed: [ " + UNIT_TEST_CODE + " ]. "

    # errors = "Here are the errors that were generated: [ " + ERRORS + " ]. "

    ending = "Please provide constructive and concise feedback that will help the student learn computer science concepts."

    # prompt = intro + spec + student_code + grade_report + unit_code + ending
    if args.unittestcode != None:
        UNIT_TEST_CODE_file_path = args.unittestcode
        UNIT_TEST_CODE = readfile(UNIT_TEST_CODE_file_path)

        unit_code = "Here is the code that generated their grade report: [ " + UNIT_TEST_CODE + " ]. "
        prompt = spec + student_code + grade_report + unit_code + ending
        return prompt
    else:
        prompt = spec + student_code + grade_report + ending
        return prompt


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("usercode", type=str,
                        help="user code file")
    parser.add_argument("spec", help="lab specification file")
    parser.add_argument("result", help="grade report / unit test output file")
    parser.add_argument("--unittestcode", help="code that tests the student's code")
    parser.add_argument("--temperature", help="temperature parameter of the llm", type=float)
    parser.add_argument("--model", help="choose between gpt-4-1106-preview with '4' and gpt-3.5-turbo-1106 with '3'", type=int)
    parser.add_argument("--short", help="only output short response", action="store_true")

    args = parser.parse_args()

    prompt = generate_prompt(args)

    if args.temperature != None:
        prompt += " temp: " + str(args.temperature)

    chosen_model = 'gpt 4'
    if args.model != None:
        if args.model == 3:
            chosen_model = 'gpt-3.5-turbo-1106'
            prompt += chosen_model
    if args.short:
        prompt += "SHORT"
    else:
        prompt += "LONG"

    print(prompt)