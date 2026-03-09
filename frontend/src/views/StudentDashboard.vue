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
        <!-- Approved Student -->
        <div v-if="loginned && status === 'approved'">

            <!-- Navbar -->
            <nav class="navbar navbar-dark bg-dark px-4 mb-4">
                <span class="navbar-brand fw-bold">Student Dashboard</span>
                <div class="d-flex align-items-center gap-3">
                    <span class="text-white">Hello, <strong>{{ user_name }}</strong></span>
                    <span class="badge bg-success">{{ status }}</span>
                    <RouterLink to="/edit_profile" class="btn btn-outline-light btn-sm">Edit Profile</RouterLink>
                    <RouterLink to="/application_history" class="btn btn-outline-light btn-sm">View History</RouterLink>
                    <button class="btn btn-danger btn-sm" @click="logout">Logout</button>
                </div>
            </nav>

            <div class="container">
                <approved_companies></approved_companies>
            </div>
        </div>

        <!-- Pending or Blacklisted Student -->
        <div v-else-if="loginned && (status === 'pending' || status === 'blacklist')" class="container mt-5">
            <nav class="navbar navbar-dark bg-dark px-4 mb-4 rounded">
                <span class="navbar-brand fw-bold">Student Dashboard</span>
                <div class="d-flex align-items-center gap-3">
                    <span class="text-white"><strong>{{ user_name }}</strong></span>
                    <span class="badge" :class="status === 'pending' ? 'bg-warning text-dark' : 'bg-danger'">{{ status }}</span>
                    <button class="btn btn-danger btn-sm" @click="logout">Logout</button>
                </div>
            </nav>
            <div class="alert alert-warning text-center">
                You are not allowed to perform the functionalities !!!
            </div>
        </div>

        <!-- Not Logged In -->
        <div v-else class="container mt-5">
            <div class="alert alert-warning text-center">
                Please <RouterLink to="/">login</RouterLink> to access this page.
            </div>
        </div>

    </div>
</template>

<style scoped>
</style>