import google.generativeai as genai
from config import gemini_token , prompt , askl_prompt


def general(history):
    global prompt
    genai.configure(api_key=gemini_token)

    prompt += "Chat History: \n"


    for item in history:
        prompt += item + '\n'
    prompt += "\nRespond as L. "
    print("AIPROMPT:", prompt)
    
    model = genai.GenerativeModel("gemini-1.5-pro")
    tries = 3
    while tries > 0:
        try:
            response = model.generate_content(prompt)
            return (response.text)
        except ValueError as e:
            print("Trying Again.....Tries:", tries)
            tries -= 1
        except:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return (response.text)
        


def askl(question_with_history):
    global askl_prompt
    genai.configure(api_key=gemini_token) 
    askl_prompt += question_with_history
    print(askl_prompt)
    model = genai.GenerativeModel("gemini-1.5-pro")
    tries = 3
    while tries > 0:
        try:
            response = model.generate_content(prompt)
            return (response.text)
        except ValueError as e:
            print("Trying Again.....Tries:", tries)
            tries -= 1
        except:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return (response.text)
        




        

