class ScheduleEditor {
    constructor(formId, scheduleType) {
        this.formId = formId;
        this.scheduleType = scheduleType;
        this.scheduleId = window.SCHEDULE_ID;
        this.init();
    }

    init() {
        this.loadScheduleData();
        this.initFormSubmit();
    }

    loadScheduleData() {
        fetch(`/api/schedule/${this.scheduleId}/`)
            .then(response => response.json())
            .then(data => {
                this.fillFormData(data);
            })
            .catch(error => {
                console.error('Error:', error);
                window.notifications.show('Ошибка при загрузке данных графика', 'error');
            });
    }

    fillFormData(data) {
        document.getElementById('title').value = data.title;
        document.getElementById('description').value = data.description || '';
        
        switch(this.scheduleType) {
            case 'weekly':
                this.fillWeeklyData(data.weekly_schedules);
                break;
            case 'single':
                this.fillSingleData(data.single_day_schedule);
                break;
            case 'flexible':
                this.fillFlexibleData(data.flexible_schedule);
                break;
        }
    }

    fillWeeklyData(weeklySchedules) {
        if (weeklySchedules?.length > 0) {
            weeklySchedules.forEach(ws => this.addWeeklySlot(ws));
        } else {
            this.addWeeklySlot();
        }
    }

    fillSingleData(singleSchedule) {
        if (singleSchedule) {
            document.getElementById('date').value = singleSchedule.date;
            document.getElementById('start_time').value = singleSchedule.start_time;
            document.getElementById('end_time').value = singleSchedule.end_time;
        }
    }

    fillFlexibleData(flexibleSchedule) {
        if (flexibleSchedule) {
            document.getElementById('repeat_type').value = flexibleSchedule.repeat_type;
            document.getElementById('repeat_interval').value = flexibleSchedule.repeat_interval;
            document.getElementById('start_date').value = flexibleSchedule.start_date;
            document.getElementById('end_date').value = flexibleSchedule.end_date;
            document.getElementById('start_time').value = flexibleSchedule.start_time;
            document.getElementById('end_time').value = flexibleSchedule.end_time;
        }
    }

    initFormSubmit() {
        document.getElementById(this.formId).addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveSchedule(e.target);
        });
    }

    saveSchedule(form) {
        const formData = new FormData(form);
        const scheduleData = this.prepareScheduleData(formData);

        fetch('/api/schedule/save/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            },
            body: JSON.stringify(scheduleData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.notifications.show('График успешно сохранен', 'success');
                window.location.href = `/schedule/${this.scheduleId}/`;
            } else {
                window.notifications.show('Ошибка при сохранении графика', 'error');
                console.error(data.errors);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            window.notifications.show('Ошибка при сохранении графика', 'error');
        });
    }

    prepareScheduleData(formData) {
        const baseData = {
            id: this.scheduleId,
            title: formData.get('title'),
            description: formData.get('description'),
            schedule_type: this.scheduleType
        };

        switch(this.scheduleType) {
            case 'weekly':
                return {
                    ...baseData,
                    weekly_schedules: Array.from(document.querySelectorAll('.weekly-slot')).map(slot => ({
                        weekday: slot.querySelector('[name="weekday[]"]').value,
                        start_time: slot.querySelector('[name="start_time[]"]').value,
                        end_time: slot.querySelector('[name="end_time[]"]').value
                    }))
                };
            case 'single':
                return {
                    ...baseData,
                    single_day_schedule: {
                        date: formData.get('date'),
                        start_time: formData.get('start_time'),
                        end_time: formData.get('end_time')
                    }
                };
            case 'flexible':
                return {
                    ...baseData,
                    flexible_schedule: {
                        repeat_type: formData.get('repeat_type'),
                        repeat_interval: formData.get('repeat_interval'),
                        start_date: formData.get('start_date'),
                        end_date: formData.get('end_date'),
                        start_time: formData.get('start_time'),
                        end_time: formData.get('end_time')
                    }
                };
        }
    }
} 