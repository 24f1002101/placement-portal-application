<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/counter';
import { computed } from 'vue';
import router from '@/router';
import { RouterLink } from 'vue-router';
import approved_companies from '@/components/approved_companies.vue';
const auth_store = useAuthStore();
const loginned = computed(()=>
    auth_store.isAuthenticated
)
const user_name = ref(JSON.parse(localStorage.getItem('user'))?.name || null)
const status = ref(JSON.parse(localStorage.getItem('user'))?.status || null)
const email = ref(JSON.parse(localStorage.getItem('email'))?.email || null)

function logout(){
    auth_store.clearAuthToken()
    alert("successfully logouted !!!")
    router.push("/")
}
</script>

<template>
    <div>
        <div v-if="loginned && status === 'approved' ">
            Hello,{{ user_name }} , {{ status }}
            <a v-on:click="logout">Logout</a>
            <a><RouterLink to="/edit_profile">Edit Profile</RouterLink></a>
            <a><RouterLink to="/application_history">View History</RouterLink></a>
            <approved_companies></approved_companies>
        </div>
        <div v-else-if=" loginned && (status === 'pending' || status === 'blacklist' )">
            Hello !!! {{ user_name }} | status : {{ status }}
            <p>You are not allowed to perform the functionalities !!!</p>
            <p><a v-on:click="logout">Logout</a></p>
        </div>
    </div>
</template>

<style scoped>

</style>