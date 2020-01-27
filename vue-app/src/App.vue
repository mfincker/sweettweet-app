<template>
  <div id="app">
    <phone-form @add:newPhoneNumber="addPhoneNumber" :phoneNumber="phoneNumber"/>
    <glucose-form @add:newBG="addNewBG" />
    <glucose-vis :pastData="pastData" :forecastData="forecastData"/>
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
      pastData: [],
      forecastData: [],
      newBG: "",
      alarm: 0
    }
  },

  methods: {

    // Update phoneNumber state
    addPhoneNumber(newPhoneNumber) {
      this.phoneNumber = newPhoneNumber
    },

    // POST new BG measurement - returns full live glucose data + model output - TODO
    async addNewBG(newBG) {
      try {
        const response = await fetch(base_url + 'api/update-glucose', {
          method: 'POST',
          body: JSON.stringify({'newBG' : newBG,
                                'pastData': this.pastData,
                                'phoneNumber' : this.phoneNumber,
                                'alarm' : this.alarm}),
          headers: {'Content-type' : 'application/json; charset=UTF-8', }
        })
        const data = await response.json() // server should return the phone number
        this.newBG = data.newBG
        this.pastData = data.pastData
        this.forecastData = data.forecastData
        this.alarm = data.alarm
      } catch(error) {
        console.error(error)
      }
    },

    // Get live pastData from user session
    async getGlucoseData() {
      try {
        const response = await fetch(base_url + 'api/glucose-data')
        const data = await response.json()
        this.pastData = data.pastData
        this.forecastData = data.forecastData
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
