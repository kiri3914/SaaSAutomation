// Общие функции для работы с данными расписания
const ScheduleUtils = {
    // Функция для форматирования даты
    formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString('ru-RU');
    },

    // Функция для получения типа графика на русском
    getScheduleTypeDisplay(type) {
        const types = {
            'weekly': 'Недельный',
            'single': 'Однодневный',
            'flexible': 'Гибкий'
        };
        return types[type] || type;
    },

    // Функция для получения цветов в зависимости от типа
    getTypeColors(type) {
        const colors = {
            'weekly': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
            'single': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
            'flexible': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
        };
        return colors[type] || colors['weekly'];
    },

    // Функция для инициализации календаря
    initializeCalendar(elementId, eventsUrl) {
        const calendarEl = document.getElementById(elementId);
        const calendar = new FullCalendar.Calendar(calendarEl, {
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
            events: eventsUrl,
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
        return calendar;
    }
};

// Экспортируем утилиты для использования в других файлах
window.ScheduleUtils = ScheduleUtils; 