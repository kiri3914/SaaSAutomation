class ScheduleDetail {
    constructor(scheduleId) {
        this.scheduleId = scheduleId;
        this.init();
    }

    init() {
        this.loadScheduleData();
    }

    loadScheduleData() {
        fetch(`/api/schedule/${this.scheduleId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                this.updateScheduleInfo(data);
                this.initializeCalendar();
            })
            .catch(error => {
                console.error('Error:', error);
                this.showError();
                window.notifications.show('Ошибка при загрузке данных графика', 'error');
            });
    }

    showError() {
        document.getElementById('schedule-container').innerHTML = `
            <div class="text-center py-12">
                <svg class="mx-auto h-12 w-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
                <h3 class="mt-2 text-lg font-medium text-gray-900 dark:text-white">Ошибка загрузки</h3>
                <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                    Не удалось загрузить данные графика. Пожалуйста, попробуйте позже.
                </p>
                <div class="mt-6">
                    <a href="/schedule/" class="btn btn-primary">
                        Вернуться к списку графиков
                    </a>
                </div>
            </div>
        `;
    }

    updateScheduleInfo(data) {
        document.getElementById('schedule-title').textContent = data.title;
        document.getElementById('schedule-description').textContent = data.description || '';
        document.getElementById('schedule-actions').innerHTML = this.getActionsHtml(data);
        
        // Обновляем детали расписания
        const detailsContainer = document.getElementById('schedule-details');
        if (data.schedule_type === 'weekly' && data.weekly_schedules?.length > 0) {
            detailsContainer.innerHTML = `
                <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Недельное расписание</h4>
                <div class="space-y-4">
                    ${data.weekly_schedules.map(ws => `
                        <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                            <p class="text-sm text-gray-700 dark:text-gray-200">
                                ${ws.weekday_display}: ${ws.start_time} - ${ws.end_time}
                            </p>
                            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                                Период: ${ScheduleUtils.formatDate(ws.start_date)} - ${ScheduleUtils.formatDate(ws.end_date)}
                            </p>
                        </div>
                    `).join('')}
                </div>
            `;
        } else if (data.schedule_type === 'single' && data.single_day_schedule) {
            detailsContainer.innerHTML = `
                <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Однодневное расписание</h4>
                <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                    <p class="text-sm text-gray-700 dark:text-gray-200">
                        Дата: ${ScheduleUtils.formatDate(data.single_day_schedule.date)}
                    </p>
                    <p class="text-sm text-gray-700 dark:text-gray-200 mt-1">
                        Время: ${data.single_day_schedule.start_time} - ${data.single_day_schedule.end_time}
                    </p>
                </div>
            `;
        } else if (data.schedule_type === 'flexible' && data.flexible_schedule) {
            detailsContainer.innerHTML = `
                <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Гибкое расписание</h4>
                <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                    <p class="text-sm text-gray-700 dark:text-gray-200">
                        Период: ${ScheduleUtils.formatDate(data.flexible_schedule.start_date)} - ${ScheduleUtils.formatDate(data.flexible_schedule.end_date)}
                    </p>
                    <p class="text-sm text-gray-700 dark:text-gray-200 mt-1">
                        Время: ${data.flexible_schedule.start_time} - ${data.flexible_schedule.end_time}
                    </p>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                        Тип повтора: ${data.flexible_schedule.repeat_type_display}
                    </p>
                </div>
            `;
        }
    }

    getActionsHtml(data) {
        return `
            <a href="${this.getEditUrl(data.schedule_type, data.id)}" 
               class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
                Редактировать
            </a>
            <a href="/schedule/${data.id}/delete/" 
               class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700">
                <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
                Удалить
            </a>
        `;
    }

    getEditUrl(scheduleType, scheduleId) {
        switch(scheduleType) {
            case 'weekly':
                return `/schedule/${scheduleId}/edit/weekly/`;
            case 'single':
                return `/schedule/${scheduleId}/edit/single/`;
            case 'flexible':
                return `/schedule/${scheduleId}/edit/flexible/`;
            default:
                return `/schedule/${scheduleId}/edit/`;
        }
    }

    initializeCalendar() {
        const calendarEl = document.getElementById('calendar');
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'ru',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: `/schedule/${this.scheduleId}/events/`,
            height: 'auto',
            firstDay: 1,
            dayMaxEvents: true,
            eventTimeFormat: {
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
            },
            slotMinTime: '06:00:00',
            slotMaxTime: '22:00:00',
            slotDuration: '00:30:00',
            expandRows: true,
            navLinks: true,
            nowIndicator: true,
            dayHeaders: true,
            weekNumbers: false,
            weekNumberCalculation: 'ISO',
            editable: false,
            selectable: false,
            selectMirror: true,
            displayEventEnd: true,
            eventDisplay: 'block',
            eventBackgroundColor: 'rgb(79 70 229)',
            eventBorderColor: 'rgb(79 70 229)',
            eventTextColor: 'white',
            eventClassNames: ['shadow-sm'],
            views: {
                timeGrid: {
                    dayMaxEvents: 4
                },
                dayGrid: {
                    dayMaxEvents: 4
                }
            }
        });
        
        // Сохраняем ссылку на календарь глобально
        window.calendar = calendar;
        calendar.render();
    }
} 