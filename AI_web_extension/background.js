var title = "";
function getPageTitle() {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      if (tabs && tabs[0]) {
        title = tabs[0].title;
      }
        title = "Empty tab";
    });
    return title;
  }
  
  function sendHttpPostRequest(url, data, callback) {
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(data)
    };
  
    fetch(url, options)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        callback(null, data);
      })
      .catch(error => {
        callback(error, null);
      });
  }
  
  // Example usage:
  // getPageTitle((error, title) => {
  //   if (error) {
  //     console.error('Error:', error);
  //     return;
  //   }
  //   console.log('Page title:', title);
  // });
  
  // Example usage:
  // const postData = { key: 'value' };
  // sendHttpPostRequest('https://example.com/api', postData, (error, response) => {
  //   if (error) {
  //     console.error('Error:', error);
  //     return;
  //   }
  //   console.log('Response:', response);
  // });
  

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'sendHttpPostRequest') {
    // Capture webpage title
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      const title = tabs[0].title; // Get the title of the current webpage

      // Capture the screenshot and include it in the postData object
      chrome.tabs.captureVisibleTab(null, { format: 'png' }, function(dataUrl) {
        const screenshotData = dataUrl; // Use the captured data URL as screenshot data
    
        // Create the postData object
        const postData = {
          title: title, // Include the current page title
          parsed_data: "some_data", // Placeholder for parsed data, replace with actual parsed data
          url: "https://youtube.com/8719879", // Placeholder for URL, replace with actual URL
          screenshot: screenshotData // Include the screenshot data
        };

        // Send HTTP POST request with postData
        sendHttpPostRequest('http://127.0.0.1:55570', postData, function(error, response) {
          if (error) {
            sendResponse({ error: error.message });
          } else {
            sendResponse({ success: true });
          }
        });
      });
    });

    return true; // Indicates that sendResponse will be called asynchronously
  }
});

  