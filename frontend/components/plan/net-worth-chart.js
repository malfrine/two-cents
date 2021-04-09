import { Line, mixins } from 'vue-chartjs'

export default {
  extends: Line,
  mounted () {
    this.renderChart(this.chartData, this.options)
  },
  mixins: [mixins.reactiveProp],
  data () {
    return {
      options: {
        responsive: true,
        maintainAspectRatio: false,
        aspectRatio: 1,
        hover: {
          mode: true
        },
        scales: {
          yAxes: [{
            stacked: true,
            scaleLabel: {
              display: true,
              labelString: 'Value ($)'
            },
            gridLines: {
              display: true
            }
          }],
          xAxes: [{
            type: 'time',
            time: {
              unit: 'month'
            },
            gridLines: {
              display: false
            }
          }]
        }
      }
    }
  }
}
