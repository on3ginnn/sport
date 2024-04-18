const body = document.querySelector('body');
const modals = document.querySelector('.modals');

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

let hideModals = [];
let activeModal = null;

function clickEvent(event){
    if (event.target.closest('.modal_btn')) {
        let modalBtn = event.target.closest('.modal_btn');
        let activateModal = document.querySelector(`.modal#${modalBtn.id}`);

        if (activateModal){
            modals.classList.add('_active');
            body.classList.add('_lock');

            let modalItems = document.querySelectorAll('.modal');
            modalItems.forEach(item => item.classList.remove('_active'));

            if (activeModal) {
                hideModals.push(activeModal);
            }
            
            activeModal = activateModal;

            activeModal.classList.add('_active');
        }
    }
    if (event.target.closest('.btn_filter_close') || event.target.classList.value.includes("modals")) {

        if (activeModal){
            activeModal.classList.remove('_active');

            if (hideModals.length > 0) {
                activeModal = hideModals.pop();
                activeModal.classList.add('_active');
            } else {
                activeModal = null;

                modals.classList.remove('_active');
                body.classList.remove('_lock');
            }
        }
    }
    if (event.target.closest('.form__button') && event.target.classList.value.includes("btn")){
        if (activeModal){
            activeModal.classList.remove('_active');

            if (hideModals.length > 0) {
                activeModal = hideModals.pop();
                activeModal.classList.add('_active');
            } else {
                activeModal = null;
                
                modals.classList.remove('_active');
                body.classList.remove('_lock');
            }
        }
    }
}