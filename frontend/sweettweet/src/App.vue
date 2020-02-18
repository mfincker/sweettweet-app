<template>
  <div id="app">
    <div id='banner'>
      <h1><img src="../public/sweettweet.svg" alt='sweettweet logo' id="logo">SweetTweet</h1>
      <p>Helping you prevent hypoglycemia</p>
    </div>
    <user-form @add:userInfo="setUserInfo" />
    <glucose-form @add:newBG="addNewBG" v-if="full_user_info" :alarm="alarm"/>
    <glucose-vis :data="data" v-if="full_user_info"/>

    <footer>
      <span>&copy; Maeva Fincker - 2020</span>
      <br>
      Developped with Flask and Vue.js
      <br>
      Logo adapted from <a href="https://www.svgrepo.com/svg/3466/hummingbird">here</a>
    </footer>
  </div>
</template>

<script>
import GlucoseVis from '@/components/GlucoseVis.vue'
import GlucoseForm from '@/components/GlucoseForm.vue'
import UserForm from '@/components/UserForm.vue'

// Change base_url when deployed - Flask server base_url
// const base_url = 'http://sweettweet.me/'
const base_url = 'http://0.0.0.0:5000/'

export default {
  name: 'app',
  components: {
    GlucoseVis,
    GlucoseForm,
    UserForm
  },

  data() {
    return {
      newBG: "",
      alarm: 0,
      userInfo: {},
      data: [],
      full_user_info: false
    }
  },

  methods: {

    // Update userInfo object from UserForm
    setUserInfo(userInfo) {
      this.userInfo = userInfo
      this.userInfo.height = this.userInfo.feet * 0.3048 + this.userInfo.inch * 0.0254
      this.userInfo.bmi = this.userInfo.weight * 0.453 / (this.userInfo.height * this.userInfo.height)
      this.full_user_info = true
      this.getGlucoseData()
    },

    // POST new glucose measurement - returns past + predicted glucose level
    async addNewBG(newBG) {
      try {
        const response = await fetch(base_url + 'api/forecast-glucose/', {
          method: 'POST',
          body: JSON.stringify({'newBG' : newBG,
                                'data': this.data,
                                'alarm' : this.alarm,
                                'userInfo' : this.userInfo}),
          headers: {'Content-type' : 'application/json; charset=UTF-8', }
        })
        const data = await response.json() // server should return the phone number
        this.newBG = data.newBG
        this.data = data.data
        this.alarm = data.alarm
        this.userInfo = this.userInfo
      } catch(error) {
        console.error(error)
      }
    },

    // Get glucose pastData to initialize glucose-vis
    async getGlucoseData() {
      try {
        const response = await fetch(base_url + 'api/get-glucose/')
        const data = await response.json()
        this.data = data.data
      } catch(error) {
        console.error(error)
      }
    },


  },

  mounted() {
    // Initialize glucose data from server on mount
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
  
}
footer {
  color: #f2f2f2;
  background-color: #6e5773;
  padding: 20px 0px 10px 0px;
  font-size: 8pt;
}
footer > span {
  font-size: 10pt;
}
footer > a, footer > a:hover {
  color: white;
  text-decoration: none;
}
#banner {
  color: white;
  background-color: #6e5773;
  padding: 10px 0px;
}

h1 {
  color: white;
  font-size: 50pt;
  margin-bottom: 0px;
}
#banner > p {
  font-size: 15pt;
}
button {
  background-color: #d45d79;
  border: 1px solid #d45d79;
}

#logo {
  width: 80px;
  height: 80px;
}

button:hover {
  background-color: #6e5773;
  border: 1px solid #6e5773;;
}
</style>
