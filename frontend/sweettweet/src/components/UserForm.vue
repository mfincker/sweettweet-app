<!-- Form to add/update user info -->
<!-- age, gender, height, weight, insulinDelivery -->


<template>
	<div id='user-form'>
		<div class='hgroup'>
		<h3>User information</h3>
		<button id='user-info-mod' v-if="!show_user_info" @click="toggleUserInfo">Modify</button>
		</div>
		<p v-if='!show_user_info & phoneNumber_is_empty'>Sending SMS alerts to {{userInfo.phoneNumber}}.</p>
		<p v-if='!show_user_info & !phoneNumber_is_empty'>No phone number provided.</p>

		<div v-if="show_user_info">
			<p>Before SweetTweet can help you prevent low blood sugar, we need to learn more about you.
				<br>
			Your data is only stored locally and never saved on the server.</p>
			<div ref='genderField' class='field'>
				<label> What is your gender?</label>
				<div class='hgroup'>
				<div class='radio'>
					<input  type="radio"
							v-model="userInfo.gender" id="M" value="M"> 
					<label for="M">Male</label>
				</div>

				<div class='radio'>
					<input  type="radio"
							v-model="userInfo.gender" id="F" value="F">
					<label for="F">Female</label>
				</div>
				</div>
			</div>

			<div class='field'>
				<label> How old are you?</label>
				<input class='number' type="number" name="age" value="" v-model="userInfo.age" ref='ageField' min="0" max="150">
			</div>

			<div class='field' ref='heightField'>
				<label> How tall are you?</label>
				<div class="hgroup">
					<div class='range'>
					<input type="range" name="feet" min='0' max='7' v-model="userInfo.feet"> 
					<label for="feet">{{userInfo.feet}} ft</label>
					</div>

					<div class='range'>
					<input type="range" name="inch" min='0' max='11' v-model="userInfo.inch">
					<label for="inch">{{userInfo.inch}} in</label>
					</div>
				</div>

			</div>

			<div class='field'>
				<label> How much do you weigh?</label>
				<input class='number' type="number" name="weight" value="" v-model="userInfo.weight" ref='weightField' min="0" max="600">
				<label for="weight">lbs</label>

			</div>

			<div class='field' ref='insulinDeliveryField'>
				<label> How do you get your insulin?</label>
				<div class='hgroup'>
				<div class='radio'>
					<input  type="radio"
							v-model="userInfo.insulinDelivery" id="Pump" value="pump"> 
					<label for="Pump">Pump</label>
				</div>

				<div class='radio'>
					<input  type="radio"
							v-model="userInfo.insulinDelivery" id="Injection" value="injection">
					<label for="Injection">Injection</label>
				</div>
			</div>
			</div>

			<div class='field'>
				<label>What is your phone number?</label>
				SweetTweet can send you SMS alerts when you're about to be low.
				<input id="pnum" class='number' type="number" name="p-num" value="" v-model="userInfo.phoneNumber">


			</div>

			<button v-if="show_user_info" @click="handleSubmit">Submit</button>
		</div>


  </div>
</template>

<script>
	export default {
		name : 'user-form',
		data() {
			return {
				userInfo: {gender: 'F',
							age: '30',
							feet: 5,
							inch: 6,
							weight: '130',
							insulinDelivery: 'injection',
							phoneNumber: ''
							},
				show_user_info: true,
			}
		},

		methods: {
			handleSubmit() {
				this.$emit('add:userInfo', this.userInfo)
				this.toggleUserInfo()
			},
			toggleUserInfo() {
				this.show_user_info = !this.show_user_info
			}
		},
		computed: {
			gender_is_empty() {
				return this.userInfo.gender == ''
			},
			age_is_empty() {
				return this.userInfo.age == ''
			},
			weight_is_empty() {
				return this.userInfo.weight == 0
			},
			height_is_empty() {
				return this.userInfo.feet == 0
			},
			insulin_delivery_is_empty() {
				return this.userInfo.insulinDelivery == ''
			},
			phoneNumber_is_empty() {
				return this.userInfo.phoneNumber != ''
			}
		},
	}
</script>

<style scoped>
#user-form {
	padding: 5px 0px 10px 0px;
	background-color: #f2f2f2;
}
form {
	margin: auto;
	width: 100%;
}
.radio {
	display: flex;
	flex-direction: row;
	align-items: baseline;
	justify-content: center;
	padding: 0px 15px;
}
#height {
	margin: auto;
	width: 300px;
	display: flex;
	justify-content: space-between;
	flex-wrap: wrap;
}
.number {
	width: 100px;
	margin: auto;
}
.field {
	width: 50%;
	margin: 10px auto;
	background-color: white;
	border-radius: 10px;
	padding: 10px;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	flex-wrap: wrap;
}
.hgroup {
	display: flex;
	flex-direction: row;
	align-items: baseline;
	justify-content: center;
	flex-wrap: wrap;
}
input[type='number'] {
	height: 40px;
}
label {
	margin: 0px 0px 2px 0px;
}
#user-info-mod {
	margin: 0px 15px;
}
#pnum {
	width: 200px;
}
input[type='radio'] {
	margin-right: 10px;
}
.range {
	margin-right: 10px;
}
</style>