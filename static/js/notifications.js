class NotificationManager {
    constructor() {
        this.container = this.createContainer();
    }

    createContainer() {
        const container = document.createElement('div');
        container.id = 'notification-container';
        container.className = 'fixed bottom-4 right-4 z-50 space-y-2';
        document.body.appendChild(container);
        return container;
    }

    show(message, type = 'success') {
        const colors = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            warning: 'bg-yellow-500',
            info: 'bg-blue-500'
        };

        const notification = document.createElement('div');
        notification.className = `${colors[type]} text-white px-6 py-4 rounded-lg shadow-lg transform transition-all duration-500 opacity-0 translate-x-full`;
        notification.innerHTML = `
            <div class="flex items-center space-x-3">
                <div class="flex-1">${message}</div>
                <button class="focus:outline-none">
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                </button>
            </div>
        `;

        this.container.appendChild(notification);

        // Анимация появления
        setTimeout(() => {
            notification.classList.remove('opacity-0', 'translate-x-full');
        }, 100);

        // Автоматическое скрытие через 5 секунд
        setTimeout(() => {
            this.hide(notification);
        }, 5000);

        // Обработчик клика по кнопке закрытия
        notification.querySelector('button').addEventListener('click', () => {
            this.hide(notification);
        });
    }

    hide(notification) {
        notification.classList.add('opacity-0', 'translate-x-full');
        setTimeout(() => {
            notification.remove();
        }, 500);
    }
}

window.notifications = new NotificationManager(); 