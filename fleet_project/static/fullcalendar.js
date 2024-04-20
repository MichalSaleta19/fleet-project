document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        // Dodaj inne opcje konfiguracyjne, jeśli są potrzebne
    });

    calendar.render();
});