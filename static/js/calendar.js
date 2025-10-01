// Общие функции для работы с календарем
const CalendarUtils = {
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

window.CalendarUtils = CalendarUtils; 