document.addEventListener('DOMContentLoaded', function() {
    // Функция для форматирования даты
    function formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString('ru-RU');
    }

    // Функция для получения типа графика на русском
    function getScheduleTypeDisplay(type) {
        const types = {
            'weekly': 'Недельный',
            'single': 'Однодневный',
            'flexible': 'Гибкий'
        };
        return types[type] || type;
    }

    // Функция для получения цветов в зависимости от типа
    function getTypeColors(type) {
        const colors = {
            'weekly': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
            'single': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
            'flexible': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
        };
        return colors[type] || colors['weekly'];
    }

    // Загрузка данных
    fetch('/api/today-data/')
        .then(response => response.json())
        .then(data => {
            // Обновляем общее количество графиков
            document.getElementById('total-schedules').textContent = data.total_schedules;

            // Обновляем события на сегодня
            const todayEventsContainer = document.getElementById('today-events');
            if (data.today_events.length > 0) {
                todayEventsContainer.innerHTML = data.today_events.map(event => `
                    <div class="flex items-center space-x-3">
                        <div class="flex-shrink-0">
                            <span class="inline-flex items-center justify-center h-8 w-8 rounded-full ${getTypeColors(event.type)}">
                                ${event.title.charAt(0).toUpperCase()}
                            </span>
                        </div>
                        <div class="min-w-0 flex-1">
                            <p class="text-sm font-medium text-gray-900 dark:text-white">
                                ${event.title}
                            </p>
                            <p class="text-sm text-gray-500 dark:text-gray-400">
                                ${event.start_time} - ${event.end_time}
                            </p>
                        </div>
                    </div>
                `).join('');
            } else {
                todayEventsContainer.innerHTML = '<p class="text-sm text-gray-500 dark:text-gray-400">На сегодня дел нет</p>';
            }

            // Обновляем последние графики
            const recentSchedulesContainer = document.getElementById('recent-schedules');
            if (data.recent_schedules.length > 0) {
                recentSchedulesContainer.innerHTML = getRecentSchedulesHtml(data);
            } else {
                recentSchedulesContainer.innerHTML = getEmptyStateHtml();
            }
        })
        .catch(error => console.error('Error:', error));

    // Инициализация календаря
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'ru',
        headerToolbar: {
            left: 'prev,next',
            center: 'title',
            right: ''
        },
        buttonText: {
            today: 'Сегодня',
            month: 'Месяц'
        },
        titleFormat: { year: 'numeric', month: 'long' },
        dayHeaderFormat: { weekday: 'short' },
        height: 'auto',
        fixedWeekCount: false,
        showNonCurrentDates: true,
        events: '/api/all-events/',
        eventDisplay: 'block',
        eventTimeFormat: {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        },
        firstDay: 1,
        displayEventEnd: true,
        slotMinTime: '00:00:00',
        slotMaxTime: '24:00:00',
        eventContent: function(arg) {
            return {
                html: `
                    <div class="fc-event-main-frame">
                        <div class="fc-event-dot" style="background-color: ${arg.event.backgroundColor}"></div>
                        <div class="fc-event-title">${arg.event.title}</div>
                        <div class="fc-event-time">${arg.event.extendedProps.startTime || arg.event.start.toLocaleTimeString('ru-RU', {hour: '2-digit', minute:'2-digit'})}</div>
                    </div>
                `
            };
        }
    });
    calendar.render();

    // Вспомогательные функции для HTML
    function getRecentSchedulesHtml(data) {
        return `
            <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
                <div>
                    <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                        Последние графики
                    </h3>
                    <p class="mt-1 max-w-2xl text-sm text-gray-500 dark:text-gray-400">
                        Ваши недавно созданные или обновленные графики
                    </p>
                </div>
            </div>
            <div class="border-t border-gray-200 dark:border-gray-700">
                <ul class="divide-y divide-gray-200 dark:divide-gray-700">
                    ${data.recent_schedules.map(schedule => getScheduleItemHtml(schedule)).join('')}
                </ul>
                ${getShowAllLinkHtml(data.total_schedules)}
            </div>
        `;
    }

    function getScheduleItemHtml(schedule) {
        return `
            <li class="px-4 py-4 sm:px-6 hover:bg-gray-50 dark:hover:bg-gray-700">
                <div class="flex items-center justify-between">
                    <div class="flex-1 min-w-0">
                        <a href="/schedule/${schedule.id}/" class="text-sm font-medium text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300 truncate">
                            ${schedule.title}
                        </a>
                        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                            ${schedule.description || ''}
                        </p>
                    </div>
                    <div class="ml-4 flex-shrink-0 flex items-center space-x-4">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getTypeColors(schedule.schedule_type)}">
                            ${getScheduleTypeDisplay(schedule.schedule_type)}
                        </span>
                        <span class="text-sm text-gray-500 dark:text-gray-400">
                            ${formatDate(schedule.created_at)}
                        </span>
                    </div>
                </div>
            </li>
        `;
    }

    function getShowAllLinkHtml(totalSchedules) {
        return totalSchedules > 5 ? `
            <div class="bg-gray-50 dark:bg-gray-700 px-4 py-4 sm:px-6">
                <a href="/schedule/" class="text-sm font-medium text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300">
                    Показать все графики <span aria-hidden="true">&rarr;</span>
                </a>
            </div>
        ` : '';
    }

    function getEmptyStateHtml() {
        return `
            <div class="px-4 py-12 text-center">
                <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">Нет графиков</h3>
                <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                    Начните с создания вашего первого графика.
                </p>
                <div class="mt-6">
                    <a href="/schedule/create/"
                       class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700">
                        Создать график
                    </a>
                </div>
            </div>
        `;
    }
}); 