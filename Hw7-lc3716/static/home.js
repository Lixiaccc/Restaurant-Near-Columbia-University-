current_id = 10

$(document).ready(function() {
  // Fetch and display restaurant data
  $.getJSON('/restaurants', function(data) {
      data.restaurants.sort((a, b) => parseFloat(b.Rating) - parseFloat(a.Rating));
      const topThreeRestaurants = data.restaurants.slice(0, 3);
      const row = $('<div>').addClass('row');
      topThreeRestaurants.forEach(restaurant => {
          const col = $('<div>').addClass('col bordered-col');
          const content = $(`
          <a href="/view/${restaurant.id}" class="stretched-link custom-link mb-2">
          <div class="restaurant_name">${restaurant.Restaurant}
              <div class="badge badge-warning badge-pill">${restaurant.Rating}</div>
          </div>
          <div class="restaurant_descrip">
              ${restaurant.Description}
          </div>
          <img class="restaurant_img" src="${restaurant.Restaurant_image}" alt="Image of the Restaurant or Food">
      </a>
          `);
          col.append(content);
          row.append(col);
      });
      $('#restaurant-list').append(row);
  }).fail(function(jqXHR, textStatus, errorThrown) {
      console.error('Error fetching data:', errorThrown);
  });


  $('#search-input').on('submit', function(event) {
    if (!validateSearchForm()) {
        event.preventDefault(); // Prevent the form from submitting if validation fails
    }
});

  $('#Restaurant').on('keypress', function(event) {
  $('.created, .created1, .check').remove();
  });

  // Handle restaurant form submission
  $('#submitRestaurant').on('click', function(event) {
    $('.warning').remove();
    $('.created').remove();
      event.preventDefault(); // Prevent the form from submitting in the traditional way
      let new_res = {
          "Restaurant": $('#Restaurant').val(),
          "Description": $('#Description').val(),
          "Restaurant_image": $('#Restaurant_image').val(),
          "Food_image1": $('#Food_image1').val(),
          "Food_image2": $('#Food_image2').val(),
          "Summary": $('#Summary').val(),
          "Address": $('#Address').val(),
          "price_range": $('#price_range').val(),
          "Rating":parseFloat($('#Rating').val()),
          "Menu": $('#Menu').val(),
          "Hours": $('#Hours').val(),
          "Distance_from_campus": $('#Distance_from_campus').val(),
          "Contact": $('#Contact').val(),
          "Offerings": $('#Offerings').val(),
      };

      let isValid = true;
      let rating = new_res.Rating;
      function isValidRating(input) {
        const number = parseFloat(input);
        // Check if the input is a number, within the valid range, and matches the input when converted back to a string
        return !isNaN(number) && number >= 0 && number <= 5 && number.toString() === input.trim();
      }
      
      // Use the isValidRating function to validate the 'Rating' field
      if (!isValidRating($('#Rating').val())) {
        $("<span class='warning'>Rating must be a number between 0 and 5 and cannot contain letters or extra characters.</span>").insertAfter("#Rating");
        isValid = false;
      }

      function DollarSigns(str) {
        // This regex matches strings that consist solely of one or more $ characters.
        return /^[$]+$/.test(str);
      }
      // Corrected usage for checking price_range
      if (!DollarSigns(new_res['price_range'])) {
        $(`<span class='warning'>This field should only include "$" symbols. </span>`).insertAfter(`#price_range`);
        isValid = false;
      }

      function isValidUrl(url) {
        const pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
            '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
            '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
            '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
            '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
            '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
        return !!pattern.test(url);
    }

      // Check if any required field is empty
      for (let key in new_res) {
          if (new_res[key] === '') { // Skip Menu for URL validation
              $(`<div> <span class='warning'>This field is required. </span></div>`).insertAfter(`#${key}`);
              isValid = false;
          }
      }


      // Validate URLs for images
      ['Restaurant_image', 'Food_image1', 'Food_image2'].forEach(field => {
          if (new_res[field] && !isValidUrl(new_res[field])) {
              $(`<span class='warning'>Please enter a valid image URL for ${field}.</span>`).insertAfter(`#${field}`);
              isValid = false;
          }
      });
      
      if (new_res['Menu'] && !isValidUrl(new_res['Menu'])) {
        $(`<span class='warning'>Please enter a valid URL for the Menu.</span>`).insertAfter(`#Menu`);
        isValid = false;
    }
    if (new_res.Description.split(/\s+/).length > 4) {
      $(`<span class='warning'>Description must be 4 words or less.</span>`).insertAfter("#Description");
      isValid = false;
  }

      // Only proceed if all validations pass
      if (isValid) {
          save_res({
              ...new_res,
              Rating: rating, // Ensure rating is correctly parsed as a float
          });
          current_id += 1
          // Clear form fields after saving
          $('input[type=text], input[type=number]').val('');
          $('#Offerings').val('');
          $('#Summary').val('');
          $(`<div class="success">
          <div class="content">
          <h3 class="check">✓</h3>
            <h3 class="created created1">New item successfully created!</h3>
          </div>
          <div>
            <a class="created" href="/view/${current_id}" target="_self">see it here</a>
          </div>
        </div>
          `).insertAfter("h2");
          $('#Restaurant').focus()
      }
  });


$('#save_edit').click(function(e) {
   // Prevent form submission to validate on client-side first
  // Clear previous warnings
  let isValid = true;
  $('.warning').remove();
  let new_res = {
    "Restaurant": $('#Restaurant').val(),
    "Description": $('#Description').val(),
    "Restaurant_image": $('#Restaurant_image').val(),
    "Food_image1": $('#Food_image1').val(),
    "Food_image2": $('#Food_image2').val(),
    "Summary": $('#Summary').val(),
    "Address": $('#Address').val(),
    "price_range": $('#price_range').val(),
    "Rating":$('#Rating').val(),
    "Menu": $('#Menu').val(),
    "Hours": $('#Hours').val(),
    "Distance_from_campus": $('#Distance_from_campus').val(),
    "Contact": $('#Contact').val(),
    "Offerings": $('#Offerings').val(),
};


function isValidRating(input) {
  const number = paseFloat(input);
  // Check if the input is a number, within the valid range, and matches the input when converted back to a string
  return !isNaN(number) && number >= 0 && number <= 5 && number.toString() === input.trim();
}

// Use the isValidRating function to validate the 'Rating' field
if (!isValidRating($('#Rating').val())) {
  $("<span class='warning'>Rating must be a number between 0 and 5 and cannot contain letters or extra characters.</span>").insertAfter("#Rating");
  isValid = false;
}


function DollarSigns(str) {
  // This regex matches strings that consist solely of one or more $ characters.
  return /^[$]+$/.test(str);
}

// Corrected usage for checking price_range
if (!DollarSigns(new_res['price_range'])) {
  $(`<span class='warning'>This field should only include "$" symbols. </span>`).insertAfter(`#price_range`);
  isValid = false;
}

function isValidUrl(url) {
  const pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
      '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
      '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
      '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
      '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
      '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  return !!pattern.test(url);
}

// Check if any required field is empty
for (let key in new_res) {
    if (new_res[key] === '') { // Skip Menu for URL validation
        $(`<div> <span class='warning'>This field is required. </span></div>`).insertAfter(`#${key}`);
        isValid = false;
    }
}


// Validate URLs for images
['Restaurant_image', 'Food_image1', 'Food_image2'].forEach(field => {
    if (new_res[field] && ! isValidUrl(new_res[field])) {
        $(`<span class='warning'>Please enter a valid image URL for ${field}.</span>`).insertAfter(`#${field}`);
        isValid = false;
    }
});

if (new_res['Menu'] && !isValidUrl(new_res['Menu'])) {
  $(`<span class='warning'>Please enter a valid URL for the Menu.</span>`).insertAfter(`#Menu`);
  isValid = false;
}
if (new_res.Description.split(/\s+/).length > 4) {
$(`<span class='warning'>Description must be 4 words or less.</span>`).insertAfter("#Description");
isValid = false;
}

  if (!isValid) {
    e.preventDefault(); // This will now allow the form to be submitted.
  }
});

$(function() {
  var dialog = $("#dialog").dialog({
      autoOpen: false,
      width: 600, // Adjust the width as needed
      height: "auto", // Adjust the height or set it to "auto" for automatic height adjustment
      title: "Confirm Discard Changes", // Ensure title is visible by setting it here if it's not showing
      open: function() {
          var closeBtn = $('.ui-dialog-titlebar-close');
          closeBtn.blur();
      }
  });

  $("#open-dialog").on("click", function() {
      dialog.dialog("open");
  });

  $("#yes-button").on("click", function() {
      window.location = $(this).data("url");
  });

  $("#no-button").on("click", function() {
      dialog.dialog("close");
  });
});

$('#descriptionText').click(function() {
  console.log("Description clicked"); // Debug line
  var description = $(this).data('description');
  $('#search-input').val(description);
  $('form').submit();
});
});

function save_res(new_res) {
  $.ajax({
      url: '/add',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(new_res),
      success: function(response) {
          console.log('Restaurant added:', response);
          // Assuming 'restaurants' is a global variable or otherwise handled
          // Update the UI or notify the user as appropriate
      },
      error: function(error) {
          console.error('Error saving restaurant:', error);
      }
  });
}

function validateSearchForm() {
  var searchInput = document.getElementById('search-input');
  if (!searchInput.value.trim()) {
      searchInput.value = '';
      searchInput.focus();
      return false;
  }
  return true;
}


