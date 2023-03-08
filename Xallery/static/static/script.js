const deleteForm = document.querySelector('#delete-picture-form');
const submitButton = document.querySelector('.delete-button');
submitButton.addEventListener('click', submit);

function submit() {
	
       deleteForm.submit();
	};
