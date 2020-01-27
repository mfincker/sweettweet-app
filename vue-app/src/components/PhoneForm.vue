<!-- Form to add/update user phone number -->
<!-- emit: add:newPhoneNumber -->

<template>
	<div id='phone-form'>
		<form @submit.prevent="handleSubmit"
				v-if="empty">
			<label>Enter your phone number below to receive hypoglycemia alerts:</label>
			<input  type="text"
					:class="{ 'has-error': submitting && invalidPhone }"
					v-model="newPhoneNumber"
					@focus="clearStatus"
					@keypress="clearStatus"
					ref="phoneField">
			<p v-if="error && submitting" class="error-message">❗Please fill out your phone number as +10123456789
			</p>
			<button>Submit</button>
		</form>
		<div v-if="success" 
				class="success-message">
		<p>
Sending alerts to {{phoneNumber}}
  </p>
  <button @click="handleChangePhoneNumber">Change phone number</button>
  </div>
	</div>
</template>

<script>
	export default {
		name : 'phone-form',
		data() {
			return {
				submitting : false,
				error : false,
				success: false,
				newPhoneNumber : '',
				empty: true 
			}
		},

		props: {
			phoneNumber: String,
		},

		methods: {
			handleSubmit() {
				// console.log('Testing handleSubmit in phone-form');
				this.submitting = true
				this.clearStatus()

				if (this.invalidPhone) {
					this.error = true
					this.$refs.phoneField.focus()
					return
				}

				this.$emit('add:newPhoneNumber', this.newPhoneNumber)
				this.error = false
				this.success = true
				this.submitting = false
				this.empty = false
				this.newPhoneNumber = ''
			},

			clearStatus() {
				this.success = false
				this.error = false
			},

			handleChangePhoneNumber() {
				this.clearStatus()
				this.newPhoneNumber = ''
				this.$emit('add:newPhoneNumber', this.newPhoneNumber)
				this.empty = true
				// this.$refs.phoneField.focus()
			},
		},
		computed: {
			invalidPhone() {
				let phoneno = /^\+\d{11,13}$/;
				return this.newPhoneNumber.match(phoneno) == null
			},
		},
	}
</script>

<style scoped>
	#phone_form {
		margin-bottom: 5em;
	}
  form {
    margin: auto;
    width: 50%;
  }
</style>