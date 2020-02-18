<!-- Form to add new glucose measurement -->
<!-- emit: add:newBG -->

<template>
<div id="glucose-form">

	<h3>Glucose levels</h3>

	<p>The interactive plot below shows you the past 12h of glucose levels and the predicted levels for the next 30 min. Hover over a point to compare past predictions and measured glucose levels.</p>

	<p>SweetTweet can also analyze new measurement, predict your levels for the next 30 min and warn you in case of impending hypoglycemia.</p>

	<form @submit.prevent="handleSubmit">
		<label>Enter your next glucose measurement:</label>
		<div id="glucose">
			<input  type="number" min="10" max="600"
			:class="{ 'has-error': submitting && invalidBG }"
			v-model="newBG"
			@focus="clearStatus"
			@keypress="clearStatus"
			ref="glucoseField">
			<button>Submit</button>
			<p v-if="error && submitting" class="error-message"> Please, enter a valid glucose measurement between 10 and 600.
			</p>
		</div>

		<p v-if="alarm == 1" class="important"> You're likely to dip below 70 mg/dL in the next 30min. How about some orange juice?
		</p>
	</form>

</div>
</template>

<script>
	export default {
		name : 'glucose-form',
		data() {
			return {
				submitting : false,
				error : false,
				success: false,
				newBG : ''
			}
		},
		props: {
			alarm: Number
		},
		methods: {
			// Set new glucose measurement
			handleSubmit() {
				this.submitting = true
				this.clearStatus()

				if (this.invalidBG) {
					this.error = true
					this.$refs.glucoseField.focus()
					return
				}

				this.$emit('add:newBG', this.newBG)
				this.newBG = ''
				this.error = false
				this.success = true
				this.submitting = false
				this.$refs.glucoseField.focus()
			},

			clearStatus() {
				this.success = false
				this.error = false
			},

		},
		computed: {
			invalidBG() {
				let BG_pattern = /^\d{2,3}$/;
				return this.newBG.match(BG_pattern) == null
			},
		},
	}
</script>

<style scoped>
form {
	margin-bottom: 2rem;
	margin: auto;
	width: 50%;
}
input[type=number] {
	width: 100px;
	height: 40px;
	margin-right: 10px;

}
#glucose {
	display: flex;
	flex-direction: row;
	justify-content: center;
}
.important {
	color: #eb4034;
}
</style>