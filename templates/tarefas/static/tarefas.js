document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {          
        locale: 'pt-br',
        events: '#',        
    dateClick: function() {
alert('a day has been clicked!');
}
    });
    calendar.render();

});