<template>
  <div id="app">
    <phone-form @add:newPhoneNumber="addPhoneNumber" :phoneNumber="phoneNumber"/>
    <glucose-form @add:newBG="addNewBG" />
    <glucose-vis :glucoseData="glucoseData"/>
  </div>
</template>

<script>
import GlucoseVis from '@/components/GlucoseVis.vue'
import GlucoseForm from '@/components/GlucoseForm.vue'
import PhoneForm from '@/components/PhoneForm.vue'

// Change base_url when deployed - Flask server base_url
const base_url = 'http://127.0.0.1:5000/'

export default {
  name: 'app',
  components: {
    PhoneForm,
    GlucoseVis,
    GlucoseForm,
  },

  data() {
    return {
      phoneNumber: "",
      glucoseData: [],
      newBG: "",
    }
  },

  methods: {

    // POST user phone number
    async addPhoneNumber(newPhoneNumber) {
      try {
        const response = await fetch(base_url + 'api/change-phone-number', {
          method: 'POST',
          body: JSON.stringify({'phoneNumber' : newPhoneNumber}),
          headers: {'Content-type' : 'application/json; charset=UTF-8', }
        })
        const data = await response.json() // server should return the phone number
        this.phoneNumber = data.phoneNumber
      } catch(error) {
        console.error(error)
      }
    },

    // POST new BG measurement - returns full live glucoseData + model output - TODO
    addNewBG() {
      console.log(this.glucoseData[this.glucoseData.length - 2])
      console.log(this.glucoseData[this.glucoseData.length - 1])
    },

    // Get live glucoseData from user session
    async getGlucoseData() {
      try {
        const response = await fetch(base_url + 'api/glucose-data')
        const data = await response.json()
        this.glucoseData = data
      } catch(error) {
        console.error(error)
      }
    },


  },

  mounted() {
    // TODO: initialize user session on server
    this.getGlucoseData()
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
