const body = document.querySelector('body');
const modals = document.querySelector('.modals');
let hideModals = [];
let activeModal = null;

// шаблон элемента фильтра
const filterSample = body.dataset.filterItem;

// данные с сервера
let games = JSON.parse(body.dataset.games ? body.dataset.games : null);
let teams = JSON.parse(body.dataset.teams ? body.dataset.teams : null);
let users = JSON.parse(body.dataset.users ? body.dataset.users : null);
console.log(games);
console.log(teams);
console.log(users);

// активные фильтры (общие и по категориям отдельно)
let activeFilters = [];
let activeFiltersGames = [];
let activeFiltersTeams = [];
let activeFiltersUsers = [];

// доступные для выбора фильтры
let availableFiltersGames = games.slice();
let availableFiltersTeams = teams.slice();
let availableFiltersUsers = users.slice();

// события (оптимизированы)
document.addEventListener('change', changeEvent);
document.addEventListener('click', clickEvent);
document.addEventListener('DOMContentLoaded', filtrationRendering);

// рендеринг всех фильтров на странице
function filterRender(){
    console.log(activeFiltersGames);
    console.log(activeFiltersTeams);
    console.log(activeFiltersUsers);
    activeFilters = [];

    // собираем фильтры в актив массив
    if (activeFiltersGames.length === 0) {
        availableFiltersGames = games.slice();
    } else {
        activeFilters.push(...activeFiltersGames);
    }
    if (activeFiltersTeams.length === 0) {
        availableFiltersTeams = teams.slice();
    } else {
        activeFilters.push(...activeFiltersTeams);
    }
    if (activeFiltersUsers.length === 0) {
        availableFiltersUsers = users.slice();
    } else {
        activeFilters.push(...activeFiltersUsers);
    }

    // функция для рендера
    function render(container, content="все", dataId=null, dataCategory=null){
        const filterItem = document.createElement('li');
        filterItem.classList.add("filters__item");
        filterItem.innerHTML = filterSample;
        if (dataId) {
            filterItem.setAttribute("data-id", dataId);
        }
        if (dataCategory) {
            filterItem.setAttribute("data-category", dataCategory);
        }

        container.insertAdjacentElement('beforeend', filterItem);

        let filterContent = filterItem.querySelector('.filter__content');
        filterContent.innerHTML = content;
    }
    // рендер активных фильтров на странице
    const filterActive = document.querySelector(".active_filters.active_filters_public");
    const filterActivePublicContainer = filterActive.querySelector('.filter_container');
    filterActivePublicContainer.innerHTML = "";
    if (activeFilters.length === 0){
        render(filterActivePublicContainer);
    } else {
        activeFilters.forEach(filter => {
            render(filterActivePublicContainer, content=filter.content, dataId=filter.id, dataCategory=filter.category);
        });
    }

    // рендер доступных фильтров на странице
    const gamesFilterAvailable = document.querySelector(".available_filters.filter_games");
    const gamesFilterAvailableContainer = gamesFilterAvailable.querySelector('.filter_container');
    gamesFilterAvailableContainer.innerHTML = "";
    availableFiltersGames.forEach(filter => {
        render(gamesFilterAvailableContainer, content=filter.title, dataId=filter.id);
    });

    const teamsFilterAvailable = document.querySelector(".available_filters.filter_teams");
    const teamsFilterAvailableContainer = teamsFilterAvailable.querySelector('.filter_container');
    const teamsFilterActive = document.querySelector('.active_filters_teams');
    const teamsFilterActiveContainer = teamsFilterActive.querySelector('.filter_container');
    teamsFilterAvailableContainer.innerHTML = "";
    teamsFilterActiveContainer.innerHTML = "";
    if (activeFiltersTeams.length === 0) {
        render(teamsFilterActiveContainer);
        availableFiltersTeams.forEach(filter => {
            render(teamsFilterAvailableContainer, content=filter.title, dataId=filter.id);
        });
    } else {
        availableFiltersTeams.forEach(filter => {
            render(teamsFilterAvailableContainer, content=filter.title, dataId=filter.id);
        });
        activeFiltersTeams.forEach(filter => {
            render(teamsFilterActiveContainer, content=filter.title, dataId=filter.id, dataCategory=filter.category);
        });
    }

    const usersFilterAvailable = document.querySelector(".available_filters.filter_users");
    const usersFilterAvailableContainer = usersFilterAvailable.querySelector('.filter_container');
    const usersFilterActive = document.querySelector('.active_filters_users');
    const usersFilterActiveContainer = usersFilterActive.querySelector('.filter_container');
    usersFilterAvailableContainer.innerHTML = "";
    usersFilterActiveContainer.innerHTML = "";
    if (activeFiltersUsers.length === 0) {
        render(usersFilterActiveContainer);
        availableFiltersUsers.forEach(filter => {
            render(usersFilterAvailableContainer, content=filter.username, dataId=filter.id);
        });
    } else {
        availableFiltersUsers.forEach(filter => {
            render(usersFilterAvailableContainer, content=filter.username, dataId=filter.id);
        });
        activeFiltersUsers.forEach(filter => {
            render(usersFilterActiveContainer, content=filter.username, dataId=filter.id, dataCategory=filter.category);
        });
    }
    
}

