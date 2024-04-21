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
// неактивированные фильтры(не нажата кнопка принять)
let inActiveFilters = [];
let inActiveFiltersGames = [];
let inActiveFiltersTeams = [];
let inActiveFiltersUsers = [];
// вложенные фильтры для команд
let nestedInActiveFiltersTeams = []
let nestedInActiveFiltersUsers = []
// доступные для выбора фильтры
let availableFiltersGames = [];
let availableFiltersTeams = [];
let availableFiltersUsers = [];

// доступные для выбора фильтры
let allFiltersGames = [];
let allFiltersTeams = [];
let allFiltersUsers = [];
// события (оптимизированы)
document.addEventListener('change', changeEvent);
document.addEventListener('click', clickEvent);

// только если на странице игр
if (body.dataset.viewName === "streetsport:orders"){
    // доступные для выбора фильтры
    allFiltersGames = games.slice();
    allFiltersTeams = teams.slice();
    allFiltersUsers = users.slice();
    document.addEventListener('DOMContentLoaded', filtrationApplyed);
}

// сбор всех активных фильтров
function filterAdd() {

    inActiveFilters = [];
    // собираем фильтры в актив массив
    if (inActiveFiltersGames.length === 0) {
        availableFiltersGames = allFiltersGames.slice();
    } else {
        inActiveFilters.push(...inActiveFiltersGames);
        availableFiltersGames = allFiltersGames.filter(filter => !inActiveFiltersGames.includes(filter));
    }
    if (nestedInActiveFiltersTeams.length === 0) {
        availableFiltersTeams = teams.slice();
    } else {
        inActiveFilters.push(...nestedInActiveFiltersTeams);
        availableFiltersTeams = allFiltersTeams.filter(filter => !nestedInActiveFiltersTeams.includes(filter));
    }
    if (nestedInActiveFiltersUsers.length === 0) {
        availableFiltersUsers = users.slice();
    } else {
        inActiveFilters.push(...nestedInActiveFiltersUsers);
        availableFiltersUsers = allFiltersUsers.filter(filter => !nestedInActiveFiltersUsers.includes(filter));
    }
}

