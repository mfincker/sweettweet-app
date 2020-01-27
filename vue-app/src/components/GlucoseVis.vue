<!-- Visualize BG data -->
<!-- Used in Live BG and historical BG (TODO) -->
<!-- Props: pastData -->

<template>
	<div id="vis">
	</div>
</template>

<script>
	export default {
		name : 'glucose-vis',

		props: {
			pastData: Array,
			forecastData: Array,
		},
		watch: {
			pastData: function(newVal) {
				if (newVal.length > 0) {
					this.plotGlucose()
				}
			}
		},

		methods: {
			plotGlucose() {
			// 	var vlSpec = {
			// 		$schema: 'https://vega.github.io/schema/vega-lite/v4.json',
			// 		data: {values: this.$props.pastData},
			// 		width: 'container',
			// 		mark: 'point',
			// 		encoding: {
			// 			y: {field: 'Glucose', type: 'quantitative'},
			// 			x: {field: 'Timestamp', type: 'temporal',axis: {title: 'Glucose levels'}
			// 		}
			// 	}
			// };

				var vlSpec = {
					$schema: 'https://vega.github.io/schema/vega-lite/v4.json',
					data: {values: this.$props.pastData},
					width: 'container',
					height: 'container',
					layer: [
					{
						data: {"values": [{"Glucose": 70}]},
						mark: 'rule',
						encoding: {
							y: {field: 'Glucose', type: 'quantitative'},
							color: {value: "black"},
							size: {value: 1}
						}
					},
					{
						mark: 'point',
						encoding: {
							y: {field: 'Glucose', type: 'quantitative'},
							x: {field: 'Timestamp', type: 'temporal',axis: {title: 'Glucose levels'}},
							size: {value: 15},
							color: {value: 'grey'}
						}
					},
					{
						data: {values: this.$props.forecastData},
						mark: 'point',
						encoding: {
							y: {field: 'Glucose', type: 'quantitative'},
							x: {field: 'Timestamp', type: 'temporal',axis: {title: 'Glucose levels'}},
							size: {value: 20},
							color: {value: 'red'}
						}
					},
					]
				};
			// Embed the visualization in the container with id `vis`
			window.vegaEmbed('#vis', vlSpec);
		},
	},
}


</script>

<style scoped>
	#vis {
		width: 80%;
		height: 300px
	}
</style>