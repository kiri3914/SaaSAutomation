class Profile {
    constructor() {
        this.loadProfileData();
    }

    async loadProfileData() {
        try {
            const response = await fetch('/accounts/profile/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const data = await response.json();
            console.log('Loaded data:', data);
            this.updateUI(data);
        } catch (error) {
            console.error('Error loading profile data:', error);
        }
    }

    updateUI(data) {
        this.updateUserInfo(data.user);
        this.updateStats(data.total_schedules);
        this.updateTodayEvents(data.today_events);
        this.updateSchedules(data.schedules);
    }

    updateUserInfo(user) {
        const avatarHtml = user.avatar_url 
            ? `<img class="h-24 w-24 rounded-full ring-4 ring-white dark:ring-gray-800 object-cover" src="${user.avatar_url}" alt="Аватар">`
            : `<div class="h-24 w-24 rounded-full ring-4 ring-white dark:ring-gray-800 bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                <span class="text-2xl font-bold text-white">${user.username[0].toUpperCase()}</span>
               </div>`;
        
        document.querySelector('.user-avatar').innerHTML = avatarHtml;
        document.querySelector('.user-name').textContent = 
            `${user.first_name} ${user.last_name}`.trim() || user.username;
        document.querySelector('.user-username').textContent = `@${user.username}`;

        const statusesHtml = this.generateStatusBadges(user);
        document.querySelector('.user-statuses').innerHTML = statusesHtml;

        document.querySelector('#email').textContent = user.email || 'Не указан';
        document.querySelector('#phone').textContent = user.phone || 'Не указан';
        document.querySelector('#date-joined').textContent = user.date_joined;
        document.querySelector('#last-login').textContent = user.last_login || 'Нет данных';
    }

    generateStatusBadges(user) {
        const badges = [];
        badges.push(`<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium 
            ${user.is_active ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 
                              'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'}">
            ${user.is_active ? 'Активен' : 'Неактивен'}
        </span>`);

        if (user.is_staff) {
            badges.push(`<span class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium 
                bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                Сотрудник
            </span>`);
        }

        if (user.is_superuser) {
            badges.push(`<span class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium 
                bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">
                Администратор
            </span>`);
        }
        return badges.join('');
    }

    updateStats(totalSchedules) {
        const element = document.querySelector('#total-schedules');
        if (element) {
            element.textContent = totalSchedules;
        }
    }

    updateTodayEvents(events) {
        const container = document.querySelector('#today-events');
        if (events.length === 0) {
            container.innerHTML = '<p class="text-sm text-gray-500 dark:text-gray-400">На сегодня дел нет</p>';
            return;
        }

        container.innerHTML = events.map(event => `
            <div class="flex items-center p-4 bg-gray-50 dark:bg-gray-700/50 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200">
                <div class="flex-shrink-0">
                    <span class="inline-flex items-center justify-center h-10 w-10 rounded-xl 
                        ${this.getScheduleTypeColors(event.schedule_type)}">
                        ${event.title[0].toUpperCase()}
                    </span>
                </div>
                <div class="min-w-0 flex-1 ml-4">
                    <p class="text-sm font-medium text-gray-900 dark:text-white">
                        ${event.title}
                    </p>
                    <p class="mt-1 text-sm text-gray-500 dark:text-gray-400 flex items-center">
                        <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        ${event.start_time} - ${event.end_time}
                    </p>
                </div>
            </div>
        `).join('');
    }

    updateSchedules(schedules) {
        const container = document.querySelector('#schedules-list');
        if (schedules.length === 0) {
            container.innerHTML = this.getEmptySchedulesHtml();
            return;
        }

        // Показываем только первые 4 графика
        const recentSchedules = schedules.slice(0, 4);

        container.innerHTML = recentSchedules.map(schedule => `
            <li class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-200">
                <div class="p-6">
                    <div class="flex items-center justify-between">
                        <div class="flex-1 min-w-0">
                            <div class="flex items-center justify-between">
                                <a href="/schedule/${schedule.id}/" 
                                   class="text-lg font-medium text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300">
                                    ${schedule.title}
                                </a>
                                <a href="/schedule/${schedule.id}/" 
                                   class="ml-2 inline-flex items-center px-3 py-1.5 text-sm font-medium text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300 border border-indigo-600 dark:border-indigo-400 rounded-lg hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-colors duration-200">
                                    Подробнее
                                </a>
                            </div>
                            <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                                ${schedule.description || ''}
                            </p>
                            <div class="mt-3 flex items-center space-x-4">
                                <span class="inline-flex items-center px-3 py-1 rounded-lg text-xs font-medium 
                                    ${this.getScheduleTypeColors(schedule.schedule_type)}">
                                    ${this.getScheduleTypeDisplay(schedule.schedule_type)}
                                </span>
                                <span class="text-sm text-gray-500 dark:text-gray-400 flex items-center">
                                    <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                    </svg>
                                    ${schedule.created_at}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </li>
        `).join('');

        // Если есть больше 4 графиков, добавляем ссылку "Показать все"
        if (schedules.length > 4) {
            container.innerHTML += `
                <li class="px-4 py-4 sm:px-6 bg-gray-50 dark:bg-gray-700/50">
                    <a href="/schedule/" 
                       class="text-sm font-medium text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300 flex items-center justify-center">
                        Показать все графики
                        <svg class="h-4 w-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        </svg>
                    </a>
                </li>
            `;
        }
    }

    getScheduleTypeColors(type) {
        const colors = {
            'weekly': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
            'single': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
            'flexible': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
        };
        return colors[type] || colors['weekly'];
    }

    getScheduleTypeDisplay(type) {
        const types = {
            'weekly': 'Недельный',
            'single': 'Однодневный',
            'flexible': 'Гибкий'
        };
        return types[type] || type;
    }

    getEmptySchedulesHtml() {
        return `
            <div class="text-center py-12">
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
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new Profile();
}); 