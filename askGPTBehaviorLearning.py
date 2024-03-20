import google.generativeai as genai


def identify_bad_habits(history):

    genai.configure(api_key="***APIKEY***")

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat()

    response = chat.send_message("""
                                 Here is a log of responses from an AI that determines if a webpage is something a student, who should be studying, should be looking at or not by the content,\n
                                 The Content AI takes in information and determines a "content prediction", this content prediction will return 'yes' if it determines the webpage is time wasting or not.\n
                                 Additionally, the Content AI also determines if a webpage is timewasting in "screenshot prediction" by taking a screenshot and determining if the web extension looks productive, if the response is 'yes' then it is considered timewasting.\n
                                 Finally, the "title" of the webpage corresponding to each AI prediction is given, to give you an idea of what web pages they tend to get distracted on.
                                 Based on this given log formatted in json with "context prediction", "screenshot prediction", and "title", please determine if the student is being more productive than not and identify what webpages the student tends to get distracted on.  
                                 \n
                                 here is the log:\n
                                 """+history)

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
