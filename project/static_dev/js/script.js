
document.addEventListener('change', changeEvent);

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
