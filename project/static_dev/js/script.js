
document.addEventListener('change', changeEvent);
document.addEventListener('click', clickEvent);

function changeEvent(event){
    if (event.target.closest('.input_file')){
        let fileInput = event.target.closest('.input_file');
        let countFiles = '';
        if (fileInput.files && fileInput.files.length >= 1){
            countFiles = fileInput.files.length;
        }
        if (countFiles){
            let fileField = event.target.closest('.form__field');
            let fileFieldContent = fileField.querySelector('.form__field-content');

            fileFieldContent.innerHTML = `Выбрано файлов: ${countFiles}`;
        } else{
            fileFieldContent.innerHTML = `Файлы не выбраны`;
        }
    }
}

function clickEvent(event){
    if (event.target.closest('.modal_btn')) {
        let body = document.querySelector('body');
        let modals = document.querySelector('.modals');
        let modalBtn = event.target.closest('.modal_btn');
        let modalItems = document.querySelectorAll('.modal');
        modalItems.forEach(item => item.classList.remove('._active'));
        let activateModal = document.querySelector(`#${modalBtn.id}`);

        if (activateModal){
            activateModal.classList.add('_active');
            modals.classList.add('_active');
            body.classList.add('_lock');
        }
    }
    if (event.target.closest('.btn_filter_close') || event.target.classList.value.includes("modals")) {

        let body = document.querySelector('body');
        let modals = document.querySelector('.modals');
        let activeModal = document.querySelector(`.modal._active`);

        if (activeModal){
            activeModal.classList.remove('_active');
            modals.classList.remove('_active');
            body.classList.remove('_lock');
        }
    }
}