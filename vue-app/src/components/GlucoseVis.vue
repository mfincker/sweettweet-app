<!-- Visualize BG data -->
<!-- Used in Live BG and historical BG (TODO) -->
<!-- Props: glucoseData -->

<template>
	<div id="vis">
	</div>
</template>

<script>
	export default {
		name : 'glucose-vis',

		props: {
			glucoseData: Array,
		},
		watch: {
			glucoseData: function(newVal) {
				if (newVal.length > 0) {
					this.plotGlucose()
				}
			}
		},

		methods: {
			plotGlucose() {
				var vlSpec = {
					$schema: 'https://vega.github.io/schema/vega-lite/v4.json',
					data: {values: this.$props.glucoseData},
					width: 'container',
					mark: 'point',
					encoding: {
						y: {field: 'Glucose', type: 'quantitative'},
						x: {field: 'Timestamp', type: 'temporal',axis: {title: 'Glucose levels'}
					}
				}
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
	}
</style>