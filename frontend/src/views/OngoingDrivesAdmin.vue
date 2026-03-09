<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/counter';
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router';
const auth_store = useAuthStore()
const companies = ref([])
async function fetch_ongoing_drives(){
    const auth_token = auth_store.getAuthToken()
    const response = await fetch("http://127.0.0.1:5000/api/get_drives_admin",{
        method : "GET",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        }
    })
    if(response.ok){
        const output = await response.json()
        companies.value = output
    }
}
async function change(drive_id){
    const auth_token = auth_store.getAuthToken()
    const input = {
        drive_id : drive_id
    }
    const response = await fetch(" http://127.0.0.1:5000/api/update_drive",{
        method : "PUT",
        headers:{
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
    })
    if(response.ok){
        const output = await response.json()
        alert(output.message)
        fetch_ongoing_drives()
    }
    else{
        const output = await response.json()
        alert(output.message)
        return
    }
}
onMounted(()=>{
    fetch_ongoing_drives()
})
</script>

<template>
    <div>
        <div v-if="companies.length > 0 ">
            <table border="1">
                <thead>
                    <th>Drive ID</th>
                    <th>Company Name</th>
                    <th>Job Role</th>
                    <th>Job Description</th>
                    <th>Action</th>
                </thead>
                <tbody>
                    <tr v-for="company in companies">
                        <td>{{ company.drive_id }}</td>
                        <td>{{ company.company_name }}</td>
                        <td>{{ company.Job_Role }}</td>
                        <td>{{ company.Job_Description }}</td>
                        <td><button v-on:click="change(company.drive_id)">Mark as complete</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            No Ongoing Drives !!!
        </div>
        <div>
            <RouterLink to="/admin_dashboard">Go Back</RouterLink>
        </div>
    </div>
</template>

<style scoped>
</style>