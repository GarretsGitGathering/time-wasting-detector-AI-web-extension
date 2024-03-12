document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to the "Get Page Title" button
    document.getElementById('getTitleButton').addEventListener('click', function() {
      // Send message to background script to get page title
      chrome.runtime.sendMessage({ action: 'getPageTitle' }, function(response) {
        if (response && response.title) {
          alert('Page Title: ' + response.title);
        } else {
          alert('Error: Unable to get page title.');
        }
      });
    });
  
    // Add event listener to the "Send HTTP POST Request" button
    document.getElementById('sendRequestButton').addEventListener('click', function() {
      // Data to be sent in the HTTP POST request
      const postData = { key: 'value' };
      
      // Send message to background script to send HTTP POST request
      chrome.runtime.sendMessage({ action: 'sendHttpPostRequest', data: postData }, function(response) {
        if (response && response.success) {
          alert('HTTP POST Request Successful');
        } else {
          alert('Error: HTTP POST Request Failed');
        }
      });
    });
});
  