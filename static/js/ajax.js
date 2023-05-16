// JavaScript code in ajax.js
$(document).ready(function() {
  // Handler for the button click event
  $('#submit-button').click(function() {
    // Retrieve form data
    var data = {
      recipient: $('#recipient').val(),
      name: $('#name').val(),
      staff_id: $('#staff_id').val(),
      position: $('#position').val(),
      department: $('#department').val(),
      leave_type: $('#leave_type').val(),
      annual_leave_entitled: $('#annual_leave_entitled').val(),
      leave_days_taken: $('#leave_days_taken').val(),
      leave_days_requested: $('#leave_days_requested').val(),
      remaining_leave_days: $('#remaining_leave_days').val(),
      proposed_leave_start_date: $('#proposed_leave_start_date').val(),
      proposed_leave_end_date: $('#proposed_leave_end_date').val(),
      handing_over_notes_done: $('#handing_over_notes_done').val(),
      resumption_date: $('#resumption_date').val(),
      contact_details: $('#contact_details').val(),
      is_approved: $('#is_approved').val(),
      is_declined: $('#is_declined').val(),
      remarks: $('#remarks').val(),
      handing_over_to: $('#handing_over_to').val()
    };

    // Send the AJAX request
    $.ajax({
      url: '/leave_request/',
      type: 'POST',
      data: data,
      success: function(response) {
        // Handle the successful response
        console.log(response);
      },
      error: function(xhr, errmsg, err) {
        // Handle any errors
        console.log(xhr.status + ': ' + xhr.responseText);
      }
    });
  });
});

//i will modify the below and use, copying the Retrieve Data from above

// JavaScript code in ajax.js
$(document).ready(function() {
  // Handler for the leave request form submission
  $('#leave-request-form').submit(function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Retrieve form data
    var formData = $(this).serialize();

    // Send the AJAX request
    $.ajax({
      url: '/leave-request/',
      type: 'POST',
      data: formData,
      success: function(response) {
        // Handle the successful response
        console.log(response);
      },
      error: function(xhr, errmsg, err) {
        // Handle any errors
        console.log(xhr.status + ': ' + xhr.responseText);
      }
    });
  });

  // Handler for the create memo form submission
  $('#create-memo-form').submit(function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Retrieve form data
    var formData = $(this).serialize();

    // Send the AJAX request
    $.ajax({
      url: '/create-memo/',
      type: 'POST',
      data: formData,
      success: function(response) {
        // Handle the successful response
        console.log(response);
      },
      error: function(xhr, errmsg, err) {
        // Handle any errors
        console.log(xhr.status + ': ' + xhr.responseText);
      }
    });
  });

  // Add more AJAX request handlers for other views if needed
});
