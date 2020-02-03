<!-- Visualize BG data -->
<!-- Used in Live BG and historical BG (TODO) -->
<!-- Props: pastData -->

<template>
	<div id='vis-container'>
		<div id="vis">

	</div>
	
	</div>
</template>

<script>
	export default {
		name : 'glucose-vis',

		props: {
			pastData: Array,
			forecastData: Array,
			data: Array
		},
		watch: {
			data: function(newVal) {
				if (newVal.length > 0) {
					this.plotGlucose()
				}
			}
		},

		methods: {
			plotGlucose() {

				// var vlSpec = {
				// 	$schema: 'https://vega.github.io/schema/vega-lite/v4.json',
				// 	data: {values: this.$props.pastData},
				// 	width: 'container',
				// 	height: 'container',
				// 	layer: [
				// 	{
				// 		data: {"values": [{"Glucose": 0}, {'Glucose' : 70}]},
				// 		mark: 'rect',
				// 		encoding: {
				// 			y: {aggregate: 'max', field: 'Glucose', type: 'quantitative'},
				// 			y2: {aggregate: 'min', field: 'Glucose', type: 'quantitative'},
				// 			opacity: {value: 0.2},
				// 			color: {value: "#d45d79"}
				// 		}
				// 	},
				// 	{
				// 		data: {"values": [{"Glucose": 70}]},
				// 		mark: 'rule',
				// 		encoding: {
				// 			y: {field: 'Glucose', type: 'quantitative'},
				// 			color: {value: "#d45d79"},
				// 			size: {value: 1}
				// 		}
				// 	},
				// 	{
				// 		mark: 'point',
				// 		encoding: {
				// 			y: {field: 'Glucose', type: 'quantitative', 
				// 				axis: {title: 'Glucose (mg/dL)'}},
				// 			x: {field: 'Timestamp', type: 'temporal',axis: {title: 'Time'}},
				// 			size: {value: 15},
				// 			color: {value: 'grey'}
				// 		}
				// 	},
				// 	{
				// 		data: {values: this.$props.forecastData},
				// 		mark: {type : 'point', filled : "true"},
				// 		encoding: {
				// 			y: {field: 'Glucose', type: 'quantitative'},
				// 			x: {field: 'Timestamp', type: 'temporal',axis: {title: 'Time'}},
				// 			size: {value: 45},
				// 			color: {value: '#ea9085'}
				// 		}
				// 	},
				// 	],
				// };



				const vegaSpec = {
  $schema: "https://vega.github.io/schema/vega/v5.json",
  width: 700,
  height: 400,
  padding: 5,
  background: "white",

  config: {
    axisBand: {
      bandPosition: 0,
      labelPadding: 7,
      tickExtra: false
    }
  },

  signals: [
    {
      name: "tipYear",
      on: [{
        events: "@cell:mouseover",
        update: "datum.forecastTime"
      }]
    },
    {
      name: "tipValue",
      on: [{
        events: "@cell:mouseover",
        update: "datum.glucose"
      }]
    }
  ],

  data: [
    {
      name: "colors",
      values : [{type : "measured", color : "grey"},
        {type : "forecasted", color : "#ea9085"}]
    },
    {
      name: "bg-levels",
      values: this.$props.data,
      transform: [
        {type: "extent",
        field: "forecastTime",
        signal: "extentForecast"
        },
        {type: "extent",
        field: "actualTime",
        signal: "extentActual"
        },
        { type: "filter", expr: "datum.actualTime >= (extentActual[1] - 36000000)" }
      ]
    },
    {
      name: "bg-actual",
      source: "bg-levels",
      transform: [
        {type: "filter", expr: "datum.forecastTime == datum.actualTime" },
        // {type: "formula", expr: "scale('x', datum.forecastTime)", as: "xcoord"},
        // {type: "formula", expr: "scale('y', datum.glucose)", as: "ycoord"},
        // {type: "voronoi", x: "xcoord", y: "ycoord", as: "cell", size: [{signal: "width"}, {signal: "height"}]}
     ]
    },
    {
      name: "tooltip",
      source: "bg-actual",
      transform: [
        {
          type: "filter",
          expr: "datum.forecastTime == tipYear && abs(datum.glucose - tipValue) <= 5"
        },
        {
          type: "aggregate",
          fields: ["glucose", "glucose"],
          ops: ["min", "argmin"],
          as: ["min", "argmin"]
        },
        { type: "formula", as: "tooltipYear", expr: "datum.argmin.actualTime" }
      ]
    },
    {
      name: "tooltip-forecast",
      source: "bg-levels",
      transform: [
        {
          type: "lookup",
          from: "tooltip", key: "tooltipYear",
          fields: ["actualTime"], as: ["tooltip"]
        },
        { type: "filter", expr: "datum.tooltip" }
      ]
    },
    {
      name: "latest-forecast",
      source: "bg-levels",
      transform: [
        { type: "filter", expr: "datum.actualTime >= extentActual[1]" }
      ]
    }
  ],

  scales: [
	{
      name: "x",
      type: "time",
      domain: {
        fields: [
          {data: "bg-levels", field: "forecastTime"}
        ]
      },
      "range": [0, {signal: "width"}]
    },


    {
      name: "y",
      type: "linear", zero: true,
      domain: {data: "bg-levels", field: "glucose"},
      range: "height"
    },
    {
      name: "color",
      type: "ordinal",
      domain: {data: "colors", field: "type"},
      range: {data: "colors", field: "color"}
    }
  ],

  axes: [
    {
      orient: "bottom", scale: "x",
      grid: true, domain: true,
      tickSize: 5, title: "Time",
      encode: {
        grid: {
          enter: {
            stroke: {value: "#f2f2f2"},
            strokeOpacity: {value: 0.75}
          }
        }
      }
    },
    {
      orient: "left", scale: "y",
      grid: true, "domain": true,
      tickSize: 8, title : "Glucose level (mg/dL)",
      encode: {
        grid: {
          enter: {
            stroke: {value: "#f2f2f2"},
            strokeOpacity: {value: 0.75}
          }
        }
      }
    }
  ],
  legends: [
    {
      stroke: "color",
      title: "",
      padding: 4,
      encode: {
        symbols: {
          enter: {
            strokeWidth: {value: 2},
            size: {value: 50}
          }
        }
      }
    }
  ],

  marks: [
    {
      type: "rule",
      encode: {
        enter: {
          y: {scale: "y", value: 70},
          stroke: {value: "#ea9085"},
          strokeWidth: {value: 2},
          x: {value: 0},
          x2: {field: {group: "width"}}
        }
      }
    },
    {
      type: "symbol",
      from: {data: "latest-forecast"},
      encode: {
        update: {
          x: {scale: "x", field: "forecastTime"},
          y: {scale: "y", field: "glucose"},
          fill: {value: "#ea9085"},
          stroke: {value: 'grey'},
          strokeWidth: {value: 1},
          size: {value: 75}
        }
      }
    },
    {
      type: "symbol",
      from: {data: "tooltip-forecast"},
      encode: {
        update: {
          x: {scale: "x", field: "forecastTime"},
          y: {scale: "y", field: "glucose"},
          fill: {value: "#ea9085"},
          stroke: {value: "grey"},
          strokeWidth: {value: 1}
        }
      }
    },
    {
      name: "actual",
      type: "symbol",
      from: {"data": "bg-actual"},
      encode: {
        update: {
          x: {scale: "x", field: "forecastTime"},
          y: {scale: "y", field: "glucose"},
          stroke: {value: "grey"},
          strokeWidth: {value: 2},
        }
      }
    },

    // {
    //   "type": "path",
    //   "name": "cell",
    //   "from": {"data": "bg-actual"},
    //   "encode": {
    //     "enter": {
    //       "fill": {"value": "transparent"},
    //       "strokeWidth": {"value": 0.35},
    //       "stroke": {"value": "transparent"},
    //       "path": {"field": "cell"}
    //     }
    //   }
    // }
    {
      name: "cell",
      type: "symbol",
      from: {"data": "bg-actual"},
      encode: {
        update: {
          x: {scale: "x", field: "forecastTime"},
          y: {scale: "y", field: "glucose"},
          fill: {value: "transparent"},
          opacity: {value: 0.5},
          strokeWidth: {value: 2},
          size: {value: 500}
        }
      }
    }
  ]
}

			// Embed the visualization in the container with id `vis`
			window.vegaEmbed('#vis', vegaSpec, {renderer: 'svg'}).then((result) => (window.vegaView = result.view));
		},
	},
}


</script>

<style scoped>
#vis {
	width: 70%;
	height: 300px;
}
#vis-container {
	padding-bottom: 20px;
}
</style>