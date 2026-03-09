<script setup>
import { useAuthStore } from '@/stores/counter';
import { ref } from 'vue';
import { onMounted } from 'vue';
const auth_store = useAuthStore();
const closed_companies = ref([])
async function closed_drives(){
    const auth_token = auth_store.getAuthToken()
    const mail = auth_store.getUserEmail()
    const input = {
        email : mail
    }
    const response = await fetch("http://127.0.0.1:5000/api/closed_drives",{
        method : "POST",
        headers:
            {  
                "Content-Type" : "application/json",
                "Authentication-Token" : auth_token
            },
        body : JSON.stringify(input)
    })
    if(!response.ok){
        const output = await response.json()
        alert(output.message)
    }
    else{
        closed_companies.value = await response.json()
    }
}
onMounted(()=>{
    closed_drives()
})
</script>

<template>
    <div class="container mt-4">
        <p class="fw-bold fs-5">Closed Drives</p>
        <div v-if="closed_companies.length > 0">
            <table class="table table-bordered table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Placement ID</th>
                        <th>Company Name</th>
                        <th>Job Role</th>
                        <th>Job Description</th>
                        <th>Eligible Year</th>
                        <th>Eligible Branch</th>
                        <th>Eligible CGPA</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="drive in closed_companies" :key="drive.id">
                        <td>{{ drive.id }}</td>
                        <td>{{ drive.company_details.company_name }}</td>
                        <td>{{ drive.job_title }}</td>
                        <td>{{ drive.job_description }}</td>
                        <td>{{ drive.eligibility_year }}</td>
                        <td>{{ drive.eligibility_branch }}</td>
                        <td>{{ drive.eligibility_cgpa }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else class="alert alert-warning">
            No Closed Drives by You !!!
        </div>
    </div>
</template>

<style scoped>
</style>