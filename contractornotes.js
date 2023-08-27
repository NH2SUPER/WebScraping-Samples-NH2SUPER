//no ads results each page
.search-results.organic .result

//contractor name
.business-name

//Services Offered

//email address

//website

//address

//certifications/accreditations

//notable projects

//notes

//city

//phone number
.phone.primary


const results = [];
const parent = document.querySelectorAll('.search-results.organic .result');
Array.from(parent).forEach((row) => {
	const nameElement = row.querySelector('.business-name span');
	const name = nameElement.textContent;
	const phoneElement = row.querySelector('.phone.primary');
	const phone = phoneElement.textContent;

	results.push({name, phone});

});

console.log(results);