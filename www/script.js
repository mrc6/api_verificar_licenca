// Select the form and message elements
const myForm = document.getElementById('myForm');
const userInfo = document.getElementById('userInfo');
const email = document.getElementById('email');
const password = document.getElementById('password');
const responseMessage = document.getElementById('responseMessage');

// Add an event listener for the form's submit event
myForm.addEventListener('submit', function (event) {
    // Prevent the default browser form submission (which causes a page refresh)
    event.preventDefault();

    // Collect the form data using the FormData API
    const formData = new FormData(this);
    formData.append('email', email.value);
    formData.append('password', password.value);
    const formObject = Object.fromEntries(formData);
    console.log(formObject);

    // Define the options for the fetch request
    const fetchOptions = {
        method: 'POST', // Specify the method as POST
        headers: {
            'Content-Type': 'application/json; charset=UTF-8', // Inform the server the data format
        },
        body: JSON.stringify(formObject),
    };

    // Specify the URL of your server endpoint
    const url = 'http://127.0.0.1:8080/login'; // Change this to your actual server URL

    // Perform the fetch request
    fetch(url, fetchOptions)
        .then(response => {
            // Check if the request was successful (status 200-299)
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            // Parse the response body as JSON (or .text() if the server responds with plain text)
            return response.json();
        })
        .then(data => {
            // Handle the successful response data from the server
            console.log('Success:', data);
            responseMessage.textContent = 'Form submitted successfully! Server response: ' + JSON.stringify(data);
            responseMessage.style.color = 'green';
            myForm.reset(); // Optionally reset the form
            localStorage.setItem('lic_api_token', data.token); // Store the response data in localStorage
        })
        .catch(error => {
            // Handle network errors or errors thrown in the .then() block
            console.error('Error:', error);
            responseMessage.textContent = 'An error occurred: ' + error.message;
            responseMessage.style.color = 'red';
            localStorage.setItem('lic_api_token', ''); // Store the response data in localStorage
        });
});

// Add an event listener for the form's submit event
userInfo.addEventListener('submit', function (event) {
    // Prevent the default browser form submission (which causes a page refresh)
    event.preventDefault();

    // Define the options for the fetch request
    const fetchOptions = {
        method: 'GET', // Specify the method as GET
        headers: {
            'Content-Type': 'application/json; charset=UTF-8', // Inform the server the data format
            'Authorization': 'Bearer ' + localStorage.getItem('lic_api_token') // Include the stored token in the request headers
        },
    };

    // Specify the URL of your server endpoint
    const url = 'http://127.0.0.1:8080/user/all'; // Change this to your actual server URL

    // Perform the fetch request
    fetch(url, fetchOptions)
        .then(response => {
            // Check if the request was successful (status 200-299)
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            // Parse the response body as JSON (or .text() if the server responds with plain text)
            return response.json();
        })
        .then(data => {
            // Handle the successful response data from the server
            console.log('Success:', data);
            responseMessage.textContent = 'Form submitted successfully! Server response: ' + JSON.stringify(data);
        })
        .catch(error => {
            // Handle network errors or errors thrown in the .then() block
            console.error('Error:', error);
            responseMessage.textContent = 'An error occurred: ' + error.message;
            responseMessage.style.color = 'red';
        });
});