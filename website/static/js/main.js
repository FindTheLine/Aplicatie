// await post data
async function postData(url = '', data, token) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': token
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response
}

// Set-Cookie: key=value; SameSite=Strict;
function deleteInterval() {
  return window.location.replace(keepLastDates(window.location.href, count=0));
}

$(document).ready(function () {
  if (hasDates(window.location.href))
  {
    return window.location.replace(keepLastDates(window.location.href));
  }
  else if (hasDates(window.location.href, count=2))
  {
    $(".delete-interval-btn").css("display","block");
  }
});

// sleep func

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// HIDE TOASTS AFTER DELAY
function hideItem(selector) {
  if (document.querySelector(selector) != null) {
    setTimeout(function () {
      $(selector).fadeOut(500);
    }, 5000)
  }
}

setTimeout(function () {
    $(".base-alerts .alert").fadeOut(500)
}, 5000);


// modal padding right fix

// MODAL
// fix padding right added to body
$(document).ready(function () {
  $('body').css('padding-right', '0');
});

// SEARCH BAR RESULTS
$(document).ready(function () {
  $("#nav-input").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    if (value.length > 1) {
      $("#search-drop").css('display', 'block')
      $("#search-drop a").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    }
    else {
      $("#search-drop").css('display', 'none')
    }
  });
});

// DROPDOWN SEARCH
$(document).ready(function () {
  $("#search-icon").click(function () {
    $(".search-wrapper").slideToggle(400)
  });
});

// HAMBURGER MENU & OVERLAY
$(document).ready(function () {
  $(".navbar-toggler").click(function () {
    $(this).toggleClass("menu-opened");
    if ($(".hamburger-menu").hasClass("menu-opened")) {
      $('.navbar-collapse').first().stop(true, true).slideDown();
      $('.overlay').addClass('d-block');
      $('.overlay').removeClass('d-none');
    }
    else {
      $('.navbar-collapse').first().stop(true, true).slideUp();
      $('.overlay').removeClass('d-block');
      $('.overlay').addClass('d-none');
    }
  });
});

$(document).ready(function () {
  $('.overlay').click(function (event) {
    if ($(".hamburger-menu").hasClass("menu-opened")) {
      $('.navbar-toggler').click()
    }
    else {
      $('.overlay').removeClass('d-block');
      $('.overlay').addClass('d-none');
    }
  });
});

$(document).ready(function () {
  $('.account').on('hide.bs.dropdown', function () {
    $(this).find('#toggle-bg').first().stop(true, true).fadeOut(0, function () {
      $('.account-icon').addClass("text-white");
      $('.account-icon').removeClass("text-green");
    })
  });
});

//SCROLL LOADING BAR
function updateProgress(num1, num2) {
  var percent = Math.ceil(num1 / num2 * 100) + '%';
  $('#progress').css('width', percent);
}

window.addEventListener('scroll', function () {
  var top = window.scrollY;
  var height = document.body.getBoundingClientRect().height - window.innerHeight;
  updateProgress(top, height);
});

$(document).ready(function () {
  $(window).scroll(function () {
    if ($(this).scrollTop() < 100) {
      $(".progressContainer:visible").fadeOut();
      $(".progressContainer:visible").addClass("d-none");
    }
    else {
      $(".progressContainer:hidden").fadeIn();
      $(".progressContainer:hidden").removeClass("d-none");
    }
  });
});

// PIE CHART AND LINEAR CHART CONFIG AND INITIALISATION

// get averages
 
// Define an array of chart elements

function adjustListPositions(firstList, secondList) {
  var targetIndex = firstList.length - secondList.length;
  var nullValues = new Array(targetIndex).fill(null);
  if (targetIndex >= 0) {
    var nullValues = new Array(targetIndex).fill(null);
    return nullValues.concat(secondList);
  } else {
    return secondList.slice(targetIndex);
  }
}

function movingAverage(list, step = 3) {
  console.log("list: " + list);
  const length = list.length;
  let results = [];

  for (let index = step; index <= length; index++) {
    const stepSlice = list.slice(index - step, index);
    const sum = stepSlice.reduce((a, b) => a + b, 0);

    results.push(sum / step);
  }
  
  console.log("RESULT: " + results);
  return results;
}

function dateIntervalMa(list, step=3) {
  var groupsDates = [];
  for (var i = 0; i < list.length; i += step) {
    if (i === list.length-1 && list[i] == undefined)
      var firstAndLast = list[i] + " - " + "prezent"
    else 
      var firstAndLast = list[i] + " - " + list[i+step]
    groupsDates.push(firstAndLast);
  }
  return groupsDates;
}

