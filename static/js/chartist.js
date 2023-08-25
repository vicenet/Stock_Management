(function($) {
  'use strict';
  // ...

  // Line chart
  if ($('#ct-chart-line').length) {
    // Retrieve data from the Production model
    var productionData = JSON.parse('{{ production_data|safe }}');
    
    // Prepare the labels and series data from the productionData
    var labels = productionData.labels;
    var series = productionData.series;

    // Update the chart with the production data
    new Chartist.Line('#ct-chart-line', {
      labels: labels,
      series: series
    }, {
      fullWidth: true,
      chartPadding: {
        right: 40
      }
    });
  }

  // ...

})(jQuery);
