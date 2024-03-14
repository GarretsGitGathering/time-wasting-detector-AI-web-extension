# Chrome Extension with AI Time-Wasting Detection

A chrome extension that interacts with backend AI hosting servers to determine if a user is wasting their time on a browser. Currently, only the content determining AI is complete and it utilizes AI for determining the productivity rating of the webpage. It does this by taking inputs from html values of the webpage such as the title and some parsed data as well as taking a screenshot and processing the image.

Additionally, the extension now stores AI data about what pages the user interacts with on the browser side, and the user can now submit their history to a behaviour learning AI that will analyze how they interact with the web and provide helpful advice for how they can focus better.

Currently the project is still in development stages, currently it uses:

 - Chrome Extension Development
 - langchain API libraries
 - Gemini API libraries

## Here are some Proof of Concept images

![Example Image](/imgs/Full_Functionality.png)
![Example Image](/imgs/screenshot_example.png)
![Example Image](/imgs/server_response.png)
![Example Image](/imgs/request_example.png)