const chartElements = [
  { selector: '.allMovingMeanChart', type: 'line', label: 'Medii Mobile / Toate Proiectele', ma:true},
  { selector: '.allPieMeanChart', type: 'polarArea', label: 'Medie Criterii / Toate Proiectele', ma:false},
  { selector: '.allPieMedianChart', type: 'bar', label: 'Mediana Criterii / Toate Proiectele', ma:false},
  { selector: '.allPieModeChart', type: 'bar', label: 'Mod Criterii / Toate Proiectele', ma:false},
  { selector: '.projectMovingMeanChart', type: 'line', label: 'Medii Mobile / Proiectul Curent', ma:true},
  { selector: '.projectLinearChart', type: 'line', label: 'Evaluari / Proiectul Curent', ma:false},
  { selector: '.projectPieMeanChart', type: 'polarArea', label: 'Medie Criterii / Proiectul Curent', ma:false},
  { selector: '.projectPieMedianChart', type: 'bar', label: 'Mediana Criterii / Proiectul Curent', ma:false},
  { selector: '.projectPieModeChart', type: 'bar', label: 'Mod Criterii / Proiectul Curent', ma:false}
];

function minValue(values)
{
  let val = Math.min(values);
  return val;
}

function minValue(values)
{
  let val = Math.max(values);
  return val;
}

// Iterate over the chart elements
chartElements.forEach(element => {
  const chartElement = document.querySelector(element.selector);
  if (chartElement) {
    if (element.type === 'line' || element.type === 'bar') {
      
      // Convert data to array for separate assignment on chart
      var avg = (chartElement.dataset.avg).split(',').map(x => parseFloat(x));
      var crit1 = (chartElement.dataset.crit1).split(',').map(x => parseFloat(x));
      var crit2 = (chartElement.dataset.crit2).split(',').map(x => parseFloat(x));
      var crit3 = (chartElement.dataset.crit3).split(',').map(x => parseFloat(x));
      var crit4 = (chartElement.dataset.crit4).split(',').map(x => parseFloat(x));
      var labels = (chartElement.dataset.labels).split(',');

      console.log(element.selector)

      dataset = [{
        label: 'Media',
        backgroundColor: '#212121',
        borderColor: '#212121',
        fill: false,
        data: avg,
      },
      {
        label: 'C1',
        backgroundColor: '#183ba6',
        borderColor: '#183ba6',
        fill: false,
        data: crit1,
      },
      {
        label: 'C2',
        backgroundColor: '#FFC107',
        borderColor: '#FFC107',
        fill: false,
        data: crit2,
      },
      {
        label: 'C3',
        backgroundColor: '#BB86FC',
        borderColor: '#BB86FC',
        fill: false,
        data: crit3,
      },
      {
        label: 'C4',
        backgroundColor: '#4CAF50',
        borderColor: '#4CAF50',
        fill: false,
        data: crit4,
      }
      ];

      var max = Math.max([...avg,...crit1,...crit2,...crit3,...crit4])
      var min = Math.min([...avg,...crit1,...crit2,...crit3,...crit4])

      if (element.selector.includes("Moving")) 
      {
        const ma3 = adjustListPositions(avg,movingAverage(avg, step=3));
        const ma6 = adjustListPositions(avg,movingAverage(avg, step=6));
        const ma12 = adjustListPositions(avg,movingAverage(avg, step=12));

        max = Math.max([...avg,...ma3,...ma6,...ma12]) 
        min = Math.min([...avg,...ma3,...ma6,...ma12]) 

        dataset = [{
          label: 'Media / Evaluare',
          backgroundColor: '#212121',
          borderColor: '#212121',
          fill: false,
          data: avg,
        },
        {
          label: 'Medie Mobila (3)',
          backgroundColor: 'rgba(255, 170, 0, 0.5)',
          borderColor: 'rgba(255, 170, 0, 0.5)',
          fill: false,
          data: ma3,
        },
        {
          label: 'Medie Mobila (6)',
          backgroundColor: 'rgba(255, 95, 22, 0.75)',
          borderColor: 'rgba(255, 95, 22, 0.75)',
          fill: false,
          data: ma6,
        },
        {
          label: 'Medie Mobila (12)',
          backgroundColor: 'rgba(255, 20, 20, 1)',
          borderColor: 'rgba(255, 20, 20, 1)',
          fill: false,
          data: ma12,
        }
        ];
      }

      if (element.selector.includes("Median") || element.selector.includes("Mode"))
      {
        labels = " ";
      }

      const chartData = {
        labels: labels,
        datasets: dataset
      };

      // Chart configuration
      const chartConfig = {
        type: element.type,
        data: chartData,
        options: {
          plugins: {
            title: {
              display: true,
              text: element.label,
              font: {
                size: 16,
                family: 'Montserrat',
              }
            }
          },
          interaction: {
            mode: 'index'
          },
          scales: {
            x: {
              title: {
                display: true,
                text: element.selector.includes("Median") || element.selector.includes("Mode") ? 'Criterii' : 'Data'  
              },
              stacked: (element.type === "bar" && avg.length > 1) ?  true : false 
            },
            y: {
              title: {
                display: true,
                align: 'center',
                text: 'Media'
              },
              stacked: (element.type === "bar" && avg.length > 1) ?  true : false,
              suggestedMax: max,
              suggestedMin: min
            },
          },
        }
      }
      new Chart(chartElement, chartConfig);
    }
    else if (element.type === 'pie' || element.type === 'polarArea') {
      var critAverages = (chartElement.dataset.crit).split(',').map(x => parseFloat(x));
      // data initialisation
      const dataPie = {
        labels: ['C1', 'C2', 'C3', 'C4'],
        datasets: [{
          label: '',
          backgroundColor: ["#183ba6", "#FFC107", "#BB86FC", "#4CAF50"],
          data: critAverages,
        }]
      };

      var scales = null
      if (element.type === 'polarArea' )
      {
        scales = {
          r: {
            beginAtZero: element.type === 'polarArea' ? false : null 
          }
        }   
      }

      // pie chart configuration
      const configPie = {
        type: element.type,
        data: dataPie,
        options: {
          plugins: {
            title: {
              display: true,
              text: element.label,
              font: {
                size: 16,
                family: 'Montserrat',
              }
            }
          },
          scales: scales
        }
      };

      const pieChart = new Chart(
        chartElement,
        configPie
      );
    }
  }
});

