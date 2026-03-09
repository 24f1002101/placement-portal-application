<script setup>
import { useAuthStore } from '@/stores/counter';
import { ref } from 'vue';
import { onMounted } from 'vue';
import { defineEmits } from 'vue';
const auth_store = useAuthStore();
const emit = defineEmits(['drive-closed'])
const ongoing_companies = ref([])
async function ongoing_drives(){
    const auth_token = auth_store.getAuthToken()
    const mail = auth_store.getUserEmail()
    const input = {
        email : mail
    }
    const response = await fetch("http://127.0.0.1:5000/api/ongoing_drives",{
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
        ongoing_companies.value = await response.json()
    }
}
async function close_drive(placement_id){
    const auth_token = auth_store.getAuthToken()
    const mail = auth_store.getUserEmail()
    const input = {
        id : placement_id
    }
    const response = await fetch("http://127.0.0.1:5000/api/close_drive",{
        method : "PUT",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
    })
    if(response.ok){
        const output = await response.json()
        alert(output.message)
        emit('drive-closed')
    }
    await ongoing_drives()
}
onMounted(()=>{
    ongoing_drives()
})
</script>

<template>
    <div>
        <p>Ongoing Drives</p>
        <div v-if="ongoing_companies.length > 0">
           <table border="1">
                <thead>
                    <th>Drive ID</th>
                    <th>Company Name</th>
                    <th>Job Role</th>
                    <th>Job Description</th>
                    <th>Eligible Year</th>
                    <th>Eligible Branch</th>
                    <th>Eligible CGPA</th>
                    <th>Action</th>
                </thead>
                <tbody>
                <tr v-for="drive in ongoing_companies" :key="drive.id">
                    <td>{{ drive.id }}</td>
                    <td>{{ drive.company_details.company_name }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.job_description }}</td>
                    <td>{{ drive.eligibility_year }}</td>
                    <td>{{ drive.eligibility_branch }}</td>
                    <td>{{ drive.eligibility_cgpa }}</td>
                    <td><RouterLink :to="`/get_applications/${drive.id}`"><button>View Details</button></RouterLink><button v-on:click="close_drive(drive.id)">mark as complete</button></td>
                </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            No Ongoing Drives by You !!!
        </div>
    </div>
</template>

<style scoped>

</style>