function filtrationRendering(event){
    filterRender();
    ordersFilterRender();
}

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


function ordersFilterRender(){
    const filterActive = document.querySelector(".active_filters.active_filters_public");
    const filterActivePublicContainer = filterActive.querySelector('.filter_container');
    const orderFilters = document.querySelector(".orders_filters");
    const orderFiltersContainer = orderFilters.querySelector(".filter_container");
    orderFiltersContainer.innerHTML = filterActivePublicContainer.innerHTML;
}

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

                ordersFilterRender();
            }
        }
    }
    if (event.target.closest('.btn.filter')) {

        let filterItem = event.target.closest('.filters__item');
        
        // активация фильтра
        if (event.target.closest('.available_filters')) {
            if (event.target.closest('.filter_games')) {
                let filterElement = availableFiltersGames.find(filter => +filter.id === +filterItem.dataset.id);
                filterElement.content = filterElement.title;
                filterElement.category = 'game';
                if (filterElement){
                    activeFiltersGames.push(filterElement);
                    availableFiltersGames = availableFiltersGames.filter(filter => +filter.id !== +filterItem.dataset.id);
                }
            }
            if (event.target.closest('.filter_teams')) {
                let filterElement = availableFiltersTeams.find(filter => +filter.id === +filterItem.dataset.id);
                
                filterElement.content = `команда: ${filterElement.title}`;
                filterElement.category = 'team';

                if (filterElement){
                    activeFiltersTeams.push(filterElement);
                    availableFiltersTeams = availableFiltersTeams.filter(filter => +filter.id !== +filterItem.dataset.id);
                }
            }
            if (event.target.closest('.filter_users')) {
                let filterElement = availableFiltersUsers.find(filter => +filter.id === +filterItem.dataset.id);
                
                filterElement.content = `игрок: ${filterElement.username}`;
                filterElement.category = 'user';

                if (filterElement){
                    activeFiltersUsers.push(filterElement);
                    availableFiltersUsers = availableFiltersUsers.filter(filter => +filter.id !== +filterItem.dataset.id);
                }
            }
        }
        // отмена фильтра
        if (event.target.closest('.active_filters') || event.target.closest('.orders_filters')) {
            if (filterItem.dataset.category) {
                if (filterItem.dataset.category === "game") {
                    let filterElement = activeFiltersGames.find(filter => +filter.id === +filterItem.dataset.id);
                    filterElement.content = filterElement.title;
                    filterElement.category = '';
                    if (filterElement){
                        availableFiltersGames.push(filterElement);
                        activeFiltersGames = activeFiltersGames.filter(filter => +filter.id !== +filterItem.dataset.id);
                    }
                }
                if (filterItem.dataset.category === "team") {
                    let filterElement = activeFiltersTeams.find(filter => +filter.id === +filterItem.dataset.id);
                    filterElement.content = '';
                    filterElement.category = '';
    
                    if (filterElement){
                        availableFiltersTeams.push(filterElement);
                        activeFiltersTeams = activeFiltersTeams.filter(filter => +filter.id !== +filterItem.dataset.id);
                    }
                }
                if (filterItem.dataset.category === "user") {
                    let filterElement = activeFiltersUsers.find(filter => +filter.id === +filterItem.dataset.id);
                    filterElement.content = '';
                    filterElement.category = '';
    
                    if (filterElement){
                        availableFiltersUsers.push(filterElement);
                        activeFiltersUsers = activeFiltersUsers.filter(filter => +filter.id !== +filterItem.dataset.id);
                    }
                }
            }
        }

        filtrationRendering();
    }
}