function updateCheckmarkContent() {
  const radioInputs = document.querySelectorAll('input[type="radio"][data-check-name]');

  radioInputs.forEach(function (input) {
    input.addEventListener('change', function () {
      const value = this.value;
      const checkmark = this.parentNode.querySelector('.eval-check-container .checkmark');
      $(checkmark).attr('eval-check-content',value);
    });
  });
}

function changeNavbarHeight() {
  var navbar = document.querySelector('.navbar-height');
  var screenWidth = window.innerWidth;

  if (screenWidth < 768) {
    navbar.style.height = '64px';
  } else {
    navbar.style.height = '72px';
  }
}

window.addEventListener('resize', changeNavbarHeight);

changeNavbarHeight();



updateCheckmarkContent();

jQuery(document).ready(function ($) {
  $(".clickable-row").click(function () {
    window.location = $(this).data("href");
  });
});


$(document).ready(function () {
  var dateRegex = /\d{4}-\d{2}-\d{2}/g;
  var dates = window.location.href.match(dateRegex);
  
  if (dates && dates.length == 2) {
    var firstDate = dates[0];
    var secondDate = dates[1];

    var firstPref = document.querySelector('.firstDatePref');
    firstPref.textContent = "din ";

    var firstElem = document.querySelector('.firstDate');
    firstElem.textContent = firstDate;
  
    var secondPref = document.querySelector('.secondDatePref');
    secondPref.textContent = " pana in ";

    var secondElem = document.querySelector('.secondDate');
    secondElem.textContent = secondDate;
    
    // Display the paragraph container
    var intervalContainer = document.querySelector('.intervalContainer');
    intervalContainer.style.display = 'block';
  };
});

function keepLastDates(link, count=2) {
  var parts = link.split('/');
  var datesCount = 0;

  for (var i = parts.length - 1; i >= 0; i--) {
    if (/\d{4}-\d{2}-\d{2}/.test(parts[i])) {
      datesCount++;
      if (datesCount > count) {
        parts.splice(i, 1); // Remove the date segment if there are more than two dates
      }
    }
  }

  return parts.join('/');
}


function hasDates(link, count=4) {
  var parts = link.split('/');
  var dateCount = 0;

  for (var i = 0; i < parts.length; i++) {
    if (/\d{4}-\d{2}-\d{2}/.test(parts[i])) {
      dateCount++;
    }
  }

  return dateCount === count;
}

// CHAT WINDOW FROM CHAT PAGE

$(document).on('click', '.panel-heading span.icon_minim', function (e) {
  var $this = $(this);
  if (!$this.hasClass('panel-collapsed')) {
    $this.parents('.panel').find('.panel-body').slideUp();
    $this.addClass('panel-collapsed');
    $this.removeClass('glyphicon-minus').addClass('glyphicon-plus');
  } else {
    $this.parents('.panel').find('.panel-body').slideDown();
    $this.removeClass('panel-collapsed');
    $this.removeClass('glyphicon-plus').addClass('glyphicon-minus');
  }
});

