#get the inputs to the model
from model_inputs import generate_prompt
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

def main():
    from openai import OpenAI
    client = OpenAI()

    # defaults to these if no optional parameters given
    chosen_model = 'gpt-4-1106-preview'
    chosen_temp = 0.5

    if args.model != None:
        if args.model == 3:
            chosen_model = 'gpt-3.5-turbo-1106'

    if args.temperature != None:
        chosen_temp = args.temperature

    # Example of an OpenAI ChatCompletion request with stream=True
    # https://platform.openai.com/docs/guides/chat

    completion = client.chat.completions.create(
    # gpt-4 turbo is gpt-4-1106-preview
    #model='gpt-3.5-turbo-1106',
    model=chosen_model,
    messages=[
        {"role": "system", "content": "You are a teaching assistant for a computer science class. You will respond with questions to the student that will help inform them. Be constructive and concise. I will tip you $200 if you do well. You will be given the lab specification containing information about their assignment, their code, their grade report, and optionally the code that generated the grade report. "},
        {"role": "user", "content": "I will now give you these files, ASK QUESTIONS TO PROMPT THE STUDENT'S THINKING. "},
        {"role": "user", "content": prompt},
    ],
    temperature=chosen_temp,
    seed=1337,
    max_tokens=800,
    #stream=True  # this time, we set stream=True
    )

    long_advice = completion.choices[0].message.content

    if not args.short:
        print(long_advice)
        print("================================\n")

    completion2 = client.chat.completions.create(
    # gpt-4 turbo is gpt-4-1106-preview
    #model='gpt-3.5-turbo-1106',
    model=chosen_model,
    messages=[
        {"role": "system", "content": "You are a teaching assistant for a computer science class. You will RESPOND WITH QUESTIONS to the student that will help them learn. Be constructive and concise. I will tip you $200 if you do well."},
        {"role": "user", "content": "Here are some possible questions to prompt the student's thinking: [ " + long_advice + " ] I want you to pick one that is specific and actionable, only ONE, and ask it to them.  Respond with only the question, nothing else."},
    ],
    temperature=chosen_temp,
    seed=1337,
    max_tokens=800,
    #stream=True  # this time, we set stream=True
    )

    short_advice = completion2.choices[0].message.content
    print(short_advice)


if __name__ == "__main__":
    main()