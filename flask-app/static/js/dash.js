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
    
    var email_list =[]
    var count_list =[]
    var email_s_list =[]
    var email_h_list =[]
    var spam_list=[]
    var ham_list=[]
    var time_list=[]

    function createChart(data){
      let emotion = []
      let date = []
      console.log(data)
      data.forEach(stuff => {
        emotion.push(stuff['emotion']);
        date.push(stuff['time'])
      })
      console.log(emotion, date)
      var chart = document.getElementById('myChart');
      var myChart = new Chart(chart, {
        type: 'line',
        data: {
          labels: [1500,1600,1700,1750,1800,1850,1900,1950,1999,2050],
          datasets: [{ 
              data: [86,114,106,106,107,111,133,221,783,2478],
              label: "Africa",
              borderColor: "#3e95cd",
              fill: false
            }, { 
              data: [282,350,411,502,635,809,947,1402,3700,5267],
              label: "Asia",
              borderColor: "#8e5ea2",
              fill: false
            }, { 
              data: [168,170,178,190,203,276,408,547,675,734],
              label: "Europe",
              borderColor: "#3cba9f",
              fill: false
            }, { 
              data: [40,20,10,16,24,38,74,167,508,784],
              label: "Latin America",
              borderColor: "#e8c3b9",
              fill: false
            }, { 
              data: [6,3,2,2,7,26,82,172,312,433],
              label: "North America",
              borderColor: "#c45850",
              fill: false
            }
          ]
        },
        options: {
          title: {
            display: true,
            text: 'World population per region (in millions)'
          }
        }
      });
      
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
