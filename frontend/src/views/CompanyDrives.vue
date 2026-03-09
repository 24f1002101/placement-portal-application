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
    <div>
        <div v-if="drives.length > 0">
                <table border="1">
                    <thead>
                        <th>Placement ID</th>
                        <th>Job Title</th>
                        <th>Job Description</th>
                        <th>Eligibility Year</th>
                        <th>Eligibility Branch</th>
                        <th>Eligibility CGPA</th>
                        <th>Application Deadline</th>
                        <th>Action</th>
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
                            <td><RouterLink :to="`/apply/${drive.placement_id}/${comp_id}`"><button>Apply</button></RouterLink></td>
                        </tr>
                    </tbody>
                </table>
                
            </div>
        <div v-else>
            "No drives are applied to your category to apply !!!"
        </div>
            <RouterLink to="/student_dashboard"><button>Go Back</button></RouterLink>
        </div>
</template>

<style scoped>
</style>