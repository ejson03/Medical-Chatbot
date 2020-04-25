$(function () {

    'use strict';
    (function () {
    
      var aside = $('.side-nav'),
    
          showAsideBtn = $('.show-side-btn'),
    
          contents = $('#contents');
    
      showAsideBtn.on("click", function () {
    
        $("#" + $(this).data('show')).toggleClass('show-side-nav');
    
        contents.toggleClass('margin');
    
      });
    
      if ($(window).width() <= 767) {
    
        aside.addClass('show-side-nav');
    
      }
      $(window).on('resize', function () {
    
        if ($(window).width() > 767) {
    
          aside.removeClass('show-side-nav');
    
        }
    
      });
    
      var slideNavDropdown = $('.side-nav-dropdown');
    
      $('.side-nav .categories li').on('click', function () {
    
        $(this).toggleClass('opend').siblings().removeClass('opend');
    
        if ($(this).hasClass('opend')) {
    
          $(this).find('.side-nav-dropdown').slideToggle('fast');
    
          $(this).siblings().find('.side-nav-dropdown').slideUp('fast');
    
        } else {
    
          $(this).find('.side-nav-dropdown').slideUp('fast');
    
        }
    
      });
    
      $('.side-nav .close-aside').on('click', function () {
    
        $('#' + $(this).data('close')).addClass('show-side-nav');
    
        contents.removeClass('margin');
    
      });
    
    }());

    (function () {
      async function getUsers()  {
        
        var response = await fetch('/users');
        var users = await response.json();
        return users
      }
      getUsers().then(data => {
        let list = document.getElementById("users")
        console.log(data);
        data['users'].forEach((user => {
          let li = document.createElement('li')
          let a = document.createElement('a')
          a.href = `/users/${user}`
          a.innerHTML = user.charAt(0).toUpperCase() + user.slice(1)
          li.appendChild(a)
          list.appendChild(li)
        }));
      })
      
    }());
    
    
    var chart = document.getElementById('myChart');
    Chart.defaults.global.animation.duration = 2000; // Animation duration
    Chart.defaults.global.title.display = false; // Remove title
    Chart.defaults.global.title.text = "Chart"; // Title
    Chart.defaults.global.title.position = 'bottom'; // Title position
    Chart.defaults.global.defaultFontColor = '#999'; // Font color
    Chart.defaults.global.defaultFontSize = 10; // Font size for every label
    
    Chart.defaults.global.tooltips.backgroundColor = '#FFF'; // Tooltips background color
    Chart.defaults.global.tooltips.borderColor = 'white'; // Tooltips border color
    Chart.defaults.global.legend.labels.padding = 0;
    Chart.defaults.scale.ticks.beginAtZero = true;
    Chart.defaults.scale.gridLines.zeroLineColor = 'rgba(255, 255, 255, 0.1)';
    Chart.defaults.scale.gridLines.color = 'rgba(255, 255, 255, 0.02)';
    
    Chart.defaults.global.legend.display = false;


    function createChart(data){
      let happy = []
      let sad = []
      let angry = []
      let date = []
      let emotion = []
      console.log(data)
      data.forEach(stuff => {
        if(stuff['emotion'] == 'happy'){
          happy.push(10)

        }
        else{
          happy.push(3)
        }
        if(stuff['emotion'] == 'sad'){
          sad.push(8)
        }
        else{
          sad.push(3)
        }
        if(stuff['emotion'] == 'angry'){
          angry.push(6)
        }
        else{
          angry.push(3)
        }
        emotion.push(stuff['emotion'])
        date.push(stuff['time'])
      })
      var count = {};
      emotion.forEach(inst => count[inst] = (count[inst] || 0) +1);

      new Chart(document.getElementById("line"), {
        type: 'line',
        data: {
          labels: date,
          datasets: [{ 
              data: happy,
              label: "Happy",
              borderColor: "#3e95cd",
              fill: false
            }, { 
              data: sad,
              label: "Sad",
              borderColor: "#8e5ea2",
              fill: false
            }, { 
              data: angry,
              label: "Angry",
              borderColor: "#3cba9f",
              fill: false
            }

          ]
        },
        options: {
          title: {
            display: true,
            text: 'Emotion Analysis',
            fontSize: 15
          },
          legend: {
            display: true,
            position: 'top',
            labels: {
              padding: 10,
              fontSize: 15,
              fontColor: "#ffffff",
            }
          }
        }
      });

      new Chart(document.getElementById("pie"), {
        type: 'pie',
        data: {
          labels: Object.keys(count),
          datasets: [{
            label: "Emotion",
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
            data: Object.values(count)
          }]
        },
        options: {
          title: {
            display: true,
            text: 'Perecentage emotion this week'
          },
          legend: {
            display: true,
            position: 'bottom',
            labels: {
              padding: 10,
              fontSize: 15,
              fontColor: "#ffffff",
            }
          }
        }
    });

    new Chart(document.getElementById("bar-chart"), {
      type: 'bar',
      data: {
        labels: Object.keys(count),
        datasets: [
          {
            label: "Emotion",
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
            data: Object.values(count)
          }
        ]
      },
      options: {
        title: {
          display: true,
          text: 'Perecentage emotion this week'
        },
        legend: {
          display: true,
          position: 'bottom',
          labels: {
            padding: 10,
            fontSize: 15,
            fontColor: "#ffffff",
          }
        }
      }
  });

  var x = document.getElementById("hidden_div");
    x.style.display = "block";

      
    }

    $('#formid').submit(function(e) {
      e.preventDefault();
      $.ajax({
          url: '/report',
          data: $(this).serialize(),
          type: 'POST',
          success: function(data) {
              createChart(data['name']);
          }
      });
  });
   


    
    
     
    
});
