// Set new default font family and font color to mimic Bootstrap's default styling
    Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#858796';

    var myLineChart; // Global variable to hold the chart instance

    // Function to fetch data from the server
    function fetchData() {
      return fetch('data/')
        .then(response => response.json())
        .catch(error => {
          console.error('Error fetching data:', error);
          throw error; // Rethrow the error to handle it in the caller
        });
    }

    // Function to format numbers
    function numberFormat(number, decimals, decPoint, thousandsSep) {
      number = (number + '').replace(',', '').replace(' ', '');
      var n = !isFinite(+number) ? 0 : +number,
          prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
          sep = (typeof thousandsSep === 'undefined') ? ',' : thousandsSep,
          dec = (typeof decPoint === 'undefined') ? '.' : decPoint,
          s = '',
          toFixedFix = function (n, prec) {
            var k = Math.pow(10, prec);
            return '' + Math.round(n * k) / k;
          };
      // Fix for IE parseFloat(0.55).toFixed(0) = 0;
      s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
      if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
      }
      if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
      }
      return s.join(dec);
    }

    // Function to initialize the chart and fetch/update data
    function initializeChartWithData() {
      var ctx = document.getElementById("myAreaChart");
      myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            label: "Loans",
            lineTension: 0.3,
            backgroundColor: "rgba(78, 115, 223, 0.05)",
            borderColor: "rgba(78, 115, 223, 1)",
            pointRadius: 3,
            pointBackgroundColor: "rgba(78, 115, 223, 1)",
            pointBorderColor: "rgba(78, 115, 223, 1)",
            pointHoverRadius: 3,
            pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
            pointHoverBorderColor: "rgba(78, 115, 223, 1)",
            pointHitRadius: 10,
            pointBorderWidth: 2,
            data: [],
          }],
        },
        options: {
          maintainAspectRatio: false,
          layout: {
            padding: {
              left: 10,
              right: 25,
              top: 25,
              bottom: 0
            }
          },
          scales: {
            // ... existing chart scales ...

            yAxes: [{
              ticks: {
                maxTicksLimit: 5,
                padding: 10,
                // Include a dollar sign in the ticks
                callback: function (value, index, values) {
                  return 'KSH ' + numberFormat(value);
                }
              },
              gridLines: {
                color: "rgb(234, 236, 244)",
                zeroLineColor: "rgb(234, 236, 244)",
                drawBorder: false,
                borderDash: [2],
                zeroLineBorderDash: [2]
              }
            }],
          },
          legend: {
            display: false
          },
          tooltips: {
            // ... existing chart tooltips ...
          },
          // Call fetchDataAndUpdateChart function to fetch data and update the chart
          animation: {
            onComplete: fetchDataAndUpdateChart
          }
        }
      });
    }

    function fetchDataAndUpdateChart() {
      // Fetch data from the server
      fetchData()
        .then(data => {
          // Extract required data from the response
          const loanData = data.data; // Access the 'data' array

          // Extract 'amount' and 'date' values from loanData
          const amounts = loanData.map(loan => parseFloat(loan.amount));
          const dates = loanData.map(loan => loan.date);

          // Update the chart with the new data
          myLineChart.data.labels = dates;
          myLineChart.data.datasets[0].data = amounts;
          myLineChart.update();
        })
        .catch(error => {
          console.error('Error updating chart:', error);
        });
    }

    // Initialize the chart and fetch/update data
    initializeChartWithData();
