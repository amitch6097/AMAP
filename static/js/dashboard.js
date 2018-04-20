(function($) {
  'use strict';
  $(function() {
    var data = {
      labels: [document.getElementById('T0').innertext, document.getElementById('T1').innertext, document.getElementById('T2').innertext, document.getElementById('T3').innertext, document.getElementById('T4').innertext, document.getElementById('T5').innertext],
      datasets: [{
        label: 'Malware Samples',
        data: [parseInt(document.getElementById('C1V0').innertext), parseInt(document.getElementById('C1V1').innertext), parseInt(document.getElementById('C1V2').innertext), parseInt(document.getElementById('C1V3').innertext), parseInt(document.getElementById('C1V4').innertext), parseInt(document.getElementById('C1V5').innertext)],
        backgroundColor: [
          'rgba(54, 162, 235, 0.5)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
          'rgba(54, 162, 235, 0.5)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1
      }]
    };
    var data2 = {
      labels: [document.getElementById('T0').innertext, document.getElementById('T1').innertext, document.getElementById('T2').innertext, document.getElementById('T3').innertext, document.getElementById('T4').innertext, document.getElementById('T5').innertext],
      datasets: [{
        label: 'Malware Samples',
        data: [parseInt(document.getElementById('C2V0').innertext), parseInt(document.getElementById('C2V1').innertext), parseInt(document.getElementById('C2V2').innertext), parseInt(document.getElementById('C2V3').innertext), parseInt(document.getElementById('C2V4').innertext), parseInt(document.getElementById('C2V5').innertext)],
        backgroundColor: [
          'rgba(54, 162, 235, 0.5)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
          'rgba(54, 162, 235, 0.5)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1
      }]
    };

    var options = {
      animation:{
        duration: 0
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      },
      legend: {
        display: false
      },
      elements: {
        point: {
          radius: 0
        }
      }

    };
    var doughnutPieData = {
      datasets: [{
        data: [parseInt(document.getElementById('PI1').innertext), parseInt(document.getElementById('PI2').innertext)],
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)',
          'rgba(153, 102, 255, 0.5)',
          'rgba(255, 159, 64, 0.5)'
        ],
        borderColor: [
          'rgba(255,99,132,1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
        ],
      }],

      // These labels appear in the legend and in the tooltips when hovering different arcs
      labels: [
        'Windows Executable',
        'Other',
      ]
    };
    var doughnutPieOptions = {
      responsive: true,
      animation: {
        duration: 0,
        animateScale: true,
        animateRotate: false
      }
    };
    if ($("#sales-chart").length) {
      var ctx = document.getElementById('sales-chart').getContext("2d");

      var gradientStroke1 = ctx.createLinearGradient(0, 0, 0, 300);
      gradientStroke1.addColorStop(0, 'rgba(83, 227 ,218, 0.9)');
      gradientStroke1.addColorStop(1, 'rgba(45, 180 ,235, 0.9)');

      var gradientStroke2 = ctx.createLinearGradient(0, 0, 0, 300);
      gradientStroke2.addColorStop(0, 'rgba(132, 179 ,247, 0.9)');
      gradientStroke2.addColorStop(1, 'rgba(164, 90 ,249, 0.9)');

      var myChart = new Chart(ctx, {
          type: 'line',
          data: {
              labels: [1, 2, 3, 4, 5, 6, 7, 8],
              datasets: [
                {
                  label: "Audi",
                  borderColor: gradientStroke2,
                  backgroundColor: gradientStroke2,
                  pointRadius: 0,
                  fill: false,
                  borderWidth: 1,
                  fill: 'origin',
                  data: [0, 30, 60, 25, 60, 25, 50, 0]
                },
                {
                  label: "BMW",
                  borderColor: gradientStroke1,
                  borderColor: gradientStroke1,
                  backgroundColor: gradientStroke1,
                  pointRadius: 0,
                  fill: false,
                  borderWidth: 1,
                  fill: 'origin',
                  data: [0, 60, 25, 80, 35, 75, 30, 0]
                }
            ]
          },
          options: {
              legend: {
                  position: "top"
              },
              scales: {
                xAxes: [{
                  ticks: {
                    display: true,
                    beginAtZero:true,
                    fontColor: 'rgba(0, 0, 0, 1)'
                  },
                  gridLines: {
                    display:false,
                    drawBorder: false,
                    color: 'transparent',
                    zeroLineColor: '#eeeeee'
                  }
                }],
                yAxes: [{
                  gridLines: {
                    drawBorder: false,
                    display:true,
                    color: '#eeeeee',
                  },
                  categoryPercentage: 0.5,
                  ticks: {
                    display: true,
                    beginAtZero: true,
                    stepSize: 20,
                    max: 100,
                    fontColor: 'rgba(0, 0, 0, 1)'
                  }
                }]
              },
              },
              elements: {
                point: {
                  radius: 0
                }
              }
            })
    }
    if ($("#doughnutChart").length) {
    //   var doughnutChartCanvas = $("#doughnutChart").get(0).getContext("2d");
    //   var doughnutChart = new Chart(doughnutChartCanvas, {
    //     type: 'bar',
    //     data: doughnutPieData,
    //     options: doughnutPieOptions
    //   });
    // }
	var ctx = document.getElementById("doughnutChart");
	var myLineChart = new Chart(ctx, {
	  type: 'bar',
	  data: {
	    labels: ["0","1", "2", "3", "4"],
	    datasets: [{
	      label: "Amount",
	      backgroundColor: "rgba(2,117,216,1)",
	      borderColor: "rgba(2,117,216,1)",
	      data: [1,2,3,4,5]
	    }],
	  },
	  options: {
	    scales: {
	      xAxes: [{
	        time: {
	          unit: 'amount'
	        },
	        gridLines: {
	          display: false
	        },
	        ticks: {
	          maxTicksLimit: 6
	        }
	      }],
	      yAxes: [{
	        ticks: {
	          min: 0,
	          max: 10,
	          maxTicksLimit: 5
	        },
	        gridLines: {
	          display: true
	        }
	      }],
	    },
	    legend: {
	      display: false
	    }
	  }
	});
}
    if ($("#lineChart").length) {
      var lineChartCanvas = $("#lineChart").get(0).getContext("2d");
      var lineChart = new Chart(lineChartCanvas, {
        type: 'line',
        data: data,
        options: options
      });
    }
    if ($("#lineChart2").length) {
      var lineChartCanvas = $("#lineChart2").get(0).getContext("2d");
      var lineChart = new Chart(lineChartCanvas, {
        type: 'line',
        data: data2,
        options: options
      });
    }
    if ($("#satisfaction-chart2").length) {
      var ctx = document.getElementById('satisfaction-chart2').getContext("2d");

      var gradientStrokeBluePurple = ctx.createLinearGradient(0, 0, 0, 250);
      gradientStrokeBluePurple.addColorStop(0, '#5607fb');
      gradientStrokeBluePurple.addColorStop(1, '#9425eb');
      var myChart = new Chart(ctx, {
          type: 'bar',
          data: {
              labels: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
              datasets: [
                {
                  label: "Audi",
                  borderColor: gradientStrokeBluePurple,
                  backgroundColor: gradientStrokeBluePurple,
                  hoverBackgroundColor: gradientStrokeBluePurple,
                  pointRadius: 0,
                  fill: false,
                  borderWidth: 1,
                  fill: 'origin',
                  data: [50, 45, 25, 72, 40, 10, 15, 10, 20, 56, 30, 50, 99, 45, 37, 33]
                }
            ]
          },
          options: {
              legend: {
                  display: false
              },
              scales: {
                  yAxes: [{
                      ticks: {
                          display: false,
                          min: 0,
                          stepSize: 10
                      },
                      gridLines: {
                        drawBorder: false,
                        display: true
                      }
                  }],
                  xAxes: [{
                      gridLines: {
                        display:false,
                        drawBorder: false,
                        color: 'rgba(0,0,0,1)',
                        zeroLineColor: '#eeeeee'
                      },
                      ticks: {
                          padding: 20,
                          fontColor: "rgba(0,0,0,1)",
                          autoSkip: true,
                          maxTicksLimit: 6
                      },
                      barPercentage: 0.7
                  }]
                }
              },
              elements: {
                point: {
                  radius: 0
                }
              }
            })
    }
    if ($("#satisfaction-chart").length) {
      var ctx = document.getElementById('satisfaction-chart').getContext("2d");

      var gradientStrokeBluePurple = ctx.createLinearGradient(0, 0, 0, 250);
      gradientStrokeBluePurple.addColorStop(0, '#5607fb');
      gradientStrokeBluePurple.addColorStop(1, '#9425eb');
      var myChart = new Chart(ctx, {
          type: 'bar',
          data: {
              labels: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
              datasets: [
                {
                  label: "Audi",
                  borderColor: gradientStrokeBluePurple,
                  backgroundColor: gradientStrokeBluePurple,
                  hoverBackgroundColor: gradientStrokeBluePurple,
                  pointRadius: 0,
                  fill: false,
                  borderWidth: 1,
                  fill: 'origin',
                  data: [50, 45, 25, 35, 40, 25, 15, 40, 20, 15, 30, 50, 26, 45, 37, 26]
                }
            ]
          },
          options: {
              legend: {
                  display: false
              },
              scales: {
                  yAxes: [{
                      ticks: {
                          display: false,
                          min: 0,
                          stepSize: 10
                      },
                      gridLines: {
                        drawBorder: false,
                        display: true
                      }
                  }],
                  xAxes: [{
                      gridLines: {
                        display:false,
                        drawBorder: false,
                        color: 'rgba(0,0,0,1)',
                        zeroLineColor: '#eeeeee'
                      },
                      ticks: {
                          padding: 20,
                          fontColor: "rgba(0,0,0,1)",
                          autoSkip: true,
                          maxTicksLimit: 6
                      },
                      barPercentage: 0.7
                  }]
                }
              },
              elements: {
                point: {
                  radius: 0
                }
              }
            })
    }
  });
})(jQuery);
