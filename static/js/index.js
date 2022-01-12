

var timeLeft = 15;
    var elem = document.getElementById('timer');
    
    var timerId = setInterval(countdown, 1000);
    
    function countdown() {
      if (timeLeft == -1) {
        clearTimeout(timerId);
        var withinTimer = document.getElementById('withinTimer');
        withinTimer.value = "false"
        doSomething();
      }
      else if (timeLeft < 6) {
        elem.style.background='red';
        elem.innerHTML = 'Time Left ' + timeLeft;
        timeLeft--;
      }
      else if (timeLeft < 11) {
        elem.style.background='pink';
        elem.innerHTML = 'Time Left ' + timeLeft;
        timeLeft--;
      }
       else {
        elem.innerHTML = 'Time Left ' + timeLeft;
        timeLeft--;
      }
    }