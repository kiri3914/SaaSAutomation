class ThemeManager {
    constructor() {
        this.init();
    }

    init() {
        // Проверяем сохраненную тему или системные настройки
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }

        // Добавляем обработчик для кнопки переключения темы
        document.addEventListener('DOMContentLoaded', () => {
            const themeToggle = document.getElementById('theme-toggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', () => this.toggleTheme());
            }

            // Инициализируем Flatpickr с темной темой если нужно
            if (document.documentElement.classList.contains('dark')) {
                this.updateFlatpickrTheme(true);
            }
        });

        // Добавляем слушатель изменения системной темы
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (!('theme' in localStorage)) {
                if (e.matches) {
                    document.documentElement.classList.add('dark');
                    this.updateFlatpickrTheme(true);
                } else {
                    document.documentElement.classList.remove('dark');
                    this.updateFlatpickrTheme(false);
                }
            }
        });
    }

    toggleTheme() {
        const isDark = document.documentElement.classList.contains('dark');
        if (isDark) {
            document.documentElement.classList.remove('dark');
            localStorage.theme = 'light';
        } else {
            document.documentElement.classList.add('dark');
            localStorage.theme = 'dark';
        }

        // Обновляем тему для Flatpickr
        this.updateFlatpickrTheme(!isDark);

        // Обновляем календарь, если он есть на странице
        if (window.calendar) {
            window.calendar.render();
        }
    }

    updateFlatpickrTheme(isDark) {
        // Обновляем тему для всех инстансов Flatpickr
        if (window.flatpickr) {
            const fpInputs = document.querySelectorAll('.flatpickr-input');
            fpInputs.forEach(input => {
                const fp = input._flatpickr;
                if (fp) {
                    if (isDark) {
                        fp.calendarContainer.classList.add('dark');
                    } else {
                        fp.calendarContainer.classList.remove('dark');
                    }
                }
            });
        }
    }
}

// Инициализируем менеджер темы
new ThemeManager(); 