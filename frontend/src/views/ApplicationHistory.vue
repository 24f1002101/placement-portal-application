<script setup>
import { useAuthStore } from '@/stores/counter';
import { onMounted, ref } from 'vue';
import router from '@/router';
import Companies from '@/components/Companies.vue';
import Students from '@/components/Students.vue';
const auth_store = useAuthStore()
const search_value = ref('')
console.log(auth_store.isAuthenticated)
const username = ref(JSON.parse(localStorage.getItem('user'))?.name || null)
const searchType = ref('student')
const searchResults = ref([])
async function handleSearch(){
    const response = await fetch(`http://127.0.0.1:5000/api/admin_search?type=${searchType.value}&query=${search_value.value}`,{
        method : 'GET',
        headers: {
            "Authentication-Token" : auth_store.getAuthToken()
        }
    })
    if(response.ok){
        searchResults.value = await response.json()
    }
}
console.log(username)
function logouting(){
    auth_store.clearAuthToken()
    alert("Logouted Successfully !!!")
    router.push('/')
}
function removeFromSearch(id) {
    searchResults.value = searchResults.value.filter(item => 
        (item.id !== id && item.company_id !== id)
    );
}
</script>

<template>
    <div v-if="username">

        <!-- Navbar -->
        <nav class="navbar navbar-dark bg-dark px-4 mb-4">
            <span class="navbar-brand fw-bold">Admin Dashboard</span>
            <div class="d-flex align-items-center gap-3">
                <span class="text-white">{{ username }}</span>
                <RouterLink to="/ongoing_drives_admin" class="btn btn-outline-light btn-sm">Ongoing Drives</RouterLink>
                <RouterLink to="/student_applications" class="btn btn-outline-light btn-sm">Student Applications</RouterLink>
                <a class="btn btn-danger btn-sm" @click="logouting">Logout</a>
            </div>
        </nav>

        <!-- Search Bar -->
        <div class="container mb-4">
            <div class="row g-2 align-items-center">
                <div class="col-md-6">
                    <input class="form-control" v-model="search_value" placeholder="Search..." />
                </div>
                <div class="col-md-3">
                    <select class="form-select" v-model="searchType">
                        <option value="student">Students</option>
                        <option value="company">Companies</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <button class="btn btn-primary w-100" @click="handleSearch">Search</button>
                </div>
            </div>
        </div>

        <!-- Components -->
        <Companies :searchResults="searchResults" :searchType="searchType" @action-taken="removeFromSearch"></Companies>
        <Students :searchResults="searchResults" :searchType="searchType" @action-taken="removeFromSearch"></Students>

    </div>
    <div v-else class="container mt-5">
        <div class="alert alert-warning text-center">
            You must login first to view the functionalities !!!
        </div>
    </div>
</template>

<style scoped>
</style>