
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {          
        locale: 'pt-br',
    dateClick: function() {
alert('a day has been clicked!');
}
    });
    calendar.render();
});
  
