<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/counter';
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router';
const auth_store = useAuthStore()
const auth_token = auth_store.getAuthToken()
const email = auth_store.getUserEmail()
const route  = useRoute()
const drives = ref([])
const comp_id = route.params.company_id
console.log(route.params.company_id)
async function fetchcompanydrive(){
    const input = {
        company_id : route.params.company_id,
        email : email
    }
    const response = await fetch('http://127.0.0.1:5000/api/get_company_drives',{
        method : "POST",
        headers :{
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
    })
    if(response.ok){
        const output = await response.json()
        drives.value = output
    }
    else{
        const output = await response.json()
        alert(output.message)
    }
}
onMounted(()=>{
    fetchcompanydrive()
})
</script>

<template>
    <div class="container mt-4">

        <div v-if="drives.length > 0">
            <table class="table table-bordered table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Placement ID</th>
                        <th>Job Title</th>
                        <th>Job Description</th>
                        <th>Eligibility Year</th>
                        <th>Eligibility Branch</th>
                        <th>Eligibility CGPA</th>
                        <th>Application Deadline</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="drive in drives" :key="drive.placement_id">
                        <td>{{ drive.placement_id }}</td>
                        <td>{{ drive.job_title }}</td>
                        <td>{{ drive.job_description }}</td>
                        <td>{{ drive.eligibility_year }}</td>
                        <td>{{ drive.eligibility_branch }}</td>
                        <td>{{ drive.eligibility_cgpa }}</td>
                        <td>{{ drive.application_deadline }}</td>
                        <td>
                            <RouterLink :to="`/apply/${drive.placement_id}/${comp_id}`">
                                <button class="btn btn-primary btn-sm">Apply</button>
                            </RouterLink>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else class="alert alert-warning">
            No drives are available for your category !!!
        </div>

        <RouterLink to="/student_dashboard">
            <button class="btn btn-secondary mt-2">Go Back</button>
        </RouterLink>

    </div>
</template>

<style scoped>
</style>