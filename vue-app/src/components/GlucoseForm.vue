<!-- Form to add new BG measurement -->
<!-- emit: add:newBG -->

<template>
<div id="glucose-form">
	<form @submit.prevent="handleSubmit">
		<label>Enter the next glucose measurement.</label>
		<input  type="text"
		:class="{ 'has-error': submitting && invalidBG }"
		v-model="newBG"
		@focus="clearStatus"
		@keypress="clearStatus"
		ref="glucoseField">
		<p v-if="error && submitting" class="error-message"> Please, enter a valid number between 10 and 600.
		</p>
		<button>Submit</button>
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
				newBG : '',
			}
		},
		methods: {
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
</style>