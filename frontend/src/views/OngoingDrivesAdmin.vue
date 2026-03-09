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
    <div class="container mt-4">

        <div v-if="companies.length > 0">
            <table class="table table-bordered table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Drive ID</th>
                        <th>Company Name</th>
                        <th>Job Role</th>
                        <th>Job Description</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="company in companies" :key="company.drive_id">
                        <td>{{ company.drive_id }}</td>
                        <td>{{ company.company_name }}</td>
                        <td>{{ company.Job_Role }}</td>
                        <td>{{ company.Job_Description }}</td>
                        <td>
                            <button class="btn btn-danger btn-sm" @click="change(company.drive_id)">
                                Mark as Complete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else class="alert alert-warning">
            No Ongoing Drives !!!
        </div>

        <RouterLink to="/admin_dashboard" class="btn btn-secondary mt-2">Go Back</RouterLink>

    </div>
</template>

<style scoped>
</style>