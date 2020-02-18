<!-- Visualize BG data -->
<!-- Visualize glucose and predicted glucose data -->
<!-- Props: data - updated after each glucose-form submission -->

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

        // Vega plot specification
				const vegaSpec = {
  $schema: "https://vega.github.io/schema/vega/v5.json",
  width: 700,
  height: 300,
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
        },
        labels: {
          enter: {
            fontSize: {value: 15},
            dy: {value: 6}
          }
        },
        title: {
          enter: {
            fontSize: {value: 18},
            dy: {value: 5}
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
        },
        labels: {
          enter: {
            fontSize: {value: 15},
            dx: {value: -6}
          }
        },
        title: {
          enter: {
            fontSize: {value: 18},
            dx: {value: -7}
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
        },
        labels: {
          enter: {
            fontSize: {value: 15}
          }
        },
        title: {
          enter: {
            fontSize: {value: 18}
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
    },
    {
      type: "text",
      encode: {
        enter: {
          fontSize: {value: 16},
        },
        update: {
          x: {scale: 'x', signal: 'tipYear'},
          y : {scale: 'y', signal: 'tipValue'},
          dy: {value: -30},
          dx: {value: -20},
          text: {signal: "tipValue"}
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
  marig: auto auto;
}
#vis-container {
	padding-bottom: 20px;
}
</style>