// рендеринг всех фильтров на странице
function rendering(){
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
    if (inActiveFilters.length === 0){
        render(filterActivePublicContainer);
    } else {
        inActiveFilters.forEach(filter => {
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

    // рендер фильтров команды как в главных фильтрах так и в фильтрах команды
    const teamsFilterAvailable = document.querySelector(".available_filters.filter_teams");
    const teamsFilterAvailableContainer = teamsFilterAvailable.querySelector('.filter_container');
    const teamsFilterActive = document.querySelector('.active_filters_teams');
    const teamsFilterActiveContainer = teamsFilterActive.querySelector('.filter_container');
    teamsFilterAvailableContainer.innerHTML = "";
    teamsFilterActiveContainer.innerHTML = "";
    if (nestedInActiveFiltersTeams.length === 0) {
        render(teamsFilterActiveContainer);
        availableFiltersTeams.forEach(filter => {
            render(teamsFilterAvailableContainer, content=filter.title, dataId=filter.id);
        });
    } else {
        nestedInActiveFiltersTeams.forEach(filter => {
            render(teamsFilterActiveContainer, content=filter.title, dataId=filter.id, dataCategory=filter.category);
        });
        availableFiltersTeams.forEach(filter => {
            render(teamsFilterAvailableContainer, content=filter.title, dataId=filter.id);
        });
    }

    const usersFilterAvailable = document.querySelector(".available_filters.filter_users");
    const usersFilterAvailableContainer = usersFilterAvailable.querySelector('.filter_container');
    const usersFilterActive = document.querySelector('.active_filters_users');
    const usersFilterActiveContainer = usersFilterActive.querySelector('.filter_container');
    usersFilterAvailableContainer.innerHTML = "";
    usersFilterActiveContainer.innerHTML = "";
    if (nestedInActiveFiltersUsers.length === 0) {
        render(usersFilterActiveContainer);
        availableFiltersUsers.forEach(filter => {
            render(usersFilterAvailableContainer, content=filter.username, dataId=filter.id);
        });
    } else {
        nestedInActiveFiltersUsers.forEach(filter => {
            render(usersFilterActiveContainer, content=filter.username, dataId=filter.id, dataCategory=filter.category);
        });
        availableFiltersUsers.forEach(filter => {
            render(usersFilterAvailableContainer, content=filter.username, dataId=filter.id);
        });
    }
}
// добавление и рендеринг всех фильтров на странице
function filterRender(
){
    filterAdd();
    rendering();
}

// запуск рендеринга фильтров (для принятия всех фильтров)
function filtrationApplyed(
){

    filterRender();
    ordersFilterRender();
}

// событие замены сотояния
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
    if (event.target.closest('.filter_leaderboard')) {
        let leaderBoardSelect = event.target.closest('.filter_leaderboard');
        let avtivateLeaderBoardHref = leaderBoardSelect.value;
        document.location.href = avtivateLeaderBoardHref;
    }
}

// перенос всех фильров с модального окна на страницу ордеров
function ordersFilterRender(){
    const filterActive = document.querySelector(".active_filters.active_filters_public");
    const filterActivePublicContainer = filterActive.querySelector('.filter_container');
    const orderFilters = document.querySelector(".orders_filters");
    const orderFiltersContainer = orderFilters.querySelector(".filter_container");
    orderFiltersContainer.innerHTML = filterActivePublicContainer.innerHTML;
}

// событие клика
function clickEvent(event){
    // отркытие модальных окон
    if (event.target.closest('.modal_btn')) {
        let modalBtn = event.target.closest('.modal_btn');
        let activateModal = document.querySelector(`.modal#${modalBtn.id}`);

        if (activateModal){
            // подгружаем сохраненную версию фильтров при открытии
            if (activateModal.closest('#filterModal')){
                inActiveFiltersGames = activeFiltersGames.slice();
                inActiveFiltersUsers = activeFiltersUsers.slice();
                nestedInActiveFiltersUsers = inActiveFiltersUsers.slice();
                inActiveFiltersTeams = activeFiltersTeams.slice();
                nestedInActiveFiltersTeams = inActiveFiltersTeams.slice();
            } else if (activateModal.closest('#searchTeamModal')) {
                nestedInActiveFiltersTeams = inActiveFiltersTeams.slice();
            } else if (activateModal.closest('#searchUserModal')) {
                nestedInActiveFiltersUsers = inActiveFiltersUsers.slice();
            }

            filterRender();

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
    // закрытие фильтров без применения
    if (event.target.closest('.btn_filter_close') || event.target.classList.value.includes("modals")) {

        if (activeModal){

            if (activeModal.closest('#filterModal')) {
                inActiveFiltersGames = activeFiltersGames.slice();
                inActiveFiltersTeams = activeFiltersTeams.slice();
                nestedInActiveFiltersTeams = inActiveFiltersTeams.slice();
                inActiveFiltersUsers = activeFiltersUsers.slice();
                nestedInActiveFiltersUsers = inActiveFiltersUsers.slice();
            } else if (activeModal.closest('#searchTeamModal')) {
                nestedInActiveFiltersTeams = inActiveFiltersTeams.slice();
            } else if (activeModal.closest('#searchUserModal')) {
                nestedInActiveFiltersUsers = inActiveFiltersUsers.slice();
            }

            activeModal.classList.remove('_active');

            if (hideModals.length > 0) {
                activeModal = hideModals.pop();
                activeModal.classList.add('_active');
            } else {
                activeModal = null;

                modals.classList.remove('_active');
                body.classList.remove('_lock');
            }
            
            filterRender();
        }
    }
    // кнопка Применить фильры
    if (event.target.closest('.form__button') && event.target.classList.value.includes("btn")){
        if (activeModal){
            activeModal.classList.remove('_active');

            if (activeModal.closest('#filterModal')) {
                activeFiltersGames = inActiveFiltersGames.slice();
                activeFiltersUsers = inActiveFiltersUsers.slice();
                activeFiltersTeams = inActiveFiltersTeams.slice();
            } else if (activeModal.closest('#searchTeamModal')) {
                inActiveFiltersTeams = nestedInActiveFiltersTeams.slice();
            } else if (activeModal.closest('#searchUserModal')) {
                inActiveFiltersUsers = nestedInActiveFiltersUsers.slice();
            }

            if (hideModals.length > 0) {
                activeModal = hideModals.pop();
                activeModal.classList.add('_active');

                filterRender();
            } else {
                activeModal = null;
                
                modals.classList.remove('_active');
                body.classList.remove('_lock');

                filtrationApplyed();
            }
        }
    }
    // добавление фильра
    if (event.target.closest('.btn.filter')) {

        let filterItem = event.target.closest('.filters__item');
        
        // активация фильтра
        if (event.target.closest('.available_filters')) {
            if (event.target.closest('.filter_games')) {
                let filterElement = availableFiltersGames.find(filter => +filter.id === +filterItem.dataset.id);
                filterElement.content = filterElement.title;
                filterElement.category = 'game';
                if (filterElement){
                    inActiveFiltersGames.push(filterElement);
                }
            }
            if (event.target.closest('.filter_teams')) {
                let filterElement = availableFiltersTeams.find(filter => +filter.id === +filterItem.dataset.id);
                
                filterElement.content = `команда: ${filterElement.title}`;
                filterElement.category = 'team';

                if (filterElement){
                    nestedInActiveFiltersTeams.push(filterElement);
                }
            }
            if (event.target.closest('.filter_users')) {
                let filterElement = availableFiltersUsers.find(filter => +filter.id === +filterItem.dataset.id);
                
                filterElement.content = `игрок: ${filterElement.username}`;
                filterElement.category = 'user';

                if (filterElement){
                    nestedInActiveFiltersUsers.push(filterElement);
                }
            }
        }
        // отмена фильтра
        if (event.target.closest('.active_filters') || event.target.closest('.orders_filters')) {
            if (filterItem.dataset.category) {
                if (filterItem.dataset.category === "game") {
                    let filterElement = inActiveFiltersGames.find(filter => +filter.id === +filterItem.dataset.id);

                    if (filterElement){
                        inActiveFiltersGames = inActiveFiltersGames.filter(filter => +filter.id !== +filterItem.dataset.id);
                    }
                }
                if (filterItem.dataset.category === "team") {
                    let filterElement = nestedInActiveFiltersTeams.find(filter => +filter.id === +filterItem.dataset.id);
    
                    if (filterElement){
                        nestedInActiveFiltersTeams = nestedInActiveFiltersTeams.filter(filter => +filter.id !== +filterItem.dataset.id);
                    }
                }
                if (filterItem.dataset.category === "user") {
                    let filterElement = nestedInActiveFiltersUsers.find(filter => +filter.id === +filterItem.dataset.id);
                    filterElement.content = '';
                    filterElement.category = '';
    
                    if (filterElement){
                        nestedInActiveFiltersUsers = nestedInActiveFiltersUsers.filter(filter => +filter.id !== +filterItem.dataset.id);
                    }
                }
            }
        }
        
        if (event.target.closest('.orders_filters')){
            activeFiltersGames = inActiveFiltersGames.slice();
            inActiveFiltersTeams = nestedInActiveFiltersTeams.slice();
            activeFiltersTeams = inActiveFiltersTeams.slice();
            inActiveFiltersUsers = nestedInActiveFiltersUsers.slice();
            activeFiltersUsers = inActiveFiltersUsers.slice();

            filtrationApplyed();
        } else {
            filterRender();
        }
    }
    if (event.target.closest('.search_header_btn')) {
        const searchBtn = event.target.closest('.search_header_btn');
        const searchHeader = document.querySelector('.search-header');
        searchBtn.classList.toggle('_active');
        searchHeader.classList.toggle('_active');
    }
}