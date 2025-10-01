class ScheduleList {
    constructor() {
        this.init();
    }

    init() {
        this.loadSchedules();
    }

    loadSchedules() {
        fetch('/api/schedules/')
            .then(response => response.json())
            .then(data => this.renderSchedules(data))
            .catch(error => {
                console.error('Error:', error);
                this.renderError();
            });
    }

    renderSchedules(data) {
        const container = document.getElementById('schedules-container');
        
        if (data.schedules.length > 0) {
            container.innerHTML = this.getSchedulesListHtml(data.schedules);
        } else {
            container.innerHTML = this.getEmptyStateHtml();
        }
    }

    getSchedulesListHtml(schedules) {
        return `
            <div class="bg-white dark:bg-gray-800 shadow overflow-hidden sm:rounded-lg">
                <ul class="divide-y divide-gray-200 dark:divide-gray-700">
                    ${schedules.map(schedule => this.getScheduleItemHtml(schedule)).join('')}
                </ul>
            </div>
        `;
    }

    getScheduleItemHtml(schedule) {
        return `
            <li class="px-4 py-4 sm:px-6 hover:bg-gray-50 dark:hover:bg-gray-700">
                <div class="flex items-center justify-between">
                    <div class="flex-1 min-w-0">
                        <a href="/schedule/${schedule.id}/" 
                           class="text-lg font-medium text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300">
                            ${schedule.title}
                        </a>
                        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                            ${schedule.description || ''}
                        </p>
                    </div>
                    <div class="ml-4 flex-shrink-0 flex items-center space-x-4">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${ScheduleUtils.getTypeColors(schedule.schedule_type)}">
                            ${ScheduleUtils.getScheduleTypeDisplay(schedule.schedule_type)}
                        </span>
                        <span class="text-sm text-gray-500 dark:text-gray-400">
                            ${ScheduleUtils.formatDate(schedule.created_at)}
                        </span>
                        <div class="flex space-x-2">
                            <a href="${this.getEditUrl(schedule.schedule_type, schedule.id)}" 
                               class="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300">
                                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                                </svg>
                            </a>
                            <a href="/schedule/${schedule.id}/delete/" 
                               class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300">
                                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>
            </li>
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

    getEmptyStateHtml() {
        return `
            <div class="text-center py-12 bg-white dark:bg-gray-800 shadow sm:rounded-lg">
                <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">Нет графиков</h3>
                <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                    У вас пока нет созданных графиков
                </p>
            </div>
        `;
    }

    renderError() {
        document.getElementById('schedules-container').innerHTML = `
            <div class="text-center py-12 bg-white dark:bg-gray-800 shadow sm:rounded-lg">
                <p class="text-red-600 dark:text-red-400">Ошибка при загрузке графиков</p>
            </div>
        `;
    }
} 