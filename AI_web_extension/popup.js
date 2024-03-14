document.addEventListener('DOMContentLoaded', function() {
  // Add event listener to the "Send HTTP POST Request" button
  document.getElementById('sendRequestButton').addEventListener('click', function() {
    // Data to be sent in the HTTP POST request
    const postData = { key: 'value' };
    
    // Send message to background script to send HTTP POST request
    chrome.runtime.sendMessage({ action: 'sendContentAIData', data: postData }, function(response) {
      if (response && response.success) {
        alert('HTTP POST Request Successful');
      } else {
        alert('Error: HTTP POST Request Failed');
      }
    });
  });

  document.getElementById('getBehaviour').addEventListener('click', function() {
    // Data to be sent in the HTTP POST request
    const postData = { key: 'value' };
    // Send message to background script to send HTTP POST request
    chrome.runtime.sendMessage({ action: 'sendStoredData', data: postData }, function(response) {
      if (response && response.success) {
        alert('HTTP POST Request Successful');
      } else {
        alert('Error: HTTP POST Request Failed');
      }
    });
  });
  // Listen for messages from the background script
  chrome.runtime.onMessage.addListener(function(message) {
    // Check if the message is to update the status
    if (message.action === 'updateStatus') {
      const messageString = message.message["context prediction"];
      // Update the status tag
      const statusElement = document.getElementById('status');
      statusElement.textContent = messageString;
    }
  });
});
