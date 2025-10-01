class ScheduleUtils {
    static getScheduleTypeDisplay(type) {
        switch(type) {
            case 'weekly':
                return 'Еженедельный';
            case 'single':
                return 'Однодневный';
            case 'flexible':
                return 'Гибкий';
            default:
                return type;
        }
    }

    static formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    static getTypeColors(type) {
        switch(type) {
            case 'weekly':
                return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
            case 'single':
                return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
            case 'flexible':
                return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200';
            default:
                return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
        }
    }
} 