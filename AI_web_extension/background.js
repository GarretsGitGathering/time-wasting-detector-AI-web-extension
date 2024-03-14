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

  // Function to update the status tag
  function updateStatus(message) {
    const statusElement = document.getElementById('status');
    statusElement.textContent = message;
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
  if (request.action === 'sendContentAIData') {
    // Capture webpage title
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      const title = tabs[0].title; // Get the title of the current webpage
      const url = tabs[0].url      // Get the url of the current webpage

      // Capture the screenshot and include it in the postData object
      chrome.tabs.captureVisibleTab(null, { format: 'png' }, function(dataUrl) {
        const screenshotData = dataUrl; // Use the captured data URL as screenshot data
    
        // Create the postData object
        const postData = {
          title: title, // Include the current page title
          parsed_data: "some_data", // Placeholder for parsed data, replace with actual parsed data
          url: url, // Placeholder for URL, replace with actual URL
          screenshot: screenshotData // Include the screenshot data
        };

        // Send HTTP POST request with postData
        sendHttpPostRequest('http://127.0.0.1:55570', postData, function(error, response) {
          if (error) {
            sendResponse({ error: error.message });
          } else {
              // Retrieve data
              chrome.storage.local.get('stored_data', function(result) {
                const storedData_json = result['stored_data'];

                const storedData = JSON.stringify(storedData_json);
                const response_string = JSON.stringify(response);

                const newData = storedData+response_string;
                const parsedNewData = newData.replace(/\\/g, '');

                //storeData("stored_data", response);
                chrome.storage.local.set({ 'stored_data': parsedNewData}, function() {
                  console.log('Data stored successfully');
              });
            });
          }
        });
      });
    });

    return true; // Indicates that sendResponse will be called asynchronously
  }

  if (request.action === 'sendStoredData') {

    // Retrieve data
    chrome.storage.local.get('stored_data', function(result) {
      const storedData = result['stored_data'];
    

    sendHttpPostRequest('http://127.0.0.1:55575', storedData, function(error, response) {
      if (error) {
        sendResponse({ error: error.message });
      } else {
        //sendResponse({ success: true });
        //const response_json = JSON.stringify(response)
        chrome.runtime.sendMessage({ action: 'updateStatus', message: response });
      }
    });
  });
    return true;
  }
});