$(document).on('focus', '.panel-footer input.chat_input', function (e) {
  var $this = $(this);
  if ($('#minim_chat_window').hasClass('panel-collapsed')) {
    $this.parents('.panel').find('.panel-body').slideDown();
    $('#minim_chat_window').removeClass('panel-collapsed');
    $('#minim_chat_window').removeClass('glyphicon-plus').addClass('glyphicon-minus');
  }
});

$(document).on('click', '#new_chat', function (e) {
  var size = $(".chat-window:last-child").css("margin-left");
  size_total = parseInt(size) + 400;
  alert(size_total);
  var clone = $("#chat_window_1").clone().appendTo(".container");
  clone.css("margin-left", size_total);
});

$(document).on('click', '.icon_close', function (e) {
  //$(this).parent().parent().parent().parent().remove();
  $("#chat_window_1").remove();
});

// FORM PROCESSING

// serialize object
function serializeObject(obj, eval = false) {
  serialized = {}
  for (var [key, value] of obj) {
    if (key != "csrf_token") {
      serialized[key] = value.toLowerCase();
    }
    else
      continue
  }
  return serialized
}

// FORM TOAST TEMPLATES
const notification = ({ title, time, message }) => `
  <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="toast-header">
      <small class="text-muted">${time}</small>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
      ${message}
    </div>
  </div>
`;

// SET STATUS FUNCTION
function setStatusFor(formId, error, field, message = '') {
  var small = $(field).next('.js-form-message'); //next for imidiate sibling
  // verify if field is jquery obj, if so convert to DOM element  
  // error actions
  
  if (field instanceof $ && formId === "eval-form") {
    field = field[0]
  }
  if (error === true) {
    //remove success classes 
    if (field.classList.contains('border-success') && small.hasClass('text-success')) {
      field.classList.remove('border-success');
      try {
        small.classList.remove('text-success');
      }
      catch (error) {
        small.removeClass('text-success');
      }
    }
    //add error classes
    field.classList.add('border-danger');
    small.addClass('text-danger');
    if (message !== '') {
      small.text(message)
    }
    else {
      small.text('Campul este invalid.')
    }
  }
  // valid actions
  else {
    //remove error classes
    if (field.classList.contains('border-danger') && small.hasClass('text-danger')) {
      field.classList.remove('border-danger');
      try {
        small.classList.remove('text-danger');
      }
      catch (error) {
        small.removeClass('text-danger');
      }
    }
    //add success classes
    field.classList.add('border-success');
    small.addClass('text-success')
    small.text(message)
  }
}

// SET STATUS FOR ARRAY OF FIELDS
function fieldsListStatus(formId, validFields = [], errorFields = [], message = '', origin) {
  try {
    //for array values
    if (origin == "cl") {
      //valid
      for (const el of validFields) {
        
        var message = "Campul este valid.";
        setStatusFor(formId, false, el, message); //removed get el.data attribute for cl side
      };
      //errors
      if (errorFields !== []) {
        for (const el of errorFields) {
          var message = "Campul este invalid.";
          //call error status for error fields if they exist, set second arg to true (arg. error)
          setStatusFor(formId, true, el, message);
        };
      }
    }
    //for object values
    else if (origin == "sr") {
      //valid      
      var form = document.getElementById(formId)
      for (const key in validFields)//fields are valid already
      {
        // check inputs require parent row for displaying status borders
        if (formId === "eval-form" && key.startsWith('eval-check')) {
          
          var element = form.querySelector(`input:checked[name=${key}]`);
          element = $(element).parents('.row')
        }
        // if inputs are not from eval-form and aren't checks then select the inputs directly
        else
          var element = document.getElementById(formId + '-' + key);
        // if elements are null try to select them by name
        if (element === null) {          
          element = form.querySelector(`input:checked[name=${key}]`);
          if (element === null) {                        
            element = form.querySelector(`[name=${key}]`);
          }
          if (formId.includes('comment-form')) {            
            if (key == "title") {
              var element = form.querySelector('input[type="text"]')              
            }
            else if (key == "text") {
              var element = form.querySelector('textarea')              
            }            
          }
        }        
        setStatusFor(formId, false, element, "Campul este valid");
      }
      //errors
      if (Object.keys(errorFields).length != 0) {        
        let keys = Object.keys(errorFields)
        
        for (var i = 0; i < keys.length; i++) {
          // exception for eval form, rest of the forms get their id by assignment of form id plus element identifier
          if (formId === "eval-form" && keys[i].startsWith('eval-check')) {
            var form = document.getElementById(formId)
            var element = form.querySelector(`input[name=${keys[i]}]`);
            element = $(element).parents('.row')
          }
          else {
            var element = document.getElementById(formId + '-' + keys[i]);            
            if (element == null) {        
              var element = form.querySelector(`[name=${keys[i]}]`)              
            }
          }
          setStatusFor(formId, true, element, message);
        }
      }
    }
  }
  catch (error) {
    console.error(error)
  }
}

