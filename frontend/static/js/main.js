define(["jquery", "highcharts", "socketio"], function($, Highcharts, io) {
  $(document).ready(function() {
    var chart = new Highcharts.Chart({
      chart: {
        zoomType: "xy",
        margin: [80, 80, 80, 80],
        renderTo: "container"
      },
      title: {
        text: "Steering & Throttle"
      },
      subtitle: {
        text: "Plotting the pulse widths from the RF receiver in real-time using websockets."
      },
      xAxis: {
        gridLineWidth: 5,
        maxZoom: 60
      },
      yAxis: [
        {
          title: {
            text: "Steering"
          },
          min: 1000,
          max: 2000,
          plotLines: [
            {
              value: 0,
              width: 1,
              colour: "#808800"
            }
          ]
        },
        {
          title: {
            text: "Throttle"
          },
          min: 1000,
          max: 2000,
          plotLines: [
            {
              value: 0,
              width: 1,
              colour: "#008888",
            }
          ],
          opposite: true
        }
      ],
      plotOptions: {
        column: {
          pointPadding: 0,
          groupPadding: 0
        }
      },
      series: [
        {
          name: "Steering",
          type: "spline",
          color: "#008800",
          yAxis: 0,
          data: []
        },
        {
          name: "Throttle",
          type: "spline",
          yAxis: 1,
          data: []
        }
      ]
    });

    var socket = io.connect(
      window.location.protocol + "//" + window.location.hostname
    );

    socket.on("steering", data => {
      var series = chart.series[0];
      series.addPoint([data.pulse_width_microseconds], true, series.data.length > 100);
    });
    socket.on("throttle", data => {
      var series = chart.series[1];
      series.addPoint([data.pulse_width_microseconds], true, series.data.length > 100);
    });
  });
});
