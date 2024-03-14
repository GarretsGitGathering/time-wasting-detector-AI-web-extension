import google.generativeai as genai


def identify_bad_habits(history):

    genai.configure(api_key="***API_KEY***")

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat()

    response = chat.send_message("""
                                 Here is a log of the webpages a student visits when they should be studying,\n
                                 \n
                                 here is the log:\n
                                 """+history+"""\n
                                 \n
                                 Based on this history log, please make a personalized list on how the student tends to get distracted\n
                                 """)

    response.resolve()

    return response.text

def main():
    response = identify_bad_habits("""
                        {
                           "context prediction": "not wasting time",
                           "screenshot prediction": "the user is on a youtube video of how to take the derivative of a function, likely not wasting time"
                        }
                        """)
    print(response)

if __name__ == "__main__":
    main()