function collectFormData(formId) {
  var formData = new FormData(document.getElementById(formId));
  return formData
}

function checkFormFieldEmpty(formData) {
  for (var [key, value] of formData.entries()) {
    if (key !== 'csrf_token') {
      if (value == '' && value == []) {
        return true;
      }
    }
  }
  return false;
}

//form message template
const formMessage = ({message, category}) => `
  <div class="alert alert-${category} rounded-2 py-1 position-fixed" role="alert">                    
    <p class="my-1">${message}</p>
  </div>
`;

function showFormMessage(message, category) {
  
  $('.base-alerts').html(formMessage({message, category}));
}


//function for sending form 
function sendForm(form, formId, url, formData) {
  // verify for not login form
  if (formId === "login-form" || formId === "nav-form" || formId === "profile-form" || formId === "request-form" || formId === "reset-form" || formId === "mark_notifications") {
    return;
  }

  var form = document.getElementById(formId);
  var allFields = form.querySelectorAll('[data-user-input]');
  //check if any form field is empty 
  
  if (checkFormFieldEmpty(formData) == false && form[0].checkValidity()) {
    // serialize json data
    var serialized = serializeObject(formData);
    // if form is not empty and valid call fetch 
    
    var token = form.getElementsByTagName("input")[0];    
    var token = form.getElementsByTagName("input")[0].value;
  
    console.log(serialized)

    postData(url, serialized, token).then((response) => {
      if (response.status != 200 && response.status != 404) {
        showFormMessage(`Serverul nu a intors un raspuns valid, verifica daca schimbarea a fost facuta`, 'danger'); //show message of status to the user
        hideItem('.alert');
      }
      // receive data as json for accessing attributes
      return response.json()
    })
      .then((data) => {        
        fieldsListStatus(formId, data.data, data.error_fields, data.message, origin = 'sr')
        try {
          // if (formId == "eval-form" ) {            
            showFormMessage(data.message, data.category); //show message of status to the user
            hideItem('.alert');
          // }
          if (formId === "employee-interval-form"  || formId === "team-interval-form") {            
            if (data.url !== ''){              
              var fullUrl = window.location.href;
              var redirectUrl = fullUrl + data.url

              window.location.replace(keepLastDates(redirectUrl));
            }
          }
        }
        catch (error) {
          showFormMessage(error, 'danger'); //show message of status to the user
          hideItem('.alert');
        }
      });
  }
  else {    
    var invalidFields = form.querySelectorAll(':invalid');
    // if invalid fields are existent but not undefined
    if (typeof invalidFields !== 'undefined' && invalidFields.length === allFields.length) {
      if (formId == "eval-form") {
        showFormMessage('Formularul este gol', 'danger'); //show form message
        hideItem('.alert'); //timeout for alerts
      }
    }
    else if (typeof invalidFields !== 'undefined' && invalidFields.length > 0) {
      if (formId == "eval-form") {
        showFormMessage('Formularul este incomplet', 'danger'); //show form message
        hideItem('.alert'); //timeout for alerts
      }
    }
    // else {
    // }
    var validFields = $.grep(allFields, function (element) {
      return $.inArray(element, invalidFields) === -1;
    });
    fieldsListStatus(formId, validFields, invalidFields, message = '', origin = 'cl');
  }
}

// form submit first func
$(document).on('submit', 'form', function (event) {
  var form = $(this);
  var formId = form.attr('id');
  if (formId === "login-form" || formId === "profile-form" || formId === "request-form" || formId === "reset-form" || formId === "mark_notifications") {
    return;
  }
  if (formId.includes("view-form")) {
    var staticUrl = form.attr('action');
    var cutLast = staticUrl.substr(0, staticUrl.lastIndexOf("/") + 1);
    var url = cutLast + form.data('id'); // for dynamic content
  }
  else {
    var url = form.attr('action');
  }
  // var method = form.attr('method');
  var formData = collectFormData(formId);
  event.preventDefault();
  sendForm(form, formId, url, formData);
});

