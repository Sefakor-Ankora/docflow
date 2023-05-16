// Execute the code when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Get the form element
    var form = document.querySelector("#memo-form");
  
    // Add event listener for form submission
    form.addEventListener("submit", function(event) {
      // Prevent the default form submission
      event.preventDefault();
  
      // Perform any necessary form validation
      // ...
  
      // Collect form data
      var referenceNumber = document.querySelector("#reference_number").value;
      var sender = document.querySelector("#sender").value;
      var recipient = document.querySelector("#recipient").value;
      var project = document.querySelector("#project").value;
      var budgetLine = document.querySelector("#budget_line").value;
  
      // Create an object with the form data
      var formData = {
        reference_number: referenceNumber,
        sender: sender,
        recipient: recipient,
        project: project,
        budget_line: budgetLine
      };
  
      // Perform an AJAX request to submit the form data
      // Replace the URL with your actual form submission endpoint
      var url = "/docflow/create_memo/";
      var xhr = new XMLHttpRequest();
      xhr.open("POST", url, true);
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          // Handle the response from the server
          // ...
        }
      };
      xhr.send(JSON.stringify(formData));
    });
  });
  