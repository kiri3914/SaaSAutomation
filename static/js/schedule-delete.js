class ScheduleDelete {
    constructor(scheduleId) {
        this.scheduleId = scheduleId;
        this.init();
    }

    init() {
        this.initDeleteForm();
    }

    initDeleteForm() {
        document.getElementById('delete-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.deleteSchedule();
        });
    }

    deleteSchedule() {
        const formData = new FormData(document.getElementById('delete-form'));
        
        fetch(`/api/schedule/${this.scheduleId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.notifications.show('График успешно удален', 'success');
                window.location.href = '/schedule/';
            } else {
                window.notifications.show('Ошибка при удалении графика', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            window.notifications.show('Ошибка при удалении графика', 'error');
        });
    }
} 