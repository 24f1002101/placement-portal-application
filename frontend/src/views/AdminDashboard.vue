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
// Add this function to AdminDashboard.vue
function removeFromSearch(id) {
    // If we are searching students, filter by 'id', if companies, usually 'company_id'
    searchResults.value = searchResults.value.filter(item => 
        (item.id !== id && item.company_id !== id)
    );
}

// Then, pass this function down to your components
// <Companies :searchResults="searchResults" @action-taken="removeFromSearch" ... />
</script>

<template>
    <div v-if="username">
        <input v-model="search_value" placeholder="Search..." />

        <select v-model="searchType">
        <option value="student">Students</option>
        <option value="company">Companies</option>
        </select>

        <button @click="handleSearch">Search</button>
        <RouterLink to="/ongoing_drives_admin"><a>Ongoing Drives</a></RouterLink>
        <RouterLink to="/student_applications">Student Applications</RouterLink>
        {{username}}
        <Companies :searchResults="searchResults" :searchType="searchType" @action-taken="removeFromSearch"></Companies>
        <Students :searchResults="searchResults" :searchType="searchType" @action-taken="removeFromSearch"></Students>

        <a v-on:click="logouting">Logout</a>
    </div>
    <div v-else>
        <p>You must login first to view the functionalities !!!</p>
    </div>
</template>

<style scoped>

</style>