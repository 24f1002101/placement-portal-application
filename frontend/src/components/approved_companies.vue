<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useAuthStore } from '@/stores/counter';
const auth_store = useAuthStore()
const auth_token = auth_store.getAuthToken()
const approved_companies = ref([])
async function fetchApprovedCompanies(){
    const response = await fetch("http://127.0.0.1:5000/api/display_all_approved_companies",{
        method : "GET",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        }
    })
    if(response.ok){
        approved_companies.value = await response.json()
        console.log(approved_companies.value)
    }
}
onMounted(()=>{
    fetchApprovedCompanies();
})
</script>

<template>
<div>
    <div v-if="approved_companies.length > 0">
        <table border="1">
            <thead>
                <th>Company</th>
                <th>Action</th>
            </thead>
            <tbody>
            <tr v-for="company in approved_companies" :key="company.id">
                <td>{{ company.company_name }}</td>
                <td><button><RouterLink :to="`/company/${company.company_id}/drives`">view details</RouterLink></button></td>
            </tr>
            </tbody>
        </table>
    </div>
    <div v-else>
        No Companies to View !!!
    </div>
</div>
</template>
<style scoped>
</style>